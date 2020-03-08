## Thinking1 在实际工作中，FM和MF哪个应用的更多，为什么
FM应用的更多，矩阵分解MF是FM的特例，即特征只有User ID 和Item ID的FM模型  
矩阵分解MF只适用于评分预测，进行简单的特征计算，无法利用其他特征  
FM引入了更多辅助信息（Side information）作为特征  
## Thinking2 FFM与FM有哪些区别？
FM和MF的区别：
FM矩阵将User和Item都进行了one-hot编码作为特征，使得特征维度非常巨大且稀疏  
矩阵分解MF是FM的特例，即特征只有User ID 和Item ID的FM模型  
矩阵分解MF只适用于评分预测，进行简单的特征计算，无法利用其他特征  
FM引入了更多辅助信息（Side information）作为特征  
FM在计算二阶特征组合系数的时候，使用了MF  
## Thinking3 DeepFM相比于FM解决了哪些问题，原理是怎样的
FM可以做特征组合，但是计算量大，一般只考虑2阶特征组合  
DeepFM=FM+DNN，既考虑低阶（1阶+2阶），又能考虑到高阶特征  
大概流程：
首先利用FM进行embedding得到Dense Embeddings的输出。将Dense Embeddings的结果作为FM模块和DNN模块的输入。通过一定方式组合后，模型FM模块的输出完全模拟出了FM的效果，而DNN模块则学到了比FM模块更加高阶的特征交叉。最后将DNN和FM的结果组合后激活输出。
## Thinking4 假设一个小说网站，有N部小说，每部小说都有摘要描述。如何针对该网站制定基于内容的推荐系统，即用户看了某部小说后，推荐其他相关的小说。原理和步骤是怎样的
1. 对每部小说的摘要描述进行特征提取.   
	N-Gram，提取N个连续字的集合，作为特征  
	TF-IDF，按照(min_df, max_df)提取关键词，并生成TFIDF矩阵  
2. 计算小说之间的相似度矩阵 余弦相似度  
3. 对于指定的小说，选择相似度最大的Top-K部小说进行输出.  
 
## Thinking5 Word2Vec的应用场景有哪些
Word2Vec的2种模式，CBOW根据已知上下文词预测中心词，Skip-gram根据已知中心词预测上下文词。  
word2vec可以应用于文本相似度，文本分类，命名实体识别和情感分析。  
在社交网络中的推荐中，给当前用户推荐 他/她 可能关注的大V  
在商品推荐的场景中，竞品推荐和搭配推荐  
