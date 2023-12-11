# 读取public的文章

from genericpath import isdir
import json
import os
import shutil
import re
from bs4 import BeautifulSoup
import lxml
import requests
import re
import random


def saveFile(data, file_path):
    f_obj = open(f'{file_path}', 'w+', encoding="utf-8")  # w 表示打开方式,也可用wb
    f_obj.write(data)
    f_obj.close()


def update_baidu_ziyuan():
    # 读取sitemap.xml 更新到百度搜索平台
    with open('public/sitemap.xml', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # 通过正则表达式提取字符串<loc>https://blog.jaychou.site/about/index.html</loc>  <loc>和</loc>之间的内容
        urls = re.findall(r'<loc>(.*?)</loc>', ''.join(lines))
        # 将结果写入urls.txt 每行一条
        with open('seo/urls.txt', 'w+', encoding='utf-8') as f:
            for url in urls:
                f.write(url+'\n')

        headers = {
            'Content-Type': 'text/plain',
        }

        with open('seo/urls.txt', 'rb') as f:
            data = f.read()

        response = requests.post(
            'http://data.zz.baidu.com/urls?site=https://blog.jaychou.site&token=gXiKnZcZfevhKqhL',
            headers=headers,
            data=data,
        )
        if response.status_code == 200:
            print('百度搜索平台更新成功')

# 遍历public文件夹 获取所有文章


def get_public_list():
    post_list = []
    for year_root, year_dirs, year_files in os.walk('public'):
        for year_dir in year_dirs:
            # 定位年份
            if re.match(r'\d{4}', year_dir):
                year_post_path = os.path.join(year_root, year_dir)
                # 定位月份
                for month_root, month_dirs, month_files in os.walk(year_post_path):
                    for month_dir in month_dirs:
                        if re.match(r'\d{2}', month_dir):
                            month_post_path = os.path.join(
                                month_root, month_dir)
                            # 定位天
                            for day_root, day_dirs, day_files in os.walk(month_post_path):
                                for day_dir in day_dirs:
                                    if re.match(r'\d{2}', day_dir):
                                        day_post_path = os.path.join(
                                            day_root, day_dir)
                                        # 获取post_path下的文件夹
                                        for root, dirs, files in os.walk(day_post_path):
                                            for dir in dirs:
                                                post_path = os.path.join(
                                                    root, dir)
                                                post_list.append(os.path.join(
                                                    post_path, 'index.html'))

    return post_list


# key为第几张图片 value为img_ratio
default_img_dict = {}
for default_root, default_dirs, default_files in os.walk(os.path.join('source', 'img', 'bg', 'default')):
    for default_file in default_files:
        default_img_dict[default_file[:-5].split('_')[0]] = {
            'file_name': default_file,
            'ratio': default_file[:-5].split('_')[1]
        }
post_list = get_public_list()

# 添加归档,分类,友链页面
post_list.append('public/archives/index.html')
post_list.append('public/categories/index.html')
post_list.append('public/tags/index.html')
post_list.append('public/culture/index.html')
# 文艺
post_list.append('public/culture/books/index.html')
post_list.append('public/culture/documentaries/index.html')
post_list.append('public/culture/movies/index.html')
post_list.append('public/culture/music/index.html')
post_list.append('public/culture/shows/index.html')
post_list.append('public/culture/variety-show/index.html')
post_list.append('public/links/index.html')
post_list.append('public/index.html')
post_list.append('public/404.html')

for post in post_list:
    # 修改html指定标签的内容
    with open(post, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
        # 修改图片比例
        raw_style = soup.find('div', class_='banner')['style']
        post_name = post.replace('\\', '/').split('/')[-2]

        print(f'正在对文章: {post_name}进行处理')
        if post_name in ['archives', 'categories', 'public', 'tags', 'links', 'culture']:
            # 对于archives, categories, links页面  banner_img_ratio默认为31   42-29=13
            if post_name == 'culture' or post_name == 'books' or post_name == 'documentaries' or post_name == 'movies' \
                    or post_name == 'music' or post_name == 'shows' or post_name == 'variety-show':
                img_num = 3
            elif post_name == 'links':
                img_num = 4
            elif post_name == 'archives':
                img_num = 5
            elif post_name == 'categories':
                img_num = 1
            elif post_name == 'tags':
                img_num = 2
            else:
                img_num = 6
            banner_img_ratio = default_img_dict[str(img_num)]["ratio"]
        else:
            # 读取/source/_posts/文章.md里的banner_img_ratio
            raw_post_path = os.path.join(
                'source', '_posts', post_name+'.md')
            banner_img_ratio = None
            with open(raw_post_path, 'r', encoding='utf-8') as raw_post:
                raw_lines = raw_post.readlines()
                for line in raw_lines:
                    if line.startswith('banner_img_ratio:'):
                        banner_img_ratio = line.split(':')[1].strip()
                        break
            # 设置编辑页
            post_metas = soup.find('div', class_='post-metas my-3')

            edit_tag = soup.new_tag('div')
            edit_tag['class'] = 'post-meta'
            edit_tag['style'] = 'margin-left: auto'

            edit_tag_a = soup.new_tag('a')
            edit_tag_a['class'] = 'print-no-link'
            edit_tag_a[
                'href'] = f'https://github.com/nichuanfang/hexo-blog/edit/main/posts/{post_name}/index.md'
            edit_tag_a['target'] = '_blank'
            edit_tag_a_span = soup.new_tag(
                'span', style='color: #007bff', aria_label='hexo-blog')
            edit_tag_a_span['class'] = 'hint--top hint--rounded'
            edit_tag_a_span_i = soup.new_tag('i')
            edit_tag_a_span_i['class'] = 'iconfont icon-pen'
            edit_tag_a_span_i.append('在Github上编辑本页')
            edit_tag_a_span.append(edit_tag_a_span_i)
            edit_tag_a.append(edit_tag_a_span)
            edit_tag.append(edit_tag_a)
            post_metas.append(edit_tag)

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
            new_list.append(
                f'{banner_img_ratio}%;{raw_style_list[3].split(";",1)[1]}')
            soup.find('div', class_='banner')['style'] = ' '.join(new_list)
        else:
            # 获取文章目录名称
            post_name = os.path.basename(os.path.dirname(post))

            # 查看source/img/post/文章文件夹下是否有图片
            if os.path.exists(os.path.join('source', 'img', 'post', post_name)):
                # 判断该文件夹是否包含banner图
                banner_flag = False
                for root, dirs, files in os.walk(os.path.join('source', 'img', 'post', post_name)):
                    for file in files:
                        if file.startswith('banner') and file.endswith(('.jpg', '.png', '.webp')):
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
                new_list.append(
                    f'{banner_img_ratio}%;{raw_style_list[3].split(";",1)[1]}')
                soup.find('div', class_='banner')['style'] = ' '.join(new_list)
        # 保存
        saveFile(soup.__str__(), post)

# seo优化

# 将rebot.txt复制到public文件夹下
shutil.copy2('seo/robots.txt', 'public/robots.txt')
# 将googled6964a02c0841f8d.html复制到public下
shutil.copy2('seo/googled6964a02c0841f8d.html',
             'public/googled6964a02c0841f8d.html')
# 将baidu_verify_codeva-MeGg14ZRyV.html复制到public下
shutil.copy2('seo/baidu_verify_codeva-MeGg14ZRyV.html',
             'public/baidu_verify_codeva-MeGg14ZRyV.html')
# 更新百度搜索平台
update_baidu_ziyuan()
