#!/usr/local/bin/python
# coding=utf-8

# 生成的静态资源处理 提升国内的访问速度
import os
import subprocess

from bs4 import BeautifulSoup
import re

base_path = '/root/code/hexo-blog'
# base_path = '.'


def saveFile(data,file_name):
    f_obj = open(f'{base_path}/public/post/{file_name}', 'w+',encoding="utf-8") # w 表示打开方式,也可用wb
    f_obj.write(data)
    f_obj.close()


# 拷贝js文件
subprocess.call(f'cp -rf {base_path}/source/js/* {base_path}/public/static/js',shell=True)


# 拷贝css文件
subprocess.call(f'cp -rf {base_path}/source/css/* {base_path}/public/static/css',shell=True)

# 处理public/post/*.html 将国外的资源全部替换为私服的资源

for dir_path,dir_list,file_list in os.walk(f'{base_path}/public/post'):
        for file in file_list:
            with open(dir_path+'/'+file,encoding="utf-8") as post_file:
                soup = BeautifulSoup(post_file,'lxml')
                # 替换静态资源
                js_scripts = soup.findAll('script',attrs={"src":re.compile(r'.js(.*)$')})
                css_links = soup.findAll('link',attrs={"href":re.compile(r'.css(.*)$')})
                for script in js_scripts:
                    src = script['src']
                    script['src'] = '/static/js/'+src.split('/')[-1]
                for link in css_links:
                    href = link['href']
                    link['href'] = '/static/css/'+href.split('/')[-1]
                # 保存
                saveFile(soup.__str__(),file)
