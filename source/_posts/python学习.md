---
# 标签
tags: python
# 分类
categories: 编程语言
# banner图片比例
banner_img_ratio: 10
title: python学习
date: 2023-11-09 04:18:36
updated: 2023-11-09 04:18:36
banner_img: /img/post/python学习/banner.jpg
index_img: /img/post/python学习/index.jpg
---

# Python 学习

## 1. Python 简介

{%note info%}

1. Python 是一种解释型、面向对象、动态数据类型的高级程序设计语言。Python 由 Guido van Rossum 于 1989 年底发明，第一个公开发行版发行于 1991 年。Python 语法简洁清晰，特色之一是强制用空白符(white space)作为语句缩进。

2. Python 具有丰富和强大的库。它常被昵称为胶水语言，它能够把用其他语言制作的各种模块（尤其是 C/C++）很轻松地联结在一起。常见的一种应用情形是，使用 Python 快速生成程序的原型（有时甚至是程序的最终界面），然后对其中[有特别要求的部分](https://zh.wikipedia.org/wiki/%E7%89%B9%E5%88%A5%E9%AB%94%E7%B3%BB)，用更合适的语言改写，比如[3D 游戏中的图形渲染模块，CPython](https://zh.wikipedia.org/wiki/CPython)就是这样产生的。

3. Python 解释器本身几乎可以在所有的操作系统中运行。Python 的官方解释器 CPython 是用 C 语言编写的、是一个[开源软件](https://zh.wikipedia.org/wiki/%E9%96%8B%E6%BA%90%E8%BB%9F%E9%AB%94)，目前由[Python 软件基金会](https://zh.wikipedia.org/wiki/Python%E8%BB%9F%E4%BB%B6%E5%9F%BA%E9%87%91%E6%9C%83)管理。它是一个[社群驱动](https://zh.wikipedia.org/wiki/%E7%A4%BE%E7%BE%A4%E9%A9%85%E5%8B%95)的[自由软件](https://zh.wikipedia.org/wiki/%E8%87%AA%E7%94%B1%E8%BB%9F%E9%AB%94)，源代码和[解释器实现](https://zh.wikipedia.org/wiki/%E8%A7%A3%E9%87%8A%E5%99%A8)遵循[GPL](https://zh.wikipedia.org/wiki/GNU%E9%80%A3%E7%8E%AF%E5%85%AC%E5%85%B1%E8%A8%B1%E5%8F%AF%E8%AD%89)（GNU General Public License）或[Python 软件基金会许可协议](https://zh.wikipedia.org/wiki/Python%E8%BB%9F%E4%BB%B6%E5%9F%BA%E9%87%91%E6%9C%83%E8%A8%B1%E5%8F%AF%E5%8D%94%E8%AD%B0%E6%9D%A1%E7%B4%84)（Python Software Foundation License）。

{%endnote%}

## 2. Python 安装

### 2.1. Windows

#### 2.1.1. 下载

[Python 官网](https://www.python.org/downloads/)下载最新版本的 Python，目前最新版本为 3.9.1。

#### 2.1.2. 安装

> 安装时注意勾选 `Add Python 3.9 to PATH`，这样就可以在命令行中直接使用 `python` 命令。

#### 2.1.3. 验证

> 在命令行中输入 `python`，如果出现以下信息，则说明安装成功。

```shell
Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", ...
```

### 2.2. Linux

#### 2.2.1. 下载

[Python 官网](https://www.python.org/downloads/)下载最新版本的 Python，目前最新版本为 3.9.1。

#### 2.2.2. 安装

```shell
# 下载
wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
# 解压
tar -zxvf Python-3.9.1.tgz
# 进入目录
cd Python-3.9.1
# 配置
./configure --prefix=/usr/local/python3
# 编译
make
# 安装
make install
```

#### 2.2.3. 验证

```shell
# 查看版本
python3 -V
# 进入交互式环境
python3
```
