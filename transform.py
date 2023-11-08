import os
import datetime
import sys
import re


img_regex = re.compile(r'[(](.*?)[)]',re.S)
theme = sys.argv[1]
# 正则替换

# 获取现在的日期 格式yyyy-MM-dd HH:mm:ss 时区为中国
date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if theme == 'fluid':
    fluid_posts_path = os.path.join(os.path.pardir,'hexo-blog-fluid','source','_posts')
    fluid_img_path = os.path.join(os.path.pardir,'hexo-blog-fluid','source','img','post')
    # 遍历posts文件夹
    for root, dirs, files in os.walk('posts'):
        for dir in dirs:
            for post_root, post_dirs, post_files in os.walk(os.path.join(root,dir)):  
                for post_file in post_files:
                    # 横幅图片
                    if post_file.endswith('.jpg'):
                        # 如果 fluid_img_path/dir不存在则创建
                        if not os.path.exists(os.path.join(fluid_img_path,dir)):
                            os.mkdir(os.path.join(fluid_img_path,dir))
                        # 将文件移动到对应的img文件夹
                        os.rename(os.path.join(post_root,post_file),os.path.join(fluid_img_path,dir,post_file))
                    # 文档
                    elif post_file == 'index.md':
                        # 处理post_file的头部
                        with open(os.path.join(post_root,post_file),'r+',encoding='utf-8') as f:
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
                        head_lines.append(f'date: {date}\n')
                        
                        # 对left_lines的图片进行替换
                        for i in range(len(left_lines)):
                            if left_lines[i].__contains__('.jpg'):
                                # 根据正则表达式[^/\\(]+.(jpg|png) 找出符合的字符串
                                result_list:list[str] = img_regex.findall(left_lines[i])
                                for result in result_list:
                                    result = result.strip()
                                    # 如果是https或者http开头 不替换
                                    if result.startswith('https') or result.startswith('http'):
                                        continue
                                    elif result.endswith('.jpg') or result.endswith('.png'):
                                        # 如果是/开头 则在前面加上posts/目录名
                                        if result.startswith('/'):
                                            left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}{result}')
                                        else:
                                            left_lines[i] = left_lines[i].replace(result,f'/img/post/{dir}/{result}')
                        
                        # 如果当前目录下有banner.jpg则设置banner_img
                        if 'banner.jpg' in post_files:
                            head_lines.append(f'banner_img: /img/post/{dir}/banner.jpg\n')
                        # 如果当前目录下有index.jpg则设置index_img
                        if 'index.jpg' in post_files:
                            head_lines.append(f'index_img: /img/post/{dir}/index.jpg\n')
                        
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