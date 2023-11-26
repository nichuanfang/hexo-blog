---
# 标签
tags: 环境变量 windows
# 分类
categories: 应用
# banner图片比例
banner_img_ratio: 25
# 置顶配置 数字越大优先级越高
#sticky: 
title: windows环境变量配置
date: 2023-11-26 17:25:11
updated: 2023-11-26 17:43:05
banner_img: /img/post/windows环境变量配置/banner.webp
index_img: /img/post/windows环境变量配置/index.webp
---

# 开发环境配置(win10/11)

## java 

变量设置参数如下：

```shell
变量名：JAVA_HOME
变量值：D:\soft\java\jdk1.8.0_91        // 要根据自己的实际路径配置

变量名：CLASSPATH
变量值：.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;         //记得前面有个"."

变量名：Path
变量值：%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;
```

## python

## go

## git

## github

## maven

## tomcat

## ffmpeg

## yt-dlp

