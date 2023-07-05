#!/usr/local/bin/python
# coding=utf-8

# 处理api接口数据错乱问题(时间 乱序)
import json
import os
import datetime
import copy
import logging

logging.basicConfig(level=logging.INFO) 


UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def utc_format(json_data:dict,field:str):
  """将UTC时间转为GMT+8(中国标准时间)
  """  
  try:
    json_data[field] = (datetime.datetime.strptime(json_data[field], UTC_FORMAT) + datetime.timedelta(hours=8)).__str__()
  except:
    # 不处理
     pass

# 日期格式化后、排好序的文章列表
articles:list[dict] = []
# 不带prev和post的文章列表
articles_simple:list[dict] = []
# 文章的uid与分类关系表
article_uid_category:dict[str,list] = {}
# 文章的uid与标签关系表
article_uid_tag:dict[str,list] = {}
for dir_path,dir_list,file_list in os.walk(f'./public/api'):
    # 先处理文章列表
    for article_dir_path,article_dir_list,article_file_list in os.walk(dir_path+'/'+'articles'):
      for article_file in article_file_list:
        # 修正为中国时区
        with open(article_dir_path+'/'+article_file,'r',encoding='utf8') as article:
          article_json_data = json.load(article)
          date = article_json_data['date']
          # 将UTC时间转为东八区时间
          utc_format(article_json_data,'date')
          utc_format(article_json_data,'updated')
          articles.append(article_json_data)
          pass
      # 按照创建时间重新排序
      articles = sorted(articles, key=lambda k: k['date'],reverse=True)

      # 对每一篇文章的prev和post重新赋值
      for index,art in enumerate(articles):
        prev_post = {}
        next_post = {}
        if index == 0:
          # 深拷贝: 拷贝当前对象的属性以及内部的对象属性
          next_post = copy.deepcopy(articles[index+1])
        elif index == len(articles)-1:
          prev_post = copy.deepcopy(articles[index-1])
        else:
          prev_post = copy.deepcopy(articles[index-1])
          next_post = copy.deepcopy(articles[index+1])
        art['prev_post'] = prev_post
        art['next_post'] = next_post
        prev_post.pop('prev_post',None)
        prev_post.pop('next_post',None)
        next_post.pop('prev_post',None)
        next_post.pop('next_post',None)
        art_path:str = art['path']
        # encoding='utf8'配合ensure_ascii=False 防止中文乱码
        json.dump(art,open(f'./public/{art_path}','w+',encoding='utf8'),ensure_ascii=False)
        art.pop('prev_post',None)
        art.pop('next_post',None)
        art.pop('content',None)
        art.pop('toc',None)
        articles_simple.append(art)
        # 处理分类映射
        article_uid_category[art['uid']] = Stream(art['categories']).map(lambda category: category['name']).to_list()
        # 处理标签映射
        article_uid_tag[art['uid']] = Stream(art['tags']).map(lambda tag: tag['name']).to_list()
    for dir in dir_list:
      match dir:
        case 'authors':
            # 作者信息
            for authors_dir_path,authors_dir_list,authors_file_list in os.walk(dir_path+'/'+dir):
                for author_file in authors_file_list:
                  with open(authors_dir_path+'/'+author_file,'r',encoding='utf8') as author_f:
                    author = json.load(author_f)
                    author['post_list'] = articles_simple
                    json.dump(author,open(f'./public/api/authors/{author_file}','w+',encoding='utf8'),ensure_ascii=False)
        case 'categories':
            # 分类
            for categories_dir_path,categories_dir_list,categories_file_list in os.walk(dir_path+'/'+dir):
                for category_file in categories_file_list:
                  with open(categories_dir_path+'/'+category_file,'r',encoding='utf8') as category_f:
                    category = json.load(category_f)
                    postlist = []
                    for article in articles_simple:
                       if category['name'] in article_uid_category[article['uid']]:
                          # 该文章属于当前分类
                          postlist.append(article)
                    category['postlist'] = postlist
                    json.dump(category,open(categories_dir_path+'/'+category_file,'w+',encoding='utf8'),ensure_ascii=False)
                       
        case 'pages':
            # 页面
            pass
        case 'posts':
            # 文章分页信息
            for posts_dir_path,posts_dir_list,posts_file_list in os.walk(dir_path+'/'+dir):
                for post_file in posts_file_list:
                  with open(posts_dir_path+'/'+post_file,'r',encoding='utf8') as post_f:
                     post = json.load(post_f)
                     post['data'] = articles_simple
                     json.dump(post,open(posts_dir_path+'/'+post_file,'w+',encoding='utf8'),ensure_ascii=False)
        case 'tags':
            # 标签
            for tags_dir_path,tags_dir_list,tags_file_list in os.walk(dir_path+'/'+dir):
                for tag_file in tags_file_list:
                  with open(tags_dir_path+'/'+tag_file,'r',encoding='utf8') as tag_f:
                    tag = json.load(tag_f)
                    postlist = []
                    for article in articles_simple:
                       if tag['name'] in article_uid_tag[article['uid']]:
                          # 该文章属于当前标签
                          postlist.append(article)
                    tag['postlist'] = postlist
                    json.dump(tag,open(tags_dir_path+'/'+tag_file,'w+',encoding='utf8'),ensure_ascii=False)
        
        case _:
            # 缺省匹配
            pass
         
    # 处理外层的json数据
    for file in file_list:
      if file == 'features.json':
        # 推荐文章
        with open(dir_path+'/'+file,'r',encoding='utf8') as features_file:
          features:list[dict] = []
          count = 0
          for article in articles_simple:
              if article.__contains__('feature') and article['feature'] and count <3:
                features.append(article)
                count+=1
          json.dump(features,open(dir_path+'/'+file,'w+',encoding='utf8'),ensure_ascii=False)
      elif file == 'search.json':
        # 搜索文章
        with open(dir_path+'/'+file,'r',encoding='utf8') as search_file:
          search:list[dict] = json.load(search_file)
          Stream(search).for_each(lambda item: utc_format(item,'date'))
          json.dump(search,open(dir_path+'/'+file,'w+',encoding='utf8'),ensure_ascii=False)