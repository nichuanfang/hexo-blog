# 读取public的文章

from genericpath import isdir
import os
import shutil 
import re
from bs4 import BeautifulSoup
import lxml


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

# 添加归档,分类,友链页面
post_list.append('public/archives/index.html')
post_list.append('public/categories/index.html')
post_list.append('public/links/index.html')

for post in post_list:
    # 修改html指定标签的内容
    with open(post, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
        # 修改图片比例
        raw_style = soup.find('div',class_='banner')['style']
        if post.replace('\\','/').split('/')[-2] in ['archives','categories','links']:
            # 对于archives, categories, links页面  banner_img_ratio默认为31
            banner_img_ratio = 31
        else:
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
            # raw_style_list = raw_style.split(' ')
            # # center 90% / cover no-repeat;
            # raw_style_list[4] = f'{banner_img_ratio}%;'
            # new_list = []
            # new_list.append(raw_style_list[0])
            # new_list.append(raw_style_list[1])
            # new_list.append(f'center {banner_img_ratio}% / cover no-repeat;')
            # new_list.append(raw_style_list[5])
            # new_list.append(raw_style_list[6])
            # soup.find('div',class_='banner')['style'] = ' '.join(new_list)
            raw_style_list = raw_style.split(' ')
            # center 90% / cover no-repeat;
            new_list = []
            new_list.append(raw_style_list[0])
            new_list.append(raw_style_list[1])
            new_list.append(raw_style_list[2])
            new_list.append(f'{banner_img_ratio}%;{raw_style_list[3].split(";",1)[1]}')
            soup.find('div',class_='banner')['style'] = ' '.join(new_list)
            
            # 保存
            saveFile(soup.__str__(),post)
        else:
            # 获取文章目录名称
            post_name = os.path.basename(os.path.dirname(post))
            
            # 查看source/img/post/文章文件夹下是否有图片
            if os.path.exists(os.path.join('source', 'img', 'post', post_name)):
                # 判断该文件夹是否包含banner图
                banner_flag = False
                for root, dirs, files in os.walk(os.path.join('source', 'img', 'post', post_name)):
                    for file in files:
                        if file.startswith('banner') and file.endswith(('.jpg','.png','.webp')):
                            # 设置了banner图  但没有设置banner_img_ratio头 默认使用center
                            banner_flag = True
                            break
                if not banner_flag:
                    # 没有设置banner图 使用默认图  需要设置比率30%
                    banner_img_ratio = 30
            else:
                banner_img_ratio = 30
            if banner_img_ratio:
                # 设置默认banner的比例
                # raw_style_list = raw_style.split(' ')
                # # center 90% / cover no-repeat;
                # raw_style_list[4] = f'{banner_img_ratio}%;'
                # new_list = []
                # new_list.append(raw_style_list[0])
                # new_list.append(raw_style_list[1])
                # new_list.append(f'center {banner_img_ratio}% / cover no-repeat;')
                # new_list.append(raw_style_list[5])
                # new_list.append(raw_style_list[6])
                # soup.find('div',class_='banner')['style'] = ' '.join(new_list)
                raw_style_list = raw_style.split(' ')
                # center 90% / cover no-repeat;
                new_list = []
                new_list.append(raw_style_list[0])
                new_list.append(raw_style_list[1])
                new_list.append(raw_style_list[2])
                new_list.append(f'{banner_img_ratio}%;{raw_style_list[3].split(";",1)[1]}')
                soup.find('div',class_='banner')['style'] = ' '.join(new_list)
                # 保存
                saveFile(soup.__str__(),post)
                
# seo优化

# 将rebot.txt复制到public文件夹下
shutil.copy2('robots.txt','public/robots.txt')
# 将googled6964a02c0841f8d.html复制到public下
shutil.copy2('googled6964a02c0841f8d.html','public/googled6964a02c0841f8d.html')
# 将baidu_verify_codeva-MeGg14ZRyV.html复制到public下
shutil.copy2('baidu_verify_codeva-MeGg14ZRyV.html','public/baidu_verify_codeva-MeGg14ZRyV.html')