---
title: python高级学习日志第一天之网络编程
date: 2022-9-30T14:22:00+08:00
tags: Python网络编程
categories: Python
cover: /img/python高级学习日志第一天之网络编程/python高级学习日志第一天之网络编程.jpg
---

## python 高级学习日志第一天之网络编程

### UDP 发送数据

> 一个 Java 程序员，但是打算自学一下 python，所以把自己学到的东西记录在这里。也免得我自己忘记新学的，年纪大了真的很容易忘东西。

哈哈，我喜欢边写程序边听歌

> 中国人民真蒸汽

<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=433107530&auto=0&height=66"></iframe>

这里直接记录的是我的实践内容

**首先是怎么利用简单的 udp 来发送数据？**

这里我用的编辑工具是== Pycharm ==
测试的工具是 == 网络调试助手 ==
其中网络调试助手有多种样式的，下对了能用的就 ok，我的就长这样子：![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106212353613.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
利用 udp 进行简单的数据发送有四个步骤

1.  创建一个套接字
2.  从键盘读取你要发送的数据
3.  使用套接字发送你的数据
4.  关闭套接字

那么在 python 中要用到套接字，就像 java 导包一样也需要导入其中的套接字使用模块，使用 Pycharm 会自动提示不劝导入，真滴是特别的方便了。

接着在最后的位置给 python 设置一个启动器(main 方法)，类似，java 里的

```
public static void main(String[] args){}
```

python 里的写法是 main 方法：

```
if __name__ == '__main__':
```

在这个 main 函数缩进的位置上写上要执行的函数名就 ok
按照刚刚说的流程走一遍：

```python
#引入套接字使用模块
import socket


#自定义一个方法叫做main(),方法名随意
def main():
    #1.创建一个套接字,叫做udp_socket,固定的创建写法
    #其中SOCK_DGRAM是代表基于udp的套接字，无保障的
    udp_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #2.从键盘读取输入数据,赋值给send_data变量
    send_data = input("请输入要发送的数据:")

    #3.使用套接字发送数据
    #udp_socket套接字已经创建,用其自带的方法即可以实现发送,并且把发送的数据编码，防止中文输入乱码
    udp_socket.sendto(send_data.encode("gbk"), ("10.128.246.239", 6666))

    #4.关闭套接字
    udp_socket.close()


#在main方法里执行main()函数
if __name__ == '__main__':
    main()

```

ok,这是一个简单的流程，其中 10.128.246.239 和 6666 分别是要接受数据方的 ip 地址和端口号，接收方也是一个 udp，只不过这个 udp 用来接收数据，在这里用网络调试助手来模拟接收数据的 udp 方。

> 注意：套接字的 sendto 方法需要带两个参数，第一个是发送的数据，是 byte 类型的，第二个参数是一个元组，类似 java 里的数组，(ip 地址，端口号)，ip 地址是字符串类型的，端口号是整型的。

接下来用网络调试助手模拟数据接收方，打开网络调试助手，如下
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106215312639.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)新建一个 udp
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106215359375.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)其中 ip 地址换成当前联网的 ip，window 下可以用 win+R，输入 cmd 开启命令模式输入 ipconfig 即可查看当前网络的 ip
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106215618224.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
把这个 ip 地址输入到网络调试助手的设置区的本地 ip 位置，当然助手也能自动捕获，如图，用上这个就行
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106215854875.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
然后设置一个端口号，自己设置就行了，大于 1024 小于 65535 就行，排除电脑上有程序在用这个端口以外。启动，最终如下图，
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106220020862.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
这个时候通过代码里的参数配置，已经可以连接上这个接收器了，运行 python 程序
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106220213861.png)
点绿色按钮选择运行即可,运行如图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106220352802.png)
然后输入数据测试发送，输入后回车。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106220442349.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
这个时候回到网络调试助手可以看到：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106220529883.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
来自本机地址，因为是自己发给自己测试，这个端口发来的这个数据。

**这个时候开始想，能不能循环输入数据发送？**
答案是可以的，把发送数据执行的代码片作为循环体即可。然后可以简单地设置一下，当用户输入“exit”的时候，让用户结束发送。
然后代码变成了这样，把从键盘获取数据到发送数据作为循环体。用 while True: 圈起来，也就是把循环体一段缩进，相当于 java 中的{}大括号。然后用 if 判断用户输入的是不是 exit 字符串，是的话，则跳出循环，直接执行关闭套接字操作，程序运行结束。

```python
import socket


def main():
    # 创建一个udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # 从键盘获取数据
        send_data = input("请输入要发送的数据:")
        # 如果输入的数据是exit。则推出程序
        if send_data == "exit":
            break
        # 使用套接字发送数据
        udp_socket.sendto(send_data.encode("gbk"), ("10.128.246.239", 6666))
    # 关闭套接字
    udp_socket.close()


if __name__ == '__main__':
    main()

```

> 注意，if 里也用了缩进，就相当于 java 的{}

运行程序:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106221413209.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
这个时候，可以循环发送数据。打开网络调试助手：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106221456114.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
它也循环收到了数据
如果输入“exit”
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106221601628.png)
退出程序，结束发送。

这里我们可能会注意到这个细节
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190106221712480.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQwOTQ4Nzk1,size_16,color_FFFFFF,t_70)
有两种端口，这个是因为代码运行了两次，每次运行都由操作系统随机分配端口，总而言之，一个应用程序需要运行，则需要一个端口，当然在代码里也可以绑定端口，套接字绑定端口的操作会在 udp 接收数据里记录。

> 小白新学 python 之网络编程入门，大神勿喷
> 下一次记录  
> **怎么利用 udp 接收数据？**
