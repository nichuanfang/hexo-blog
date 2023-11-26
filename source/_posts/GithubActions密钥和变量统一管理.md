---
# 标签
tags: GithubActions
# 分类
categories: 技术
# banner图片比例
banner_img_ratio: 37
# 置顶配置 数字越大优先级越高
# sticky:
title: GithubActions密钥和变量统一管理
date: 2023-11-10 01:34:19
updated: 2023-11-27 02:54:02
banner_img: /img/post/GithubActions密钥和变量统一管理/banner.webp
index_img: /img/post/GithubActions密钥和变量统一管理/banner.webp
---

# 集中管理同一个账户下的变量和密钥

## 使用步骤

### 编辑[`config.json`](https://github.com/nichuanfang/.github/blob/main/config.json)

{%note info%}

topic: 当前区块的主要分类
repositories: 配置的变量和密钥应用到哪些仓库
vars: 全局变量 通过 ${{ vars.变量名  }} 调用
secrets: 全局密钥 通过 ${{ secrets.密钥名 }} 调用

{%endnote%}

### 触发工作流[`generate and sync`](https://github.com/nichuanfang/.github/actions/workflows/main.yml)

{%note info%}

1. your project-> Settings -> Secrets and variables -> config your secrets and variables

2. 生成的[`synchronize_secrets.yml`](https://github.com/nichuanfang/.github/blob/main/.github/workflows/synchronize_secrets.yml)和[`synchronize_variables.yml`](https://github.com/nichuanfang/.github/blob/main/.github/workflows/synchronize_variables.yml)为两个新的工作流

3. synchronize_variables.yml: 同步全局变量

4. synchronize_secrets.yml: 同步全局密钥

{%endnote%}
