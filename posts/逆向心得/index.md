---
tags: 逆向
categories: 技术分享
# banner图片比例
banner_img_ratio: 20
# sticky: 20
---

## js 逆向技巧分享

当我们抓取网页端数据时，经常被加密参数、加密数据所困扰，如何快速定位这些加解密函数，尤为重要。本片文章是我逆向 js 时一些技巧的总结，如有遗漏，欢迎补充。

所需环境：Chrome 浏览器

## 1\. 搜索

### 1.1 全局搜索

> 适用于根据关键词快速定位关键文件及代码

当前页面右键->检查，弹出检查工具

![](https://pic2.zhimg.com/80/v2-f020da306c78f450a4ae1c4b2c129fcd_720w.jpg)

搜索支持 关键词、正则表达式

### 1.2 代码内搜索

> 适用于根据关键词快速定位关键代码

点击代码，然后按 ctrl+f 或 command+f 调出搜索框。搜索支持 关键词、css 表达式、xpath

![](https://pic1.zhimg.com/80/v2-5e22d4cf5e06c61e0d7067bb061f19e8_720w.jpg)

## 2\. debug

### 2.1 常规 debug

> 适用于分析关键函数代码逻辑

1.  埋下断点

![](https://pic4.zhimg.com/80/v2-6247db5fa1fe6a8a4bff702773ec52bb_720w.jpg)

1.  调试

![](https://pic3.zhimg.com/80/v2-b8899448ba6083942245b37ad98eb5f6_720w.jpg)

如图所示，我标记了 1 到 6，下面分别介绍其含义  
1.执行到下一个端点 2.执行下一步，不会进入所调用的函数内部 3.进入所调用的函数内部 4.跳出函数内部 5.一步步执行代码，遇到有函数调用，则进入函数 6.Call Stack 为代码调用的堆栈信息，代码执行顺序为由下至上，这对于着关键函数前后调用关系很有帮助

### 2.2 XHR debug

> 匹配 url 中关键词，匹配到则跳转到参数生成处，适用于 url 中的加密参数全局搜索搜不到，可采用这种方式拦截

![](https://pic4.zhimg.com/80/v2-4abddf7eb7623ef687439e1f382510db_720w.jpg)

### 2.3 行为 debug

> 适用于点击按钮时，分析代码执行逻辑

![](https://pic3.zhimg.com/80/v2-b01aa62b26eb0ce686a60e184bae3b06_720w.jpg)

如图所示，可快速定位点击探索按钮后，所执行的 js。

## 3 查看请求调用的堆栈

可以在 Network 选项卡下，该请求的 Initiator 列里看到它的调用栈，调用顺序由上而下：

![](https://pic3.zhimg.com/80/v2-38a3fdfa0a35515c76768b69687847a6_720w.jpg)

## 4\. 执行堆内存中的函数

当 debug 到某一个函数时，我们想主动调用，比如传递下自定义的参数，这时可以在检查工具里的 console 里调用

![](https://pic1.zhimg.com/80/v2-3c624185fb64645fa8692005eb882cc0_720w.jpg)

此处要注意，只有 debug 打这个函数时，控制台里才可以调用。如果想保留这个函数，可使用 this.xxx=xxx 的方式。之后调用时无需 debug 到 xxx 函数，直接使用[http://this.xxx](https://link.zhihu.com/?target=http%3A//this.xxx)  即可。

## 5\. 修改堆栈中的参数值

![](https://pic3.zhimg.com/80/v2-09b6d59eb75e4d7ca489fbcce9a07d2e_720w.jpg)

## 6\. 写 js 代码

![](https://pic4.zhimg.com/80/v2-9a5555cda401cad444ea3dfb52a0d23f_720w.jpg)

## 7\. 打印 windows 对象的值

在 console 中输入如下代码，如只打印\_$开头的变量值

    for (var p in window) {
        if (p.substr(0, 2) !== "_$")
            continue;
        console.log(p + " >>> " + eval(p))
    }

## 8\. 勾子

> 以 chrome 插件的方式，在匹配到关键词处插入断点

### 8.1 cookie 钩子

> 用于定位 cookie 中关键参数生成位置

    var code = function(){
        var org = document.cookie.__lookupSetter__('cookie');
        document.__defineSetter__("cookie",function(cookie){
            if(cookie.indexOf('TSdc75a61a')>-1){
                debugger;
            }
            org = cookie;
        });
        document.__defineGetter__("cookie",function(){return org;});
    }
    var script = document.createElement('script');
    script.textContent = '(' + code + ')()';
    (document.head||document.documentElement).appendChild(script);
    script.parentNode.removeChild(script);

当 cookie 中匹配到了  `TSdc75a61a`， 则插入断点。

### 8.2 请求钩子

> 用于定位请求中关键参数生成位置

    var code = function(){
    var open = window.XMLHttpRequest.prototype.open;
    window.XMLHttpRequest.prototype.open = function (method, url, async){
        if (url.indexOf("MmEwMD")>-1){
            debugger;
        }
        return open.apply(this, arguments);
    };
    }
    var script = document.createElement('script');
    script.textContent = '(' + code + ')()';
    (document.head||document.documentElement).appendChild(script);
    script.parentNode.removeChild(script);

当请求的 url 里包含`MmEwMD`时，则插入断点

### 8.3 header 钩子

> 用于定位 header 中关键参数生成位置

    var code = function(){
    var org = window.XMLHttpRequest.prototype.setRequestHeader;
    window.XMLHttpRequest.prototype.setRequestHeader = function(key,value){
        if(key=='Authorization'){
            debugger;
        }
        return org.apply(this,arguments);
    }
    }
    var script = document.createElement('script');
    script.textContent = '(' + code + ')()';
    (document.head||document.documentElement).appendChild(script);
    script.parentNode.removeChild(script);

当 header 中包含`Authorization`时，则插入断点

### 8.4 manifest.json

> 插件的配置文件

    {
       "name": "Injection",
        "version": "2.0",
        "description": "RequestHeader钩子",
        "manifest_version": 2,
        "content_scripts": [
            {
                "matches": [
                    "<all_urls>"
                ],
                "js": [
                    "inject.js"
                ],
                "all_frames": true,
                "permissions": [
                    "tabs"
                ],
                "run_at": "document_start"
            }
        ]
    }

### 使用方法

1.  如图所示，创建一个文件夹，文件夹中创建一个钩子函数文件 inject.js 及 插件的配置文件 manifest.json 即可

![](https://pic2.zhimg.com/80/v2-466c412f419b2da241b7eadf06e62395_720w.jpg)

1.  打开 chrome 的扩展程序, 加载已解压的扩展程序，选择步骤 1 创建的文件夹即可

![](https://pic4.zhimg.com/80/v2-bb6e0984226a40a1fbbdd46ba48d9117_720w.jpg)

1.  切换回原网页，刷新页面，若钩子函数关键词匹配到了，则触发 debug

![](https://pic2.zhimg.com/80/v2-b725c92acc17c677ab5810ca982c6ded_720w.jpg)

## 9\. 破解无限 debugger 防调试

如果你打开 chrome 的检查工具，发现自动断到了如下的位置，那么这种手段为常用的反调试手段

![](https://pic3.zhimg.com/80/v2-aa924874e5a23c84a142593aef48ae42_720w.jpg)

对应的破解手段如下：

### 9.1 方法置空

![](https://pic4.zhimg.com/80/v2-7339341024846b7522ea7c7e7396bb5b_720w.jpg)![](https://pic2.zhimg.com/80/v2-aca246af4b8dbc9ab648006f6f5aa93d_720w.jpg)

从原函数中可以看到这是一个无限递归的函数，目的就是当你开启了检查工具时，出现无数次 debug，阻止你 debug 调试。那么我们重写这个函数就可以了，在 Console 一栏中使用匿名函数给本函数重新赋值，这样就把`_0x355d23`函数变为了一个空函数，达到了破解无限 debugger 的目的

![](https://pic2.zhimg.com/80/v2-b971a8fef2eb13a3513aedce48f69c1d_720w.jpg)

### 9.2 干掉定时器

适用于定时器类触发的 debug

    for (var i = 1; i < 99999; i++)window.clearInterval(i);

### 9.3 中间人拦截替换无限 debug 函数

推荐使用 mitmproxy 拦截

## 10\. console 中使用 xpath 或 css

    xpath: $x("your_xpath_selector")
    css: $$("css_selector")

## 总结

以上为我做 js 逆向分析时用到的手段，如有不足之处或更多技巧，欢迎指教补充。愿本文的分享对您之后分析 js 有所帮助。谢谢～
