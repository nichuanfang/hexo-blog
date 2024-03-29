---
# 标签
tags:
  - tools
  - music
  - youtube
# 分类
categories: 工具
# banner图片比例
# banner_img_ratio:
# 置顶配置 数字越大优先级越高
# sticky: 30
---

{%note success%}
**music-tool-kit**，主要使用场景为提取[youtube](https://www.youtube.com)和[bilibili](https://www.bilibili.com)视频中的音频,支持
**音频下载**,**元信息自动补全**,**音频截取**,**youtube 列表批量下载**,**自定义批量下载**
等.配合[spotify](https://open.spotify.com)的**本地文件**
功能可以极大的提升音乐体验([教程](https://www.bilibili.com/video/BV1VL411T7mp/?vd_source=04c6a0d121b6fb871e3d3c0a2554b29b))
{%endnote%}

> 本项目仅为个人使用,无任何商业用途,仅支持 m4a 格式的音乐

---

# 环境准备

## 安装

```bash
python -m pip install –upgrade pip
pip install -U music-tool-kit
```

![help](help.png)

{%note primary%}
**准备环境**

- [python](https://www.python.org/)版本:**3.11.0 及以上**
- 需安装[ffmpeg](https://ffmpeg.org/)并正确配置环境变量
- 如果需要下载 youtube 的音乐,需要准备**科学上网**环境
- `[]`标记的项目表示可不填
- 为规避特殊字符导致路径识别失败,**标题**、**路径**、**URL**等相关的参数尽量使用**双引号**

{%endnote%}

## 升级

```bash
pip install -U music-tool-kit
```

## 卸载

```bash
pip uninstall music-tool-kit
```

# 使用

## 音乐下载

```bash
mk  "网址" "[标题]"

```

**普通下载**
![download](download.png)

**列表下载**使用方法为 `mk "列表url | 列表序号"` ,**url 需要为 [youtube](https://www.youtube.com) 的列表格式(url 中含有
list=)**,如果想下载全部歌曲,直接输入 `mk "列表url |"` 即可!

例如:

```bash
mk "https://www.youtube.com/playlist?list=PL8B3F8A7B0A9F4DE8 | 1,2,3,4,5"
```

![download_list](batch_download.png)

{%note info%}

- 仅支持下载 youtube 的列表下载,url|后面的列表序号之间需要用逗号分隔

{%endnote%}

## 音乐搜索

```bash
mk -s "关键字"
```

![search](search.png)
支持 youtube bilibili 输出优先级 youtube > bilibili,输入列表序号,输入标题,完成下载

{%note info%}

- 最多显示 20 条数据
- 直接按`Enter`可以跳出序号选择界面,输入的序号不能超过最大返回的条目数
- 如果不想设置标题 直接按`Enter`即可

{%endnote%}

## 音乐剪辑

```bash
mk -c "输入的m4a文件" 开始时间 结束时间
```

![clip](clip.png)

> Tips: 时间格式为 `00:00:00`

## csv 批量模板

```bash
mk -t
```

生成的模板文件如下:
![csv_template](csv_template.png)
用户自行填写下载信息,保存后使用`mk "csv文件"`即可批量下载

| url | title | cover_url | start_time | end_time |
|-----|-------|-----------|------------|----------|
| 网址  | 标题    | 封面 url    | 开始时间       | 结束时间     |

## 批量下载

```bash
mk "csv文件"
```

![csv_download](csv_download.png)

# License

This work is released under the MIT license. A copy of the license is provided in
the [LICENSE](https://raw.githubusercontent.com/nichuanfang/music-tool-kit/main/LICENSE) file.
