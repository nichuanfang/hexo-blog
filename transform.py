import os
import datetime
import sys
import re
import shutil
from PIL import Image


img_regex = re.compile(r'[(](.*?)[)]',re.S)
jpg_png_pattern = re.compile('.(jpg|png)$')

theme = sys.argv[1]
changes = sys.argv[2]
# [".github/workflows/pages.yml","posts/python学习/index.md"]
try:
    change_files = changes.replace('[','').replace(']','').replace('"','').split(',')
except:
    change_files = []
if len(change_files) == 0:
    exit(0)
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
    im.save(output_path,'WEBP',quality=95)
    return output_path


if theme == 'fluid':
    fluid_posts_path = os.path.join(os.path.pardir,'hexo-blog-fluid','source','_posts')
    fluid_img_path = os.path.join(os.path.pardir,'hexo-blog-fluid','source','img','post')
    # 遍历posts文件夹
    for root, dirs, files in os.walk('posts'):
        for dir in dirs:
            # 只要一下文件做变更 视为更新文档
            assert_list = ['index.md','banner.jpg','banner.png','banner.webp','index.jpg','index.png','index.webp']
            skip_flag = True
            for assert_file in assert_list:
                if change_files.__contains__(f'posts/{dir}/{assert_file}'):
                    skip_flag = False
                    break
            if skip_flag:
                continue
            for post_root, post_dirs, post_files in os.walk(os.path.join(root,dir)):
                if 'index.md' not in post_files:
                    continue
                
                for post_file in post_files:
                    # 横幅图片
                    if post_file.endswith(('.jpg','png','webp')):
                        # 如果 fluid_img_path/dir不存在则创建
                        if not os.path.exists(os.path.join(fluid_img_path,dir)): 
                            os.mkdir(os.path.join(fluid_img_path,dir))
                            # 将文件移动到对应的img文件夹
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
                        # 读取os.path.join(fluid_posts_path,dir+'.md')文件的date和updated
                        with open(os.path.join(fluid_posts_path,dir+'.md'),'r',encoding='utf-8') as f:
                            lines = f.readlines()
                            for line in lines:
                                if line.startswith('date:'):
                                    head_lines.append(line)
                                    break
                        # posts/python学习/index.md
                    head_lines.append(f'updated: {now}\n')
                    
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
                                        # 判断该图片是否大于1m 且为jpg或者png 则转为webp
                                        if os.path.getsize(os.path.join(post_root,result)) > 1024*1024 and result.split('.')[-1] in ['jpg','png']:
                                            file_to_webp(os.path.join(post_root,result),os.path.join(fluid_img_path,dir,result.split('.')[0]+'.webp'))
                                            left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}{result.split(".")[0]+".webp"}')
                                        else:
                                            # 如果是/开头 则在前面加上posts/目录名
                                            if result.startswith('/'):
                                                left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}{result}')
                                            else:
                                                left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}/{result}')
                                    except:continue
                    
                    # 获取extend 优先级jpg>png>webp
                    banner_extend = None
                    index_extend = None
                    if 'banner.jpg' in post_files:
                        banner_extend = 'jpg'
                    elif 'banner.png' in post_files:
                        banner_extend = 'png'
                    elif 'banner.webp' in post_files:
                        banner_extend = 'webp'
                        
                    if 'index.jpg' in post_files:
                        index_extend = 'jpg'
                    elif 'index.png' in post_files:
                        index_extend = 'png'
                    elif 'index.webp' in post_files:
                        index_extend = 'webp'
                    if banner_extend:
                        # 如果图片大于1m且为jpg或者png 则转为webp
                        if os.path.getsize(os.path.join(post_root,f'banner.{banner_extend}')) > 1024*1024 and banner_extend in ['jpg','png']:
                            file_to_webp(os.path.join(post_root,f'banner.{banner_extend}'),os.path.join(fluid_img_path,dir,f'banner.webp'))
                            banner_extend = 'webp'
                        head_lines.append(f'banner_img: /img/post/{dir}/banner.{banner_extend}\n')
                    if index_extend:
                        # 如果图片大于1m且为jpg或者png 则转为webp
                        if  os.path.getsize(os.path.join(post_root,f'index.{index_extend}')) > 1024*1024 and index_extend in ['jpg','png']:
                            file_to_webp(os.path.join(post_root,f'index.{index_extend}'),os.path.join(fluid_img_path,dir,f'index.webp'))
                            index_extend = 'webp'
                        head_lines.append(f'index_img: /img/post/{dir}/index.{index_extend}\n')
                    
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
elif theme == 'aurora':
    # todo 
    pass