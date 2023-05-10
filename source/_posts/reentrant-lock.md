---
title: 记一次可重入锁的实践心得
date: 2023-05-11T07:05:39+08:00
tags: ReentrantLock
categories: 可重入锁
cover: /img/life/day1.jpg
feature: false
---

## 可重入锁ReentrantLock高级特性

</br>

> ### `ReentrantLock`提供了`Synchronized`不具备的三个高级特性

---

1. 公平锁

```java
    /**
     * Creates an instance of {@code ReentrantLock}.
     * This is equivalent to using {@code ReentrantLock(false)}.
     */
    public ReentrantLock() {
        sync = new NonfairSync();
    }
```

2. 等待可中断

```java
    /**
     * 尝试锁定
     *
     * @param timeout 超时时间
     * @param unit    单位
     * @return boolean 尝试获取锁的结果
     * @throws InterruptedException 中断异常
     */
    public boolean tryLock(long timeout, TimeUnit unit)
            throws InterruptedException {
        return sync.tryAcquireNanos(1, unit.toNanos(timeout));
    }
```

3. 条件通知,一把锁可以生成多个条件,每个条件可以对应一个线程分组,可以通过condition对象来进行分组等待和唤醒,解决了`synchronized`关键字只能`notifyAll()`的问题

```java
    public Condition newCondition() {
        return sync.newCondition();
    }
```

:::warning
`ReentrantLock`条件通知使用注意点
:::

1. 每个condition可以绑定若干个线程,如果需要多个condition请先对线程进行分组;
2. 使用`await()`和`signal()`或者`signalAll()`之前需要先获取锁,在finally代码块中要释放锁;

> ### 实战演示

---
模拟三个线程,对其中两个线程分为一组绑定到`condition1`,剩下的一个线程单独一组绑定到`condition2`,main线程再分别唤醒等待状态的各线程组.

* 创建线程池

```java
    private final ThreadFactory threadFactory = ThreadFactoryBuilder.create().setNamePrefix("test").build();

    private final Executor executor = new ThreadPoolExecutor(Runtime.getRuntime().availableProcessors() + 1, Runtime.getRuntime().availableProcessors() + 1,
            10, TimeUnit.MINUTES, new LinkedBlockingQueue<>(16), threadFactory, new ThreadPoolExecutor.AbortPolicy());
```

* 初始化`CountDownLatch`和`ReentrantLock`,注册两个`condition`.

```java
        //闭锁1  让3个子线程同时启动
        CountDownLatch startCdl = new CountDownLatch(1);
        //闭锁2  main线程等待子线程都执行完毕再结束
        CountDownLatch endCdl = new CountDownLatch(3);
        //同步锁
        ReentrantLock lock = new ReentrantLock(false);

        Condition condition1 = lock.newCondition();
        Condition condition2 = lock.newCondition();
```

* 创建子线程,进入等待状态,等主线程唤醒

```java
    /**
     * 获取线程
     *
     * @param startCdl       开始同步器
     * @param endCdl         结束同步器
     * @param lock      锁
     * @param condition 条件
     * @return {@link Thread}
     */
    private Runnable getCallable(CountDownLatch startCdl, CountDownLatch endCdl, ReentrantLock lock, Condition condition) {
        return () -> {
            try {
                //让三个子线程同时启动
                startCdl.await();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            lock.lock();
            try {
                //await会释放当前锁
                condition.await();
                log.info("线程{}被唤醒,时间:{}", Thread.currentThread().getName(),new Date());
            } catch (InterruptedException e) {
                e.printStackTrace();
            } finally {
                log.info("线程:{}执行完毕,释放同步锁",Thread.currentThread().getName());
                //被唤醒后,需要释放当前持有的锁
                lock.unlock();
                //计数器为0主线程停止等待
                endCdl.countDown();
            }
        };
    }
    //启动三个子线程
    executor.execute(getCallable(startCdl,endCdl ,lock, condition1));
    executor.execute(getCallable(startCdl,endCdl ,lock, condition1));
    executor.execute(getCallable(startCdl,endCdl,lock, condition2));
```

* 主线程进行唤醒

```java
    log.info("Main线程开始执行....");
    startCdl.countDown();
    log.info("子线程正在等待....");

    lock.lock();
    condition1.signalAll();
    lock.unlock();
    try {
        //主线程阻塞2秒 区分两次唤醒
        Thread.sleep(2000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    lock.lock();
    condition2.signal();
    lock.unlock();
    try {
        log.info("等待三个子线程执行完毕");
        endCdl.await();
        log.info("main线程结束");
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
```

* 控制台输出. 可以看出两次唤醒相隔了两秒
![](https://img2023.cnblogs.com/blog/2092447/202212/2092447-20221214173438641-1508702632.png)

