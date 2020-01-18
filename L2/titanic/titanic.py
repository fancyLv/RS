# -*- coding: utf-8 -*-
# @File  : titanic.py
# @Author: LVFANGFANG
# @Date  : 2020/1/17 9:44 下午
# @Desc  :

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction import DictVectorizer
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from xgboost import XGBClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split

# 数据加载
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')
# 数据探索
# 查看train_data信息
print('查看数据信息：列名、非空个数、类型等')
print(train_data.info())
print('-' * 30)
print('查看数据摘要')
print(train_data.describe())
print('-' * 30)
print('查看离散数据分布')
print(train_data.describe(include=['O']))
print('-' * 30)
print('查看前5条数据')
print(train_data.head())
print('-' * 30)
print('查看后5条数据')
print(train_data.tail())

# 使用平均年龄来填充年龄中的nan值
train_data['Age'].fillna(train_data['Age'].mean(), inplace=True)
test_data['Age'].fillna(test_data['Age'].mean(), inplace=True)
# 使用票价的均值来填充票价中的nan值
train_data['Fare'].fillna(train_data['Fare'].mean(), inplace=True)
test_data['Fare'].fillna(test_data['Fare'].mean(), inplace=True)
# 使用登录最多的港口来填充登录港口的nan值
train_data['Embarked'].fillna(train_data['Embarked'].mode().values[0], inplace=True)
test_data['Embarked'].fillna(test_data['Embarked'].mode().values[0], inplace=True)
# 特征选择
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
train_features = train_data[features]
train_labels = train_data['Survived']
test_features = test_data[features]
print('特征值')
print(train_features)

dvec = DictVectorizer(sparse=False)
train_features = dvec.fit_transform(train_features.to_dict(orient='record'))
test_features = dvec.transform(test_features.to_dict(orient='record'))
print(dvec.feature_names_)

# 采用Z-Score规范化
ss = StandardScaler()
train_ss_x = ss.fit_transform(train_features)
test_ss_x = ss.transform(test_features)

# 构造ID3决策树
clf = DecisionTreeClassifier(criterion='entropy')
# 决策树训练
clf.fit(train_features, train_labels)

# 决策树预测
pred_labels = clf.predict(test_features)
# 得到决策树准确率(基于训练集)
acc_decision_tree = round(clf.score(train_features, train_labels), 6)
print('ID3决策树 score准确率为 %.4lf' % acc_decision_tree)
# 使用K折交叉验证 统计决策树准确率
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(clf, train_features, train_labels, cv=10)))

# 创建LR分类器
lr = LogisticRegression(solver='liblinear', multi_class='auto')
lr.fit(train_ss_x, train_labels)
pred_labels = lr.predict(test_ss_x)
print('LR score准确率为 %.4lf' % round(lr.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(lr, train_ss_x, train_labels, cv=10)))

# 创建LDA分类器
model = LinearDiscriminantAnalysis(n_components=2)
model.fit(train_ss_x,train_labels)
pred_labels = model.predict(test_ss_x)
print('LDA score准确率为 %.4lf' % round(model.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(model, train_ss_x, train_labels, cv=10)))


# 创建贝叶斯分类器
model = GaussianNB()
model.fit(train_ss_x,train_labels)
pred_labels = model.predict(test_ss_x)
print('朴素贝叶斯 score准确率为 %.4lf' % round(model.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(model, train_ss_x, train_labels, cv=10)))


# 创建SVM分类器
model = SVC(kernel='rbf',C=1.0,gamma='auto')
model.fit(train_ss_x,train_labels)
pred_labels = model.predict(test_ss_x)
print('SVM score准确率为 %.4lf' % round(model.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(model, train_ss_x, train_labels, cv=10)))


# 创建KNN分类器
model = KNeighborsClassifier()
model.fit(train_ss_x,train_labels)
pred_labels = model.predict(test_ss_x)
print('KNN score准确率为 %.4lf' % round(model.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(model, train_ss_x, train_labels, cv=10)))


# 创建AdaBoost分类器
dt_stump = DecisionTreeClassifier(max_depth=5,min_samples_leaf=1)
dt_stump.fit(train_ss_x,train_labels)
n_estimators = 500
model = AdaBoostClassifier(base_estimator=dt_stump,n_estimators=n_estimators)
model.fit(train_ss_x,train_labels)
pred_labels = model.predict(test_ss_x)
print('AdaBoost score准确率为 %.4lf' % round(model.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(model, train_ss_x, train_labels, cv=10)))


# 创建XGBoost分类器
model = XGBClassifier()
model.fit(train_ss_x,train_labels)
pred_labels = model.predict(test_ss_x)
print('XGBoost score准确率为 %.4lf' % round(model.score(train_ss_x, train_labels), 6))
print('cross_val_score准确率为 %.4lf' % np.mean(cross_val_score(model, train_ss_x, train_labels, cv=10)))

# 使用TPOT自动机器学习工具
X_train,X_test,y_train,y_test = train_test_split(train_features,train_labels,test_size=0.25)
tpot = TPOTClassifier(generations=5,population_size=20,verbosity=2)
tpot.fit(X_train,y_train)
print(tpot.score(X_test,y_test))
tpot.export('tpot_titanic_pipeline.py')
