#!/usr/local/bin/python
# coding=utf-8
from PIL import Image
import requests
import re
import base64
import os

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

# 将目录的图片转webp
def dir_to_webp(input_dir:str):
    for dir_path,dir_list,file_list in os.walk(input_dir):
        for file in file_list:
            if not file.endswith('.jpg') and not file.endswith('.jpeg') and not file.endswith('.png'):
                 continue
            file_to_webp(dir_path.replace('\\','/')+'/'+file,dir_path.replace('\\','/'))
            os.remove(dir_path+'/'+file)

if __name__ == '__main__':
    dir_to_webp(f'./source')
    base64_data = requests.api.get('https://crawler.vencenter.cn/wallpaper/random')
    #base64_data转换成图片
    imgdata = base64.b64decode(base64_data)
    with open('test.webp','wb') as file:
        file.write(imgdata)



