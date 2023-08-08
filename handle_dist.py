#!/usr/local/bin/python
# coding=utf-8

# 生成的静态资源处理 提升国内的访问速度
import os
import subprocess
import lxml
from bs4 import BeautifulSoup
import re

# base_path = '/root/code/hexo-blog'
base_path = '.'


def saveFile(data,file_path):
    f_obj = open(f'{file_path}', 'w+',encoding="utf-8") # w 表示打开方式,也可用wb
    f_obj.write(data)
    f_obj.close()

def hand_soup(soup):
     # 替换静态资源
    js_scripts = soup.findAll('script',attrs={"src":re.compile(r'.js(.*)$')})
    css_links = soup.findAll('link',attrs={"href":re.compile(r'.css(.*)$')})
    # 加入<meta name="referrer" content="no-referrer" />  防止外链403
    meta = soup.new_tag('meta')
    meta['name'] = 'referrer'
    meta['content'] = 'no-referrer'
    soup.head.append(meta)
    for script in js_scripts:
        src = script['src']
        script['src'] = '/static/js/'+src.split('/')[-1]
    for link in css_links:
        href = link['href']
        # 处理rubik
        if href.endswith('family=Rubik'):
                link['href'] = '/static/css/rubik-css.css'
                continue
        link['href'] = '/static/css/'+href.split('/')[-1]

# 拷贝js文件
subprocess.call(f'cp -rf {base_path}/source/js/* {base_path}/public/static/js',shell=True)

# 拷贝css文件
subprocess.call(f'cp -rf {base_path}/source/css/* {base_path}/public/static/css',shell=True)


# 拷贝font文件
subprocess.call(f'mkdir -p {base_path}/public/static/font',shell=True)
subprocess.call(f'cp -rf {base_path}/source/font/* {base_path}/public/static/font',shell=True)

# 处理index.html
with open(f'{base_path}/public/index.html',encoding="utf-8") as index_file:
    soup = BeautifulSoup(index_file,'lxml')
    # 替换静态资源
    hand_soup(soup)
    # 保存
    saveFile(soup.__str__(),f'{base_path}/public/index.html')

# 处理tags
for dir_path,dir_list,file_list in os.walk(f'{base_path}/public/tags'):
        for file in file_list:
            if not file.endswith('.html') and not file.endswith('.htm'):
                 continue
            with open(dir_path+'/'+file,encoding="utf-8") as tag_file:
                soup = BeautifulSoup(tag_file,'lxml')
                # 替换静态资源
                hand_soup(soup)
                # 保存
                saveFile(soup.__str__(),dir_path+'/'+file)

# 处理page
for dir_path,dir_list,file_list in os.walk(f'{base_path}/public/page'):
        for file in file_list:
            if not file.endswith('.html') and not file.endswith('.htm'):
                 continue
            with open(dir_path+'/'+file,encoding="utf-8") as page_file:
                soup = BeautifulSoup(page_file,'lxml')
                # 替换静态资源
                hand_soup(soup)
                # 保存
                saveFile(soup.__str__(),dir_path+'/'+file)

# 处理public/post/*.html 将国外的资源全部替换为私服的资源
for dir_path,dir_list,file_list in os.walk(f'{base_path}/public/post'):
        for file in file_list:
            if not file.endswith('.html') and not file.endswith('.htm'):
                 continue
            with open(dir_path+'/'+file,encoding="utf-8") as post_file:
                soup = BeautifulSoup(post_file,'lxml')
                # 替换静态资源
                hand_soup(soup)
                # 保存
                saveFile(soup.__str__(),dir_path+'/'+file)

# 处理archives
for dir_path,dir_list,file_list in os.walk(f'{base_path}/public/archives'):
        for file in file_list:
            if not file.endswith('.html') and not file.endswith('.htm'):
                 continue
            with open(dir_path+'/'+file,encoding="utf-8") as archive_file:
                soup = BeautifulSoup(archive_file,'lxml')
                # 替换静态资源
                hand_soup(soup)
                # 保存
                saveFile(soup.__str__(),dir_path+'/'+file)