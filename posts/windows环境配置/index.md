---
tags: windows
categories: 应用
banner_img_ratio: 25
---

{%note success%} 每次重装系统都需要重新配置一遍环境,索性将配置步骤记录下来,方便以后重装系统后使用{%endnote%}

# windows 环境配置(win10/11)

## 开发环境配置

### java

下载[jdk8 安装包](https://www.oracle.com/webapps/redirect/signon?nexturl=https://download.oracle.com/otn/java/jdk/8u202-b08/1961070e4c9b4e26a04e7f5a083f551e/jdk-8u202-windows-x64.exe)(需要登录 oracle),环境变量设置参数如下：

```bash
变量名：JAVA_HOME
变量值：D:\soft\java\jdk8

变量名：CLASSPATH
变量值：.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar;

变量名：Path
变量值：%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;
```

{%note warning%}

- `JAVA_HOME`要根据自己的实际路径配置
- `CLASSPATH`记得前面有个"."
- 在`Path`最前面新增变量值
  {%endnote%}

### python

下载 [python 安装包](https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe),安装之后如果没勾选添加 python.exe 到系统变量,环境变量需要设置参数如下:

```bash
变量名：PYTHON_HOME
变量值：D:\soft\python
```

{%note info%}

- 只有 python 的免安装版本需要配置
- `PYTHON_HOME`的路径根据自己 python 的实际路径配置
  {%endnote%}

### go

### git

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

   > sock5 代理地址根据实际情况修改

### maven

1. 在[maven 归档库](https://archive.apache.org/dist/maven/maven-3/)下载[压缩包](https://archive.apache.org/dist/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.zip),解压缩到软件目录
2. 新建系统变量 `MAVEN_HOME` 变量值：`D:\soft\apache-maven-3.6.3`
3. 在 `Path` 最后面添加变量值： `;%MAVEN_HOME%\bin`
4. 配置 `settings.xml` 该文件位于 **maven 安装目录 conf**下 配置如下
   {% fold success @settings.xml %}

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>

   <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

       <!-- 本地仓库路径 -->
       <localRepository>D:\mvn_repo</localRepository>

       <mirrors>
         <!-- 阿里云镜像 -->
         <mirror>
           <id>aliyun</id>
           <name>aliyun</name>
           <mirrorOf>central</mirrorOf>
           <url>https://maven.aliyun.com/repository/public</url>
         </mirror>
       </mirrors>

       <!-- 指定jdk版本 -->
       <profiles>
         <profile>
           <id>jdk8</id>
           <activation>
             <activeByDefault>true</activeByDefault>
             <jdk>8</jdk>
           </activation>
           <properties>
             <maven.compiler.source>8</maven.compiler.source>
             <maven.compiler.target>8</maven.compiler.target>
               <maven.compiler.compilerVersion>8</maven.compiler.compilerVersion>
           </properties>
         </profile>

       </profiles>

   </settings>
   ```

   {% endfold %}

### tomcat

1. 下载[tomcat 压缩包](https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.96/bin/apache-tomcat-8.5.96-windows-x64.zip),解压缩重命名为 tomcat
2. 新建环境变量`TOMCAT_HOME`,值为 Tomcat 所在的目录，例如 D:\soft\tomcat
3. 新建 `CATALINA_HOME` 和 `CATALINA_BASE`， 值都设为`%TOMCAT_HOME%`
4. 打开 PATH，在最后面添加变量值：`;%CATALINA_HOME%\lib;%CATALINA_HOME%\bin`

### idea

## 其他软件

### ffmpeg

### yt-dlp
