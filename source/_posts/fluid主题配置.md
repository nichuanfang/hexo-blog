---
tags: hexo主题
categories: 应用
# banner图片比例
banner_img_ratio: 20
# sticky: 20
title: fluid主题配置
date: 2023-12-02 17:15:58
updated: 2023-12-02 17:15:58
banner_img: /img/post/fluid主题配置/banner.webp
index_img: /img/post/fluid主题配置/banner.webp
---

个人博客搭建心得 使用`hexo + fluid`主题

{%note success%}
本文主要介绍了个人博客搭建的心得， 使用`hexo + fluid`主题，以及一些常用的插件 。
{%endnote%}

## 1. Hexo

### 1.1. 安装

#### 1.1.1. Node.js

[Node.js 官网](https://nodejs.org/en/)下载最新版本的 Node.js，目前最新版本为 14.15.4。

#### 1.1.2. Hexo

```bash
# 安装
npm install -g hexo-cli
# 查看版本
hexo -v
```

### 1.2. 初始化

#### 1.2.1. 初始化

```bash
# 初始化
hexo init blog
# 进入目录
cd blog
# 安装依赖
npm install
```
