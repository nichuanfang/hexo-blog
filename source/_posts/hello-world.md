---
# 文章标题
title: Hello World
# 创建日期
date: 2023-05-11T08:19:00+08:00
# 标签
tags: template
# 分类
categories: 测试
# 文章封面
# 这个feature属性将允许 Aurora 引擎找到这些文章，并将它们添加到推荐列表或置顶列表数据中。使用推荐布局模式或置顶布局模式。
feature: true
cover: /img/hello-world/hello-world.webp
---

---
Welcome to [Hexo](https://hexo.io/)! This is your very first post. Check [documentation](https://hexo.io/docs/) for more info. If you get any problems when using Hexo, you can find the answer in[troubleshooting](https://hexo.io/docs/troubleshooting.html) or you can ask me on [GitHub](https://github.com/hexojs/hexo/issues).

## 1. 快速开始

### 创建新文档

``` bash
hexo new "My New Post"
```

More info: [Writing](https://hexo.io/docs/writing.html)

### 启动本地服务

``` bash
hexo server
```

More info: [Server](https://hexo.io/docs/server.html)

### 构建静态文件

``` bash
hexo generate
```

More info: [Generating](https://hexo.io/docs/generating.html)

### 部署

``` bash
hexo deploy
```

More info: [Deployment](https://hexo.io/docs/one-command-deployment.html)

## 2. Markdown自定义容器

所有的自定义容器都使用这种格式:

```md
:::[type] [title]
文本内容
:::
```

- `type` 是容器的类型
- `title` 是可选的,可以用来重命名容器的标题

### Tip容器

```md
:::tip
Normal Tips Container
:::
```

![alt](/img/hello-world/tip.webp)

如果你不想使用默认的标题TIP，你可以使用以下方法重命名你的容器标题:

```md
:::tip Custom header

Custom header

- tips content
- tips new line

:::
```

![alt](/img/hello-world/tip-rename.webp)

### Warning 容器

```md
:::warning
Warning!!!
:::
```

![alt](/img/hello-world/warning.webp)

### Danger 容器

```md
:::danger
Danger!!!
:::
```

![alt](/img/hello-world/danger.webp)

### Details 容器

这是一种特殊类型的容器。如果你看过 GitHub 中的 details 容器，你可能会猜出它的功能是什么。

是的，您可以隐藏某些内容，并单击来展开它。

```md
:::details Click to see more

Fusce rutrum venenatis eros in hendrerit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam eget risus egestas, aliquet ipsum sed, volutpat tortor. Proin finibus tortor ac mauris finibus rutrum. Nullam tincidunt arcu eu urna ullamcorper, eu ultricies turpis ornare. Morbi id sollicitudin orci. Proin lobortis vehicula nibh a ornare. Cras sodales eu ligula quis fermentum. Proin eu ultrices leo, quis iaculis justo. Sed dictum, nulla sit amet imperdiet commodo, libero sapien semper justo, ut lobortis elit nunc vitae ante. Nullam lobortis odio quam, ac condimentum elit posuere vitae. Sed ornare, odio et rutrum varius, lorem eros gravida urna, in pharetra sapien justo non magna.

- details content
- details new line

`console.log('hello world')`

:::

```

**关闭状态:**

![alt](/img/hello-world/detail.webp)

**展开状态:**

![alt](/img/hello-world/detail-opened.webp)
