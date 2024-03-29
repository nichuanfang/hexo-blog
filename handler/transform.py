import datetime
import os
import re
import shutil
import sys
from io import BytesIO

import requests
from PIL import Image

img_regex = re.compile(r'[(](.*?)[)]', re.S)
jpg_png_pattern = re.compile('.(jpg|png)$')

theme = sys.argv[1]
# 新增的文件
changes_add = sys.argv[2]
# 修改的文件
changes_modify = sys.argv[3]
# [".github/workflows/pages.yml","posts/python学习/index.md"]
try:
	change_files_add = changes_add.replace(
		'[', '').replace(']', '').replace('"', '').split(',')
	change_files_modify = changes_modify.replace(
		'[', '').replace(']', '').replace('"', '').split(',')
except:
	change_files_add = []
	change_files_modify = []
# if len(change_files) == 0:
#     exit(0)
# 获取当前时间  格式为 yyyy-mm-dd hh:mm:ss
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def file_to_webp(input_path: str, output_path: str):
	"""将jpg,png转webp

	Args:
		input_path (str): 读入文件全路径
		output_path (str): 输出文件目录
	"""
	# 如果是jpg或者png 则转为webp
	im = Image.open(input_path).convert('RGB')
	quality = 92
	# 如果图片大小大于2/4m 则调整quality
	if os.path.getsize(input_path) > 2 * 1024 * 1024 and os.path.getsize(input_path) < 4 * 1024 * 1024:
		quality = 85
	if os.path.getsize(input_path) >= 4 * 1024 * 1024:
		quality = 80
	# 调整图片分辨率
	if im.size[0] > 1920:
		im = im.resize((1920, int(im.size[1] * 1920 / im.size[0])))
	im.save(output_path, 'WEBP', quality=quality)
	return output_path


if theme == 'fluid':
	fluid_posts_path = os.path.join(
		os.path.pardir, 'hexo-blog-fluid', 'source', '_posts')
	fluid_img_path = os.path.join(
		os.path.pardir, 'hexo-blog-fluid', 'source', 'img', 'post')
	
	
	def dl_img(head_lines: list, output_path: str, post_files: list):
		"""下载图片到指定文件夹

		Args:
			urls (list): 图片地址列表
			output_path (str): 指定路径
			post_files(list): 文章目录的所有文件
		"""
		for head_line in head_lines:
			head_line_split: list = head_line.split(':', 1)
			if len(head_line_split) != 2:
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
			if res_content.__sizeof__() > 2 * 1024 * 1024 and res_content.__sizeof__() < 4 * 1024 * 1024:
				quality = 85
			if res_content.__sizeof__() >= 4 * 1024 * 1024:
				quality = 80
			if im.size[0] > 1920:
				im = im.resize((1920, int(im.size[1] * 1920 / im.size[0])))
			if type == 'index_img_url':
				im.save(os.path.join(output_path, 'index.webp'),
				        'WEBP', quality=quality)
				if not ('index.webp' in post_files):
					post_files.append('index.webp')
			elif type == 'banner_img_url':
				im.save(os.path.join(output_path, 'banner.webp'),
				        'WEBP', quality=quality)
				if not ('banner.webp' in post_files):
					post_files.append('banner.webp')
	
	
	posts_update_dict = {}
	
	if os.path.exists(os.path.join(fluid_posts_path)):
		# 读取文章的更新时间 写入到posts_update_dict
		for fluid_root, fluid_dirs, fluid_files in os.walk(fluid_posts_path):
			for fluid_file in fluid_files:
				if fluid_file.endswith('.md'):
					post_date_item = {}
					with open(os.path.join(fluid_root, fluid_file), 'r', encoding='utf-8') as f:
						lines = f.readlines()
						for line in lines:
							if line.startswith('title:'):
								post_date_item['post_name'] = line.split(':', 1)[
									1].strip()
							elif line.startswith('date:'):
								post_date_item['date'] = line.split(':', 1)[
									1].strip()
							elif line.startswith('updated:'):
								post_date_item['updated'] = line.split(
									':', 1)[1].strip()
					posts_update_dict[post_date_item['post_name']
					] = post_date_item
		
		shutil.rmtree(os.path.join(fluid_posts_path))
	
	if os.path.exists(os.path.join(fluid_img_path)):
		shutil.rmtree(os.path.join(fluid_img_path))
	os.mkdir(os.path.join(fluid_posts_path))
	os.mkdir(os.path.join(fluid_img_path))
	# 遍历posts文件夹
	for root, dirs, files in os.walk('posts'):
		for dir in dirs:
			# 如果posts/{dir}/目录没有md文件 直接跳过
			if not os.path.exists(os.path.join(root, dir, 'index.md')):
				continue
			
			# 标记该文档是否需要更新
			dir_added = False
			dir_modified = False
			for change in change_files_add:
				# 说明新增了文章
				if change == f'posts/{dir}/index.md':
					dir_added = True
					break
			for change in change_files_modify:
				# 只要文章文件夹有改动 就说明修改了文章
				if change.__contains__(f'posts/{dir}/'):
					dir_modified = True
					break
			
			for post_root, post_dirs, post_files in os.walk(os.path.join(root, dir)):
				if 'index.md' not in post_files:
					continue
				# 如果 fluid_img_path/dir不存在则创建
				if not os.path.exists(os.path.join(fluid_img_path, dir)):
					os.mkdir(os.path.join(fluid_img_path, dir))
				# 将文件移动到对应的img文件夹
				for post_file in post_files:
					# 横幅图片
					if post_file.endswith(('.jpg', 'png', 'webp')):
						shutil.copy2(os.path.join(post_root, post_file), os.path.join(
							fluid_img_path, dir, post_file))
				
				# 处理post_file的头部
				with open(os.path.join(post_root, 'index.md'), 'r+', encoding='utf-8') as f:
					lines = f.readlines()
					try:
						first_index = lines.index('---\n')
						last_index = lines.index('---\n', first_index + 1)
						head_lines = lines[first_index + 1:last_index]
						left_lines = lines[last_index + 1:]
					except:
						head_lines = []
						left_lines = lines
					
					head_lines_bk = head_lines.copy()
					left_lines_bk = left_lines.copy()
					should_post_update = False
					
					# 对head_lines进行处理
					head_lines.append(f'title: {dir}\n')
					
					if dir_added:
						head_lines.append(f'date: {now}\n')
						head_lines.append(f'updated: {now}\n')
					elif dir_modified:
						if len(posts_update_dict) != 0 and dir in posts_update_dict.keys():
							if 'date' in posts_update_dict[dir].keys():
								head_lines.append(
									f'date: {posts_update_dict[dir]["date"]}\n')
							else:
								head_lines.append(f'date: {now}\n')
							head_lines.append(f'updated: {now}\n')
						else:
							head_lines.append(f'date: {now}\n')
							head_lines.append(f'updated: {now}\n')
					else:
						# 没改动 空部署
						if len(posts_update_dict) != 0 and dir in posts_update_dict.keys():
							if 'date' in posts_update_dict[dir].keys():
								head_lines.append(
									f'date: {posts_update_dict[dir]["date"]}\n')
							else:
								head_lines.append(f'date: {now}\n')
							if 'updated' in posts_update_dict[dir].keys():
								head_lines.append(
									f'updated: {posts_update_dict[dir]["updated"]}\n')
							else:
								head_lines.append(f'updated: {now}\n')
						else:
							head_lines.append(f'date: {now}\n')
							head_lines.append(f'updated: {now}\n')
					
					# 对left_lines的图片进行替换
					for i in range(len(left_lines)):
						if left_lines[i].__contains__('.jpg') or left_lines[i].__contains__('.png') or left_lines[
							i].__contains__('.webp'):
							# 根据正则表达式[^/\\(]+.(jpg|png) 找出符合的字符串
							result_list: list[str] = img_regex.findall(
								left_lines[i])
							for result in result_list:
								result = result.strip()
								# 如果是https或者http开头 不替换
								if result.startswith('https') or result.startswith('http'):
									continue
								elif result.endswith(('.jpg', 'png', 'webp')):
									try:
										# 判断该图片是否为jpg或者png 则转为webp
										if result.split('.')[-1] in ['jpg', 'png']:
											file_to_webp(os.path.join(post_root, result), os.path.join(
												fluid_img_path, dir, result.split('.')[0] + '.webp'))
											os.remove(os.path.join(
												fluid_img_path, dir, result))
											left_lines[i] = left_lines[i].replace(
												result, f'/img/post/{dir}/{result.split(".")[0] + ".webp"}')
										else:
											# 如果是/开头 则在前面加上posts/目录名
											if result.startswith('/'):
												left_lines[i] = left_lines[i].replace(
													result, f'/img/post/{dir}{result}')
											else:
												left_lines[i] = left_lines[i].replace(
													result, f'/img/post/{dir}/{result}')
									except:
										continue
					
					# 处理index图和banner图
					# 如果配置了index_img_url/banner_img_url 下载到当前文件夹下
					filtered_img_res = []
					for item in head_lines:
						if item.startswith(('index_img_url', 'banner_img_url')):
							head_lines_bk.remove(item)
							filtered_img_res.append(item)
							should_post_update = True
					if len(filtered_img_res) != 0:
						dl_img(filtered_img_res, os.path.join(
							fluid_img_path, dir), post_files)
					banner_extend = None
					index_extend = None
					if 'banner.png' in post_files:
						banner_extend = 'png'
					elif 'banner.jpg' in post_files:
						banner_extend = 'jpg'
					elif 'banner.webp' in post_files:
						banner_extend = 'webp'
					
					if 'index.png' in post_files:
						index_extend = 'png'
					elif 'index.jpg' in post_files:
						index_extend = 'jpg'
					elif 'index.webp' in post_files:
						index_extend = 'webp'
					
					if banner_extend and index_extend:
						# 如果图片为jpg或者png 则转为webp
						if banner_extend in ['jpg', 'png']:
							file_to_webp(os.path.join(post_root, f'banner.{banner_extend}'), os.path.join(
								fluid_img_path, dir, f'banner.webp'))
							shutil.copy2(os.path.join(fluid_img_path, dir, f'banner.webp'), os.path.join(
								post_root, f'banner.webp'))
							# 也需要保留生成好的webp图片到hexo目录 移除文章头部
							os.remove(os.path.join(fluid_img_path,
							                       dir, f'banner.{banner_extend}'))
							os.remove(os.path.join(post_root, f'banner.{banner_extend}'))
							banner_extend = 'webp'
							should_post_update = True
						# 如果图片为jpg或者png 则转为webp
						if index_extend in ['jpg', 'png']:
							file_to_webp(os.path.join(post_root, f'index.{index_extend}'), os.path.join(
								fluid_img_path, dir, f'index.webp'))
							shutil.copy2(os.path.join(fluid_img_path, dir, f'index.webp'), os.path.join(
								post_root, f'index.webp'))
							os.remove(os.path.join(fluid_img_path,
							                       dir, f'index.{index_extend}'))
							os.remove(os.path.join(post_root, f'index.{index_extend}'))
							index_extend = 'webp'
							should_post_update = True
						head_lines.append(
							f'banner_img: /img/post/{dir}/banner.{banner_extend}\n')
						head_lines.append(
							f'index_img: /img/post/{dir}/index.{index_extend}\n')
					elif banner_extend and index_extend == None:
						# 只设置了banner图
						if banner_extend in ['jpg', 'png']:
							file_to_webp(os.path.join(post_root, f'banner.{banner_extend}'), os.path.join(
								fluid_img_path, dir, f'banner.webp'))
							shutil.copy2(os.path.join(fluid_img_path, dir, f'banner.webp'), os.path.join(
								post_root, f'banner.webp'))
							os.remove(os.path.join(fluid_img_path,
							                       dir, f'banner.{banner_extend}'))
							os.remove(os.path.join(post_root, f'banner.{banner_extend}'))
							banner_extend = 'webp'
							should_post_update = True
						head_lines.append(
							f'banner_img: /img/post/{dir}/banner.{banner_extend}\n')
						head_lines.append(
							f'index_img: /img/post/{dir}/banner.{banner_extend}\n')
					elif index_extend and banner_extend == None:
						# 只设置了index图
						if index_extend in ['jpg', 'png']:
							file_to_webp(os.path.join(post_root, f'index.{index_extend}'), os.path.join(
								fluid_img_path, dir, f'index.webp'))
							shutil.copy2(os.path.join(fluid_img_path, dir, f'index.webp'), os.path.join(
								post_root, f'index.webp'))
							os.remove(os.path.join(fluid_img_path,
							                       dir, f'index.{index_extend}'))
							os.remove(os.path.join(post_root, f'index.{index_extend}'))
							index_extend = 'webp'
							should_post_update = True
						head_lines.append(
							f'banner_img: /img/post/{dir}/index.{index_extend}\n')
						head_lines.append(
							f'index_img: /img/post/{dir}/index.{index_extend}\n')
					else:
						# index图和banner图都不存在
						pass
					
					head_lines.insert(0, '---\n')
					head_lines.append('---\n')
					new_lines = head_lines + left_lines
					
					# 如果_posts文件夹不存在则创建
					if not os.path.exists(fluid_posts_path):
						os.mkdir(fluid_posts_path)
					file_name = dir + '.md'
					# 将处理后的文件写入
					with open(os.path.join(fluid_posts_path, file_name), 'w+', encoding='utf-8') as f:
						f.writelines(new_lines)
					# 移除头部的banner_img和index_img
					if should_post_update:
						with open(os.path.join(post_root, 'index.md'), 'w+', encoding='utf-8') as f:
							head_lines_bk.insert(0, '---\n')
							head_lines_bk.append('---\n')
							f.writelines(head_lines_bk + left_lines_bk)
							os.system(
								f'echo "should_post_update={should_post_update}" >> "$GITHUB_OUTPUT"')


elif theme == 'aurora':
	# todo
	pass
