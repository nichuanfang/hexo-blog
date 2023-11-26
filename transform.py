import os
import datetime
import sys
import re
import shutil
from PIL import Image
import requests
from io import BytesIO

img_regex = re.compile(r'[(](.*?)[)]',re.S)
jpg_png_pattern = re.compile('.(jpg|png)$')

theme = sys.argv[1]
changes = sys.argv[2]
# [".github/workflows/pages.yml","posts/python学习/index.md"]
try:
    change_files = changes.replace('[','').replace(']','').replace('"','').split(',')
except:
    change_files = []
# if len(change_files) == 0:
#     exit(0)
# 获取当前时间  格式为 yyyy-mm-dd hh:mm:ss
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def file_to_webp(input_path:str,output_path:str):
    """将jpg,png转webp

    Args:
        input_path (str): 读入文件全路径
        output_path (str): 输出文件目录
    """    
    # 如果是jpg或者png 则转为webp
    im = Image.open(input_path).convert('RGB')
    quality = 92
    # 如果图片大小大于2/4m 则调整quality
    if os.path.getsize(input_path) > 2*1024*1024 and os.path.getsize(input_path) < 4*1024*1024:
        quality = 85
    if os.path.getsize(input_path) >= 4*1024*1024:
        quality = 80
    # 调整图片分辨率
    if im.size[0] > 1920:
        im = im.resize((1920,int(im.size[1]*1920/im.size[0])))
    im.save(output_path,'WEBP',quality=quality)
    return output_path



if theme == 'fluid':
    fluid_posts_path = os.path.join(os.path.pardir,'hexo-blog-fluid','source','_posts')
    fluid_img_path = os.path.join(os.path.pardir,'hexo-blog-fluid','source','img','post')
    
    def dl_img(head_lines:list,output_path:str,post_files:list):
        """下载图片到指定文件夹

        Args:
            urls (list): 图片地址列表
            output_path (str): 指定路径
            post_files(list): 文章目录的所有文件
        """    
        for head_line in head_lines:
            head_line_split:list = head_line.split(':', 1)
            if len(head_line_split)!=2:
                continue
            type = head_line_split[0].strip()
            img_url = head_line_split[1].strip()
            try:
                response = requests.get(img_url)
            except:
                print(f'图片地址:{img_url}错误!')
                continue
            res_content = response.content
            im = Image.open(BytesIO(response.content))
            quality = 92
            # 如果图片大小大于2/4m 则调整quality
            if res_content.__sizeof__() > 2*1024*1024 and res_content.__sizeof__() < 4*1024*1024:
                quality = 85
            if res_content.__sizeof__()>= 4*1024*1024:
                quality = 80
            if im.size[0] > 1920:
                im = im.resize((1920,int(im.size[1]*1920/im.size[0])))
            if type == 'index_img_url':
                im.save(os.path.join(output_path,'index.webp'),'WEBP',quality=quality)
                if  not ('index.webp' in post_files):
                    post_files.append('index.webp')
            elif type == 'banner_img_url':
                im.save(os.path.join(output_path,'banner.webp'),'WEBP',quality=quality)
                if  not ('banner.webp' in post_files):
                    post_files.append('banner.webp')
    
    
    # 遍历posts文件夹
    for root, dirs, files in os.walk('posts'):
        for dir in dirs:
            # 只要一下文件做变更 视为更新文档
            assert_list = ['index.md','banner.jpg','banner.png','banner.webp','index.jpg','index.png','index.webp']
            # 标记该文档是否需要更新
            dir_changed = False
            for assert_file in assert_list:
                if len(change_files)!=0 and change_files.__contains__(f'posts/{dir}/{assert_file}'):
                    dir_changed = True
                    break
            # if skip_flag:
            #     continue
            for post_root, post_dirs, post_files in os.walk(os.path.join(root,dir)):
                if 'index.md' not in post_files:
                    continue
                # 如果 fluid_img_path/dir不存在则创建
                if not os.path.exists(os.path.join(fluid_img_path,dir)): 
                    os.mkdir(os.path.join(fluid_img_path,dir))
                    # 将文件移动到对应的img文件夹
                for post_file in post_files:
                    # 横幅图片
                    if post_file.endswith(('.jpg','png','webp')):
                        shutil.copy2(os.path.join(post_root,post_file),os.path.join(fluid_img_path,dir,post_file))
                
                # 处理post_file的头部
                with open(os.path.join(post_root,'index.md'),'r+',encoding='utf-8') as f:
                    lines = f.readlines()
                    try:
                        first_index = lines.index('---\n')
                        last_index = lines.index('---\n',first_index+1)
                        head_lines = lines[first_index+1:last_index]
                        left_lines = lines[last_index+1:]
                    except:
                        head_lines = []
                        left_lines = lines
                        
                    # 对head_lines进行处理
                    head_lines.append(f'title: {dir}\n')
                    # date和updated都设置为当前时间
                    if not os.path.exists(os.path.join(fluid_posts_path,dir+'.md')):
                        head_lines.append(f'date: {now}\n')
                    else:
                        # 读取os.path.join(fluid_posts_path,dir+'.md')文件的date
                        with open(os.path.join(fluid_posts_path,dir+'.md'),'r',encoding='utf-8') as f:
                            lines = f.readlines()
                            for line in lines:
                                if line.startswith('date:'):
                                    head_lines.append(line)
                                    break
                        # posts/python学习/index.md
                    if dir_changed:
                        head_lines.append(f'updated: {now}\n')
                    else:
                        # 读取os.path.join(fluid_posts_path,dir+'.md')文件的updated
                        with open(os.path.join(fluid_posts_path,dir+'.md'),'r',encoding='utf-8') as f:
                            lines = f.readlines()
                            for line in lines:
                                if line.startswith('updated:'):
                                    head_lines.append(line)
                                    break
                    
                    # 对left_lines的图片进行替换
                    for i in range(len(left_lines)):
                        if left_lines[i].__contains__('.jpg') or left_lines[i].__contains__('.png') or left_lines[i].__contains__('.webp'):
                            # 根据正则表达式[^/\\(]+.(jpg|png) 找出符合的字符串
                            result_list:list[str] = img_regex.findall(left_lines[i])
                            for result in result_list:
                                result = result.strip()
                                # 如果是https或者http开头 不替换
                                if result.startswith('https') or result.startswith('http'):
                                    continue
                                elif result.endswith(('.jpg','png','webp')):
                                    try:
                                        # 判断该图片是否为jpg或者png 则转为webp
                                        if result.split('.')[-1] in ['jpg','png']:
                                            file_to_webp(os.path.join(post_root,result),os.path.join(fluid_img_path,dir,result.split('.')[0]+'.webp'))
                                            os.remove(os.path.join(fluid_img_path,dir,result))
                                            left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}/{result.split(".")[0]+".webp"}')
                                        else:
                                            # 如果是/开头 则在前面加上posts/目录名
                                            if result.startswith('/'):
                                                left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}{result}')
                                            else:
                                                left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}/{result}')
                                    except:continue
                    
                    # 处理index图和banner图
                    # 如果配置了index_img_url/banner_img_url 下载到当前文件夹下
                    filtered_img_res = [item for item in head_lines if item.startswith(('index_img_url','banner_img_url'))]
                    if len(filtered_img_res)!=0:
                        dl_img(filtered_img_res,os.path.join(fluid_img_path,dir),post_files)
                    banner_extend = None
                    index_extend = None
                    if 'banner.webp' in post_files:
                        banner_extend = 'webp'
                    elif 'banner.png' in post_files:
                        banner_extend = 'png'
                    elif 'banner.jpg' in post_files:
                        banner_extend = 'jpg'
                        
                    if 'index.webp' in post_files:
                        index_extend = 'webp'
                    elif 'index.png' in post_files:
                        index_extend = 'png'
                    elif 'index.jpg' in post_files:
                        index_extend = 'jpg'
                    
                    if banner_extend and index_extend:
                        # 如果图片为jpg或者png 则转为webp
                        if banner_extend in ['jpg','png']:
                            file_to_webp(os.path.join(post_root,f'banner.{banner_extend}'),os.path.join(fluid_img_path,dir,f'banner.webp'))
                            os.remove(os.path.join(fluid_img_path,dir,f'banner.{banner_extend}'))
                            banner_extend = 'webp'
                        # 如果图片为jpg或者png 则转为webp
                        if  index_extend in ['jpg','png']:
                            file_to_webp(os.path.join(post_root,f'index.{index_extend}'),os.path.join(fluid_img_path,dir,f'index.webp'))
                            os.remove(os.path.join(fluid_img_path,dir,f'index.{index_extend}'))
                            index_extend = 'webp'
                        head_lines.append(f'banner_img: /img/post/{dir}/banner.{banner_extend}\n')
                        head_lines.append(f'index_img: /img/post/{dir}/index.{index_extend}\n')
                    elif  banner_extend and index_extend==None:
                        # 只设置了banner图
                        if banner_extend in ['jpg','png']:
                            file_to_webp(os.path.join(post_root,f'banner.{banner_extend}'),os.path.join(fluid_img_path,dir,f'banner.webp'))
                            os.remove(os.path.join(fluid_img_path,dir,f'banner.{banner_extend}'))
                            banner_extend = 'webp'
                        head_lines.append(f'banner_img: /img/post/{dir}/banner.{banner_extend}\n')
                        head_lines.append(f'index_img: /img/post/{dir}/banner.{banner_extend}\n')
                    elif  index_extend and banner_extend==None:
                        # 只设置了index图
                        if  index_extend in ['jpg','png']:
                            file_to_webp(os.path.join(post_root,f'index.{index_extend}'),os.path.join(fluid_img_path,dir,f'index.webp'))
                            os.remove(os.path.join(fluid_img_path,dir,f'index.{index_extend}'))
                            index_extend = 'webp'
                        head_lines.append(f'banner_img: /img/post/{dir}/index.{index_extend}\n')
                        head_lines.append(f'index_img: /img/post/{dir}/index.{index_extend}\n')
                    else:
                        # index图和banner图都不存在
                        pass
                    
                    head_lines.insert(0,'---\n')
                    head_lines.append('---\n')
                    new_lines = head_lines + left_lines
                    
                    # 如果_posts文件夹不存在则创建
                    if not os.path.exists(fluid_posts_path):
                        os.mkdir(fluid_posts_path)
                    file_name = dir + '.md'
                    # 将处理后的文件写入
                    with open(os.path.join(fluid_posts_path,file_name),'w+',encoding='utf-8') as f:
                        f.writelines(new_lines)
        # 如果在该分支删除文章 应该与fluid分支同步
        # for fluid_root,fluid_dirs,fluid_files in os.walk(fluid_posts_path):
        #     diff_dirs = fluid_dirs - dirs
        #     # 删除对应dir的文章
elif theme == 'aurora':
    # todo 
    pass