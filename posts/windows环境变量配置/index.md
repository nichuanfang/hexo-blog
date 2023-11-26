---
# 标签
tags: 环境变量 windows
# 分类
categories: 应用
# banner图片比例
banner_img_ratio: 25
---

# 开发环境配置(win10/11)

## java

下载[jdk8 安装包](https://www.oracle.com/webapps/redirect/signon?nexturl=https://download.oracle.com/otn/java/jdk/8u202-b08/1961070e4c9b4e26a04e7f5a083f551e/jdk-8u202-windows-x64.exe)(需要登录 oracle),环境变量设置参数如下：

```bash
变量名：JAVA_HOME
变量值：D:\soft\java\jdk1.8.0_91

变量名：CLASSPATH
变量值：.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;

变量名：Path
变量值：%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;
```

{%note warning%}

- `JAVA_HOME`要根据自己的实际路径配置
- `CLASSPATH`记得前面有个"."
  {%endnote%}

## python

变量设置参数如下:

```bash
变量名：PYTHON_HOME
变量值：D:\soft\python
```

{%note warning%}

- 只有 python 的免安装版本需要配置
- `PYTHON_HOME`的路径根据自己 python 的实际路径配置
  {%endnote%}

## go

## git

1. 下载 [git 安装包](https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe)并安装,需要勾选**添加 git 到环境变量**
2. 配置`用户名`和`邮箱`

   ```bash
   git config --global user.name "用户名"
   git config --global user.email "邮箱"
   ```

3. 配置`代理`

   ```bash
   # 设置代理
   git config --global http.proxy 'socks5://127.0.0.1:10808'
   git config --global https.proxy 'socks5://127.0.0.1:10808'

   # 取消代理
   git config --global --unset http.proxy
   git config --global --unset https.proxy
   ```

## maven

## tomcat

## ffmpeg

## yt-dlp
