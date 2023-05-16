#!/usr/local/bin/python
# coding=utf-8

# 批量添加md文章的aurora主题header
import os
import random
import datetime

# 标签集
tag_flags = ['']

# 分类集  
# 01学习笔记 知识学习,基础,概念,教学,由浅入深,系统
# 02日志随笔 个人零散,无特殊目的的记录
# 03备忘清单 常用问题,知识的备忘记录
# 04解决方案 遇到的问题,发现问题,分析问题,解决问题,思路过程
# 05案例教程 运用到学的知识完成功能,解决问题,满足需求
# 06工具网站 工具就是能快速解决问题,需求,在线程序,应用
# 07学习资源 未被整理为笔记的知识,可以帮助提升自己的内容(视频,文档)
category_flags = ['学习笔记','日志随笔','备忘清单','解决方案','案例教程','工具网站','学习资源']

def randomtimes(start, end, frmt=r"%Y-%m-%d %H:%M:%S"):
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    return (random.random() * (etime - stime) + stime).strftime(frmt)

def get_tag(flag:str):
     return ''

def get_category(flag:str):
     return ''

for dir_path,dir_list,file_list in os.walk('./source/_posts'):
    for file in file_list:
        md_name = file.split('.')[0]
        header_lines = []
        final_lines = []
        with open(dir_path+'/'+file,'r',encoding='utf-8') as md_file:
            # 若干操作 修改html内容
            need_rewrite = True
            lines = md_file.readlines()
            for line in lines:
                if line.strip().replace('\n','') == '':
                    # 略过空行
                    continue
                if line.strip().replace('\n','') == '---':
                    # 已经有header了
                    need_rewrite = False
                    break
            if not need_rewrite:
                continue
            # 开始插入header
            # ---
            # title: {{ title }}
            # date: {{ date }}
            # tags:
            # categories:
            # cover:
            # feature: false
            # ---
            # header起始行
            header_lines.append('---\n')
            # 文档名称
            header_lines.append(f'title: {md_name}\n')
            # 文档日期
            header_lines.append(f'date: {randomtimes("2021-09-01 07:00:00","2023-04-21 09:00:00")}\n')
            # 标签
            # header_lines.append(f'tags: {get_tag(md_name)}\n')
            # 分类
            # header_lines.append(f'categories: {get_category(md_name)}\n')
            # cover由handle_img自动生成 无需声明
            header_lines.append('feature: false\n')
            # header结束行
            header_lines.append('---\n')
            final_lines = header_lines + lines
            with open(f'./source/_posts/{file}','w+',encoding='utf-8') as md:
                    md.writelines(final_lines)