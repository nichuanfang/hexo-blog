#!/usr/local/bin/python
# coding=utf-8
from requests import Response
from PIL import Image
import requests
import re
import base64
import os
from io import BytesIO
import subprocess
# 自动生成文档的图片 并将该图片转为webp格式

pattern = re.compile('.(png|jpeg|jpg)$')

def file_to_webp(input_path:str,output_path:str):
    """将jpg,jpeg,gif等转webp

    Args:
        input_path (str): 读入文件全路径
        output_path (str): 输出文件目录
    """    
    input_file_extension = input_path.split('/')[-1].split('.')[1]
    if input_file_extension in ["png","jpeg","jpg"]:
        # 根据正则表达式 替换目标字符串的内容 转为webp扩展
        output_path  = pattern.split(output_path)[0]+'/'+input_path.split('/')[-1].split('.')[0]+'.webp'
        im = Image.open(input_path) #读入文件
        print(im.size) #可查看图片大小
        im.thumbnail((1200,900), Image.ANTIALIAS) #重新设置图片大小
        im.save(output_path) #保存

def url_to_webp(img_url:str,img_path:str):
    """url转webp

    Args:
        img_url (str): 图片url
        img_path (str): 保存的图片路径 
    """
    res:Response = requests.get(img_url)
    base64_data = base64.b64encode(res.content).decode()
    imgdata = base64.b64decode(base64_data)
    im = Image.open(BytesIO(imgdata))
    im.thumbnail((1200,900), Image.ANTIALIAS) #重新设置图片大小
    im.save(img_path)

# 将目录的图片转webp
def dir_to_webp(input_dir:str):
    for dir_path,dir_list,file_list in os.walk(input_dir):
        for file in file_list:
            if not file.endswith('.jpg') and not file.endswith('.jpeg') and not file.endswith('.png'):
                 continue
            file_to_webp(dir_path.replace('\\','/')+'/'+file,dir_path.replace('\\','/'))
            os.remove(dir_path+'/'+file)

def random_img(file_path:str):
    """随机一张图片

    Args:
        path (str): 保存的文件路径
    """    
    file_name = file_path.split('/')[-1].split('.')[0]
    base64_data = requests.api.get('https://crawler.vencenter.cn/wallpaper/random')
    #base64_data转换成图片
    imgdata = base64.b64decode(base64_data.text)
    im = Image.open(BytesIO(imgdata))
    im.thumbnail((1200,900), Image.ANTIALIAS) #重新设置图片大小
    subprocess.call(f'mkdir -p ./source/img/{file_name}',shell=True)
    im.save(f'./source{file_path}')

if __name__ == '__main__':
    for dir_path,dir_list,file_list in os.walk('./source/_posts'):
        for file in file_list:
            md_name = file.split('.')[0]
            new_md = ''
            # 标记header的数量
            count = 0
            index = 0
            need_rewrite:bool = False
            rewrite_lines:list[str] = []
            is_update = False
            with open(dir_path+'/'+file,'r',encoding='utf-8-sig') as md_file:
                # 若干操作 修改html内容
                lines = md_file.readlines()
                for line in lines:
                    if count == 2:
                        # 直接输出index之后的内容
                        if not is_update:
                            rewrite_lines = rewrite_lines+lines[len(rewrite_lines)-1:]
                        else:
                            rewrite_lines = rewrite_lines+lines[len(rewrite_lines):]
                        break
                    if line.rfind('cover') == 0 :
                        handled_line = line.strip().replace(' ', '').replace('\n','')
                        if len(handled_line) > 6 and handled_line.endswith(('jpg','jpeg','png','webp')):
                            # 已有封面 跳过
                            break
                        else:
                            # 插入封面
                            new_cover = f'/img/{md_name}/{md_name}.webp'
                            random_img(new_cover)
                            line = f'cover: {new_cover}\n'
                            is_update = True
                            # 需要重写
                            need_rewrite = True    
                    if line.startswith('---'):
                        if count == 1:
                            # 插入封面
                            if not need_rewrite:
                                new_cover = f'/img/{md_name}/{md_name}.webp'
                                random_img(new_cover)
                                rewrite_lines.append(f'cover: {new_cover}\n')
                                index = index + 1
                            need_rewrite = True
                        count = count + 1
                    index = index + 1
                    rewrite_lines.append(line)
            # 保存到新的md文件
            if need_rewrite:
                # 只重写没有封面的文档
                with open(f'./source/_posts/{file}','w+',encoding='utf-8') as md:
                    md.writelines(rewrite_lines)
    
    # url_to_webp('https://w.wallhaven.cc/full/yx/wallhaven-yxqzpd.jpg','result.webp')



