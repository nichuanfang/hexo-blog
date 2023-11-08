# 读取public的文章

from genericpath import isdir
import os
import shutil 
import re
from bs4 import BeautifulSoup
import lxml

# 将source/css/main.css拷贝到public/css/
shutil.copy('source/css/main.css','public/css/main.css')

def saveFile(data,file_path):
    f_obj = open(f'{file_path}', 'w+',encoding="utf-8") # w 表示打开方式,也可用wb
    f_obj.write(data)
    f_obj.close()


# 遍历public文件夹 获取所有文章
def get_public_list():
    post_list = []
    for year_root, year_dirs, year_files in os.walk('public'):
        for year_dir in year_dirs:
            # 定位年份
            if re.match(r'\d{4}', year_dir):
                year_post_path= os.path.join(year_root, year_dir)
                # 定位月份
                for month_root, month_dirs, month_files in os.walk(year_post_path):
                    for month_dir in month_dirs:
                        if re.match(r'\d{2}', month_dir):
                            month_post_path= os.path.join(month_root, month_dir)
                            # 定位天
                            for day_root, day_dirs, day_files in os.walk(month_post_path):
                                for day_dir in day_dirs:
                                    if re.match(r'\d{2}', day_dir):
                                        day_post_path = os.path.join(day_root, day_dir)
                                        # 获取post_path下的文件夹
                                        for root, dirs, files in os.walk(day_post_path):
                                            for dir in dirs:
                                                post_path = os.path.join(root, dir)
                                                post_list.append(os.path.join(post_path, 'index.html'))
                                        
    return post_list


post_list = get_public_list()
for post in post_list:
    # 修改html指定标签的内容
    with open(post, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
        # 修改图片比例
        raw_style = soup.find('div',class_='banner')['style']
        # 读取/source/_posts/文章.md里的banner_img_ratio
        raw_post_path = os.path.join('source', '_posts', post.replace('\\','/').split('/')[-2]+'.md')
        banner_img_ratio = None
        with open(raw_post_path, 'r', encoding='utf-8') as raw_post:
            raw_lines = raw_post.readlines()
            for line in raw_lines:
                if line.startswith('banner_img_ratio:'):
                    banner_img_ratio = line.split(':')[1].strip()
                    break
        if banner_img_ratio:
            raw_style_list = raw_style.split(' ')
            # center 90% / cover no-repeat;
            raw_style_list[4] = f'{banner_img_ratio}%;'
            new_list = []
            new_list.append(raw_style_list[0])
            new_list.append(raw_style_list[1])
            new_list.append(f'center {banner_img_ratio}% / cover no-repeat;')
            new_list.append(raw_style_list[5])
            new_list.append(raw_style_list[6])
            soup.find('div',class_='banner')['style'] = ' '.join(new_list)
            # 保存
            # saveFile(soup.__str__(),post)