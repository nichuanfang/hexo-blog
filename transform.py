import os

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
                    # 如果_posts文件夹不存在则创建
                    if not os.path.exists(fluid_posts_path):
                        os.mkdir(fluid_posts_path)
                    file_name = dir + '.md'
                    # 将文件移动到_posts文件夹
                    os.rename(os.path.join(post_root,post_file),os.path.join(fluid_posts_path,file_name))