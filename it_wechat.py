# -*- coding: utf-8 -*-

import numpy as np
import itchat
import matplotlib.pyplot as plt

itchat.login()

friends = itchat.get_friends(update=True)[0:]


# ***-----统计好友性别比例-----***
# 初始化计数器
male = female = other = 0
# friends[0]是自己的信息，因此从friends[1]开始
for i in friends[1:]:
	sex = i['Sex']
	if sex == 1:
		male += 1
	elif sex == 2:
		female += 1
	else:
		other += 1
# 计算朋友总数
total = len(friends[1:])
# 打印输出好友性别比例
print(
	"男性好友: %.2f%%" % (float(male)/total * 100) + "\n" +
	"女性好友: %.2f%%" % (float(female)/total * 100) + "\n" +
	"不明性别好友: %.2f%%" % (float(other)/total * 100)
	)

label_name = ["Boy", "Girl", "Unknown"]
gender_list = [male, female, other]
plt.figure()
plt.bar(range(len(gender_list)), gender_list, tick_label=label_name)

# 绘图中文显示设置
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

plt.xlabel(u'性别')
plt.ylabel(u'人数')
plt.title(u'好友性别比例')

# 在柱状图上显示数字
x=np.arange(3)
y=np.array(gender_list)
for a,b in zip(x,y):
	plt.text(a, b+0.1, '%.2f' % b, ha='center', va= 'bottom',fontsize=12)


# ***-----获取各类信息-----***
# 定义函数，爬去所有好友的制定信息
def get_var(var):
	variable = []
	for i in friends[1:]:
		value = i[var]
		variable.append(value)
	return variable
# 调用函数，得到对应信息，并存入csv文件，保存到桌面
NickName = get_var("NickName")
Sex = get_var("Sex")
Province = get_var("Province")
City = get_var("City")
Signature = get_var("Signature")

# Excel 打开中文乱码问题 未解决
# 不过可以通过Excel->数据->文本导入的形式，将csv文件导入，就可以避免乱码问题
# from pandas import DataFrame
# data = {"NickName": NickName, "Sex": Sex, "Province": Province,
# 		"City": City, "Signature": Signature}
# frame = DataFrame(data)
# frame.to_csv('data.csv', encoding='utf_8_sig', index=True)

# ***-----统计好友城市分布-----***
city_dict = {}
x_city = []
y_city = []
for city_name in City:
	if city_name in city_dict:
		city_dict[city_name] += 1
	else:
		city_dict[city_name] = 1
city_list = sorted(city_dict.items(), key=lambda item:item[1], reverse=True)
# print city_list
for i in city_list[1:15]:
	x_city.append(i[0])
	y_city.append(i[1])


# 绘制城市分布柱状图
plt.figure()
plt.bar(range(len(x_city)), y_city, tick_label=x_city)
plt.xlabel(u'城市')
plt.ylabel(u'人数')
plt.title(u'好友城市分布')

# 在柱状图上显示数字
x=np.arange(len(x_city))
y=np.array(y_city)
for a,b in zip(x,y):
	plt.text(a, b+0.06, '%.2f' % b, ha='center', va='bottom', fontsize=9)


# ***-----根据个性签名绘制词云图-----***
# 通过正则匹配清洗数据
import re 
Signature_list = []
for i in friends:
	signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
	rep = re.compile("lf\d+\w*|[<>/=]")
	signature = rep.sub("", signature)
	Signature_list.append(signature)
text = "".join(Signature_list)

# 调包进行分词
import jieba 
wordlist = jieba.cut(text, cut_all=False)
word_space_split = " ".join(wordlist)

# 调包进行词云图绘制
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image

coloring = np.array(Image.open("weixin_sj520_33.jpg"))
my_wordcloud = WordCloud(background_color="white", max_words=200,
	mask=coloring, max_font_size=70, random_state=42, scale=2,
	font_path="C:\Windows\Fonts\SimHei.ttf").generate(word_space_split)
image_colors = ImageColorGenerator(coloring)
plt.figure()
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
