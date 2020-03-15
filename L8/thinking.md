# Thinking
## 1 在CTR点击率预估中，使用GBDT+LR的原理是什么?
    通过GBDT将特征进行组合，然后传入给线性分类器  
    LR对GBDT产生的输入数据进行分类

## 2 Wide & Deep的模型结构是怎样的，为什么能通过具备记忆和泛化能力（memorization and generalization）
    Wide&Deep模型混合了一个线性模型（Wide part）和Deep模型(Deep part)。  
    Wide部分是广义线性模型,wide模型可以通过利用交叉特征引入非线性高效的实现记忆能力，达到准确推荐的目的。wide模型通过加入一些宽泛类特征实现一定的泛化能力。但是受限与训练数据，wide模型无法实现训练数据中未曾出现过的泛化。  
    Deep部分就是个前馈网络模型，特征首先转换为低维稠密向量，再将其作为第一个隐藏层的输入，根据最终的loss来反向训练更新。

## 3 在CTR预估中，使用FM与DNN结合的方式，有哪些结合的方式，代表模型有哪些？
    FM和DNN的组合方式有串行和并行
    并行的代表模型DeepFM，串行代表模型NFM
    
## 4 Surprise工具中的baseline算法原理是怎样的？BaselineOnly和KNNBaseline有什么区别？
    Baseline算法基于统计的基准预测线打分，$$b_{ui}=\mu+b_u+b_i$$
    包括三部分的偏置因素：训练集中所有评分记录的全局平均数μ，用户偏置bi表示某一特定用户的打分习惯，物品偏置bj表示某一特定物品得到的打分情况。
    BaselineOnly基于统计的基准预测线打分
    KNNBaseline 是协同过滤算法的变种,考虑每个用户评分的基线
    
## 5 GBDT和随机森林都是基于树的算法，它们有什么区别？
    随机森林是bagging的一种扩展,gbdt是一种boosting算法
    组成随机森林的树可以是分类树，也可以是回归树；而GBDT只由回归树组成
    组成随机森林的树可以并行生成；而GBDT只能是串行生成
    对于最终的输出结果而言，随机森林采用多数投票等；而GBDT则是将所有结果累加起来，或者加权累加起来
    随机森林对异常值不敏感，GBDT对异常值非常敏感
    随机森林对训练集一视同仁，GBDT是基于权值的弱分类器的集成
    随机森林是通过减少模型方差提高性能，GBDT是通过减少模型偏差提高性能
    
## 6 基于邻域的协同过滤都有哪些算法，请简述原理
    基于邻域的协同过滤都有基于用户的协同过滤（UserCF）和基于物品的协同过滤（ItemCF）
    UserCF：给用户推荐和他兴趣相似的其他用户喜欢的物品，把和用户兴趣相同的k个邻居，喜欢的物品进行汇总，去掉用户u已经喜欢过的物品，剩下按照从大到小进行推荐
    ItemCF：给用户推荐和他之前喜欢的物品相似的物品，和用户历史上感兴趣的物品越相似的物品，越有可能在用户的推荐列表中获得比较高的排名预测用户u对物品的兴趣度，去掉用户u已经喜欢过的物品，剩下按照从大到小进行推荐