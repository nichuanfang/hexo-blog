---
tags:
  - fluid
  - hexo
categories: 主题配置
index_img_url: https://pixabay.com/get/gc4a88896c4d477d84a476488651425d95402e9db4ee0bcebd39024d3e5f05fdaef4df79fda5225d2068d0522300b1483.jpg
# banner_img_ratio:
# sticky:
---

# 主题模板食用说明~

## Front-matter 说明

1. `tags`: 标签
2. `categories`: 分类
3. `index_img_url`: 首页缩略图 url 如果配置将忽略当前文件夹的 index.jpg
4. `banner_img_url`: 文章配图 url 如果配置将忽略当前文件夹的 banner.jpg
5. `banner_img_ratio`: banner 图片比例
6. `sticky`: 置顶配置 数字越大优先级越高

{%note info%}

- 如果配置了 index_img_url,则当前文件夹下的 index.jpg 无效
- 如果配置了 banner_img_url,则当前文件夹下的 banner.jpg 无效
- 如果只配置了 banner_img_url,则 index_img 使用相同的图片源
- 如果只配置了 index.jpg 或者 banner.jpg,则另一个缺省为 同一个图片

  {%endnote%}

## 便签

在 markdown 中加入如下的代码来使用便签：

```bash
{% note success %}
文字 或者 `markdown` 均可
{% endnote %}
```

可选便签：
{% note primary %}primary
{% endnote %}

{% note secondary %}secondary
{% endnote %}

{% note success %}success
{% endnote %}

{% note danger %}danger
{% endnote %}

{% note warning %}warning
{% endnote %}

{% note info %}info
{% endnote %}

{% note light %}light
{% endnote %}

{%note warning%}

使用时 `{% note primary %}` 和 `{% endnote %}` 需单独一行，否则会出现问题

{%endnote%}

## 折叠块

使用折叠块，可以折叠代码、图片、文字等任何内容，你可以在 markdown 中按如下格式：

```bash
{% fold info @title %}
需要折叠的一段内容，支持 markdown
{% endfold %}
```

> info: 和行内标签类似的可选参数 title: 折叠块上的 标题

## 分类

1. 技术：知识技能
2. 应用：应用笔记
3. 方法：方法论（经验谈），如工程方法
4. 工具：针对具体工具的介绍、使用方法、分析适用场景等；使用工具解决具体问题，应该放在「应用」里
5. 作品：自己的作品、个人项目日志等
6. 杂谈：生活、碎碎念，聊天打屁性质
7. 其他：没法分类的东西

## 标签

Tags 根据需要灵活添加，但应避免添加太细的 tag 以避免膨胀，例如

1. 细分领域：计算机技术、电子、嵌入式软件
2. 形式：日志
3. 具体内容：个人作品、生活、方法论、烹饪
