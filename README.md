---
tags:
categories:
index_img_url:
banner_img_url:
banner_img_ratio:
sticky:
---

---

- [主题模板食用说明~](#主题模板食用说明)
  - [Front-matter 说明](#front-matter-说明)
  - [便签](#便签)
    - [Github 自带便签](#github-自带便签)
    - [主题便签](#主题便签)
  - [折叠块](#折叠块)
    - [Github 自带折叠块](#github-自带折叠块)
    - [主题折叠块](#主题折叠块)
  - [分类](#分类)
  - [标签](#标签)

# 主题模板食用说明~

## Front-matter 说明

```BASH
---
tags:
categories:
index_img_url:
banner_img_url:
banner_img_ratio:
sticky:
---
```

- `tags`: 标签
- `categories`: 分类
- `index_img_url`: 首页缩略图 url 如果配置将忽略当前文件夹的 index.jpg
- `banner_img_url`: 文章配图 url 如果配置将忽略当前文件夹的 banner.jpg
- `banner_img_ratio`: banner 图片比例
- `sticky`: 置顶配置 数字越大优先级越高

> [!TIP]
>
> - 如果配置了 index_img_url,则当前文件夹下的 index.jpg 无效
> - 如果配置了 banner_img_url,则当前文件夹下的 banner.jpg 无效
> - 如果只配置了 index.jpg 或者 banner.jpg,则另一个缺省为同一个图片

## 便签

### Github 自带便签

> [!NOTE]
>
> 这是笔记内容

```bash
> [!NOTE]
>
> 这是笔记内容
```

> [!TIP]
>
> 这是提示内容

```bash
>  [!TIP]
>
> 这是提示内容
```

> [!IMPORTANT]
>
> 这是重要内容

```bash
> [!IMPORTANT]
>
> 这是重要内容
```

> [!WARNING]
>
> 这是注意内容

```bash
> [!WARNING]
>
> 这是注意内容
```

> [!CAUTION]
>
> 这是警告内容

```bash
> [!CAUTION]
>
> 这是警告内容
```

### 主题便签

> success

```bash
{% note success %}
文字 或者 `markdown` 均可
{% endnote %}
```

> primary

```bash
{% note primary %}
{% endnote %}
```

> secondary

```bash
{% note secondary %}
{% endnote %}
```

> success

```bash
{% note success %}
{% endnote %}
```

> danger

```bash
{% note danger %}
{% endnote %}
```

> warning

```warning
{% note warning %}
{% endnote %}
```

> info

```bash
{% note info %}
{% endnote %}
```

> light

```bash
{% note light %}
{% endnote %}
```

> [!warning]
>
> 使用时 {% note primary %} 和 {% endnote %} 需单独一行，否则会出现问题

## 折叠块

使用折叠块，可以折叠代码、图片、文字等任何内容，你可以在 markdown 中按如下格式：

### Github 自带折叠块

<details>
<summary>Click me</summary>
我是折叠块
</details>

```bash
<details>
<summary>Click me</summary>
我是折叠块
</details>

```

> summary 设置折叠块上的标题

### 主题折叠块

```bash
{% fold info @title %}
需要折叠的一段内容，支持 markdown
{% endfold %}
```

## 分类

> [!NOTE]
>
> 1. 作品
> 2. 工具
> 3. 技术
> 4. 应用
> 5. 方法
> 6. 杂谈
> 7. 其他

## 标签

Tags 根据需要灵活添加，但应避免添加太细的 tag 以避免膨胀，例如

> [!NOTE]
>
> 1. linux
> 2. web
> 3. windows
> 4. Ubuntu
> 5. 机器学习
> 6. 大数据
> 7. docker
> 8. 分布式
> 9. 计算机网络
> 10. 设计
> 11. 工具
> 12. 日志
> 13. 编程语言
> 14. 计算机软件
> 15. 软件工程
> 16. 听歌
> 17. java
> 18. spring
> 19. redis
> 20. python
