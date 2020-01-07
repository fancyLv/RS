# -*- coding: utf-8 -*-
# @File  : mnist_cart.py
# @Author: LVFANGFANG
# @Date  : 2020/1/7 10:16 下午
# @Desc  :

import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# 加载数据
digits = load_digits()
data = digits.data
# 数据探索
print(data.shape)
# 查看第一幅图像
print(digits.images[0])
# 第一幅图像代表的数字含义
print(digits.target[0])
# 将第一幅图像显示出来
plt.gray()
plt.title('Handwritten Digits')
plt.imshow(digits.images[0])
plt.show()
# 分割数据，将25%的数据作为测试集，其余作为训练集
train_x, test_x, train_y, test_y = train_test_split(data, digits.target, test_size=0.25, random_state=2020)

# # 采用Z-Score规范化
# ss = StandardScaler()
# train_ss_x = ss.fit_transform(train_x)
# test_ss_x = ss.transform(test_x)

clf = DecisionTreeClassifier(criterion='gini')
# clf.fit(train_ss_x, train_y)
# predict_y = clf.predict(test_ss_x)
clf.fit(train_x, train_y)
predict_y = clf.predict(test_x)
print('CART准确率为:%0.4lf' % accuracy_score(predict_y, test_y))
