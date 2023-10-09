---
title: python高级学习日志第四天之发布pypi包
date: 2023-10-9T23:00:00+08:00
tags: Python网络编程
categories: Python
cover: /img/python高级学习日志第四天之发布pypi包/python高级学习日志第四天之发布pypi包.jpg
---

## 打包相关的命令

egg 包文件有点老，一般我们只会生成 tar.gz 和 whl 文件, 用

```python
python setup.py sdist bdist_wheel
```

## 发布包到 PyPI

- 安装 twine

```python
pip install twine
```

- 配置~/.pypirc 文件

```python
[pypi]
  username = <username of pipi.org>
  password = <password>
```

- 上传 dist 文件夹下的包

```python
twine upload dist/*
```

> 总结打包发布的过程

```bash
1. pip install twine wheel
2. 配置好 setup.py 文件
3. python setup.py bdist_wheel
4. 配置 ~/.pypirc, 如果不想每次 upload 输入用户名/密码
5. twine upload dist/my-package-\*.whl
```
