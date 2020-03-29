# Thinking
## 1. 排序模型按照样本生成方法和损失函数的不同，可以划分成Pointwise，Pairwise, Listwise三类方法，这三类排序方法有何区别
Pointwise，针对单一文档，每个文档为单独训练数据，输出为文档与 Query 的标签类别或相关性分数  
Pairwise，关注文档的顺序关系，输入为特定的 Query，文档对 <Doc1, Doc2>，输出为文档对偏向得分，{-1, 1}  
Listwise，将一次Query对应的所有搜索结果列表作为一个训练样例，输入为特定的Query，文档集合，输出为所有文档的打分或者排列顺序


## 2. 排序模型按照结构划分，可以分为线性排序模型、树模型、深度学习模型，这些模型都有哪些典型的代表？
线性模型典型代表是LR，引入自动二阶交叉特征的FM和FFM，  
非线性树模型GBDT和GBDT+LR  
深度学习模型代表有Wide & Deep, DeepFM, NFM等


## 3. NDCG如何计算
CG即累计增益，将每个推荐结果相关性的分值累加后作为整个推荐列表的得分。$$CG_p=\sum_{i=1}^prel_i$$  
CG只考虑到了相关性的关联程度，没有考虑到位置的因素。所以在CG的基础上引入位置影响因素，即DCG，$$DCG_p=\sum_{i=1}^p\frac{rel_i}{log_2(i+1)}$$  
由于搜索结果随着检索词的不同，返回的数量是不一致的，而DCG是一个累加的值，没法针对两个不同的搜索结果进行比较，因此需要归一化处理，$$NDCG_p=\frac{DCG_p}{IDCG_p}$$，  
IDCG为理想情况下最大的DCG值，首先要拿到搜索的结果，人工对这些结果进行排序，排到最好的状态后，算出这个排列下本query的DCG，就是IDCG。


## 4. 搜索排序和推荐系统的相同和不同之处有哪些
相同之处：都需要推荐和排序  
不同之处：
搜索排序是一个非常主动的行为，并且用户的需求十分明确，推荐是有意识的被动推荐，基于某Query进行的结果排序，期望用户选中的在排序结果中是靠前的；  
推荐系统中用户接受信息是被动的，需求也都是模糊而不明确的，推荐是发散的、无意识的主动推荐，排序准确性不一定是最重要的


## 5. Listwise排序模型能否应用到推荐系统中
listwise可以应用到推荐系统中，listwise将一个查询对应的所有搜索结果列表作为一个训练样本，相对于尝试学习每一个样本是否相关或者两个文档的相对比较关系，listwise的基本思路是尝试直接优化像NDCG（Normalized Discounted Cumulative Gain）这样的指标，从而能够学习到最佳排序结果。但是计算量大复杂度较高

# Action
## 3. 如果你是某P2P租车的技术负责人，你会如何设计个性化推荐和搜索排序
   阐述相似车型，搜索排序的设计方法  
   可能的embedding策略  

p2p租车双边的短租平台（顾客，房东），可以借鉴Airbnb个性化推荐以及搜索排序。  
针对搜索排序，相似车型推荐进行的实时个性化，基于业务需求，考虑搜索的目标。  
对于query（带有位置和用车时间），同时为host和guest优化搜索结果：  
顾客角度：需要根据位置，价格，类型，评论等因素排序来获得客户喜欢的listing。  
车主角度：需要过滤掉那些有坏的评论，宠物，停留时间，人数，等其他因素而拒绝guest的listing，将这些listing排列的低一点。  
采用Learnig
to rank来做，将问题转换为pairwise
regression问题，将预定的listing作为正样本，拒绝的作为负样本。  
车源embedding，把每个用户连续点击过的车源Session看做一个句子，每个车源当做word，训练出车源的embedding。  
使用skip-gram构造基础的目标函数，采用negative sampling构造采样之后的目标函数，根据预定行为构造有导向与“booking”的目标函数，在book基础上增加同一地区的neg（适配聚集搜索）  
冷启动，在和新上传房源具有相同类型和相同价格区间的房源中，找到3个地理位置最接近的房源，求embedding平均。  
在更粗的粒度上（User Type Embedding 和 Listing Type Embedding）上进行长期兴趣学习，  
考虑双边市场的特点，通过加入“booking”、“host rejection”强反馈信号来指导无监督学习。  
基于Embedding的搜索排序：  
算法：GBDT模型（支持lambda rank）解决pairwise问题  
特征：listing　features、user　features、query　features和cross　features，和embedding
features








