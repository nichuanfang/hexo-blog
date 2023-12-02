---
tags:
categories:
index_img_url:
banner_img_url:
banner_img_ratio:
sticky:
---

# 主题模板食用说明~

## Front-matter 说明

1. `tags`: 标签
2. `categories`: 分类
3. `index_img_url`: 首页缩略图 url 如果配置将忽略当前文件夹的 index.jpg
4. `banner_img_url`: 文章配图 url 如果配置将忽略当前文件夹的 banner.jpg
5. `banner_img_ratio`: banner 图片比例
6. `sticky`: 置顶配置 数字越大优先级越高

> [!NOTE]
>
> - 如果配置了 index_img_url,则当前文件夹下的 index.jpg 无效
> - 如果配置了 banner_img_url,则当前文件夹下的 banner.jpg 无效
> - 如果只配置了 index.jpg 或者 banner.jpg,则另一个缺省为同一个图片

## 便签

> [!NOTE]
>
> 这是笔记内容

> [!TIP]
>
> 这是提示内容

> [!IMPORTANT]
>
> 这是重要内容

> [!WARNING]
>
> 这是注意内容

> [!CAUTION]
>
> 这是警告内容

## 折叠块

使用折叠块，可以折叠代码、图片、文字等任何内容，你可以在 markdown 中按如下格式：

```bash
{% fold info @title %}
需要折叠的一段内容，支持 markdown
{% endfold %}
```

> info: 和行内标签类似的可选参数 title: 折叠块上的标题

## 分类

1. 作品
2. 工具
3. 技术
4. 应用
5. 方法
6. 杂谈
7. 其他

# 标签

Tags 根据需要灵活添加，但应避免添加太细的 tag 以避免膨胀，例如

1. linux
2. web
3. windows
4. Ubuntu
5. 机器学习
6. 大数据
7. docker
8. 分布式
9. 计算机网络
10. 设计
11. 工具
12. 日志
13. 编程语言
14. 计算机软件
15. 软件工程
16. 听歌
17. java
18. spring
19. redis
20. python
