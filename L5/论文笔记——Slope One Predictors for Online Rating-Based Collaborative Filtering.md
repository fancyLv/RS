# 论文笔记——Slope One Predictors for Online Rating-Based Collaborative Filtering

## Slope One 算法试图同时满足这样的的5个目标
1. 易于实现和维护
2. 运行时可更新的
3. 高效率的查询响应
4. 对初次访问者要求少
5. 合理的准确性

## Slope One
其基本的想法来自于简单的一元线性模型 𝑤=𝑓(𝑣)=𝑣+𝑏。
已知一组训练点
![](https://cdn.nlark.com/yuque/__latex/b6930fc372ee783a24e78141d20243a1.svg#card=math&code=%28v_i%2Cw_i%29_%7Bi%3D1%7D%5En&height=26&width=89)，利用此线性模型最小化预测误差的平方和，我们可以获得
![](https://cdn.nlark.com/yuque/__latex/3ea72bf4ff81b724faf0d1dd4a8286e1.svg#card=math&code=b%3D%5Csum_i%20%5Cfrac%7Bw_i-v_i%7D%7Bn%7D&height=54&width=140)，b为𝑤𝑖和𝑣𝑖差值的平均值。
定义item i 相对于 item j 的平均偏差：![](https://cdn.nlark.com/yuque/__latex/da8d9906b6a5f1959a9991577a8352eb.svg#card=math&code=dev_%7Bj%2Ci%7D%3D%5Csum_%7Bu%5Cin%20S_%7Bj%2Ci%7D%28%5Cchi%29%7D%5Cfrac%7Bu_j-u_i%7D%7Bcard%28S_%7Bj%2Ci%7D%28%5Cchi%29%29%7D&height=63&width=261)
其中 ![](https://cdn.nlark.com/yuque/__latex/55d1ffc902b4ea68fbffbd3a0402e2af.svg#card=math&code=S_%7Bj%2Ci%7D%28%5Cchi%29&height=26&width=58)表示同时对item i 和 j给予了评分的用户集合，而 𝑐𝑎𝑟𝑑(S) 表示集合S包含的元素数量。
可以用 ![](https://cdn.nlark.com/yuque/__latex/1cbaa8c19fa73ef4774e5af74d6e2b1b.svg#card=math&code=dev_%7Bj%2Ci%7D%2Bu_i&height=24&width=91) 获得用户u对 item j的预测值。当把所有这种可能的预测平均起来，可以得到：
![](https://cdn.nlark.com/yuque/__latex/ff1a1c24b0c3a4e3a64c30b63f25c32f.svg#card=math&code=P%28u%29_j%3D%5Cfrac%7B1%7D%7Bcard%28R_j%29%7D%5Csum_%7Bi%5Cin%20R_j%7D%28dev_%7Bj%2Ci%7D%2Bu_i%29&height=61&width=308)
其中![](https://cdn.nlark.com/yuque/__latex/b9bfc05d744cd7d809107cb567db9dd5.svg#card=math&code=R_j&height=24&width=23)表示所有用户u 已经给予评分且满足条件 (![](https://cdn.nlark.com/yuque/__latex/7934733651f3f672baceb5765b0826ac.svg#card=math&code=i%5Cne%20j&height=23&width=42)且![](https://cdn.nlark.com/yuque/__latex/6957d94444cb01a7133bdfd73ce84a16.svg#card=math&code=S_%7Bj%2Ci%7D&height=24&width=29)非空) 的item集合。
对于足够稠密的数据集，我们可以使用近似![](https://cdn.nlark.com/yuque/__latex/6b845f36f2cd87002f8fc5d867415f0f.svg#card=math&code=%5Coverline%7Bu%7D%3D%5Csum_%7Bi%5Cin%20S%28u%29%7D%5Cfrac%7Bu_i%7D%7Bcard%28S%28u%29%29%7D%5Csimeq%5Csum_%7Bi%5Cin%20R_j%7D%5Cfrac%7Bu_i%7D%7Bcard%28R_j%29%7D&height=57&width=341)
把上面的预测公式简化为
![](https://cdn.nlark.com/yuque/__latex/b6d6aa33c830d0e59d974ef5a40ce36c.svg#card=math&code=P%5E%7BS1%7D%28u%29_j%20%3D%20%5Coverline%7Bu%7D%2B%5Cfrac%7B1%7D%7Bcard%28R_j%29%7D%5Csum_%7Bi%5Cin%7BR_j%7D%7Ddev_%7Bj%2Ci%7D&height=61&width=308)

## Weighted Slope One
Slope One中在计算 item i相对于 item j的平均偏差![](https://cdn.nlark.com/yuque/__latex/3885c52099d164800ccca7e76edd148a.svg#card=math&code=dev_%7Bj%2Ci%7D&height=24&width=47)时没有考虑到使用不同的用户数量平均得到的 ![](https://cdn.nlark.com/yuque/__latex/3885c52099d164800ccca7e76edd148a.svg#card=math&code=dev_%7Bj%2Ci%7D&height=24&width=47)，其可信度不同。假设有2000个用户同时评分了 item j和 k，而只有20个用户同时评分了 item j和l，那么显然获得的 ![](https://cdn.nlark.com/yuque/__latex/9b84e2eeca86831213db07ee3ecb95c3.svg#card=math&code=dev_%7Bj%2Ck%7D&height=24&width=49) 比 ![](https://cdn.nlark.com/yuque/__latex/d14c3af7e2112a54e1b8e4828a22b3f7.svg#card=math&code=dev_%7Bj%2Cl%7D&height=24&width=46)更具有说服力。所以一个修正是对最终的平均使用加权：
![](https://cdn.nlark.com/yuque/__latex/a0ffd6e665ba4d36598659d382b81df3.svg#card=math&code=P%5E%7BwS1%7D%28u%29_j%20%3D%20%5Cfrac%7B%5Csum_%7Bi%5Cin%7BS%28u%29-%5C%7Bj%5C%7D%7D%7D%28dev_%7Bj%2Ci%7D%2Bu_i%29c_%7Bj%2Ci%7D%7D%7B%5Csum_%7Bi%5Cin%7BS%28u%29-%5C%7Bj%5C%7D%7D%7Dc_%7Bj%2Ci%7D%7D&height=66&width=348)，其中![](https://cdn.nlark.com/yuque/__latex/e4c7d3f3d9a56859901a41f48a2e45fe.svg#card=math&code=c_%7Bj%2Ci%7D%3Dcard%28S_%7Bj%2Ci%7D%28%5Cchi%29%29&height=26&width=168)

## Bi-Polar Slope One
带权的slope-one算法很好地考虑了共同评分用户数的问题，但还有另外一个问题：好评和差评对用户的决策影响是不同的。很多的好评对用户的影响也不如少数的差评。因此这个算法先会计算用户对一个item的平均评分，然后将用户对item的评分集拆成两个，好评集和差评集：
![](https://cdn.nlark.com/yuque/__latex/7d4bbf04e456cf271efc16e557a6b44e.svg#card=math&code=S%5E%7Blike%7D%28u%29%3D%5C%7Bi%5Cin%7BS%28u%29%7D%7Cu_i%3E%5Coverline%7Bu%7D%5C%7D&height=28&width=253)
![](https://cdn.nlark.com/yuque/__latex/c8cd716f9575fc4e287dac3704787017.svg#card=math&code=S%5E%7Bdislike%7D%28u%29%3D%5C%7Bi%5Cin%7BS%28u%29%7D%7Cu_i%3C%5Coverline%7Bu%7D%5C%7D&height=28&width=272)
类似地，可以定义对item i 和 j 具有相同喜好的用户集合：
![](https://cdn.nlark.com/yuque/__latex/8012aea1d6b655c5b4b9522945c3c2d2.svg#card=math&code=S%5E%7Blike%7D_%7Bi%2Cj%7D%3D%5C%7Bu%5Cin%7B%5Cchi%7D%7Ci%2Cj%5Cin%7BS%5E%7Blike%7D%28u%29%7D%5C%7D&height=32&width=259)
![](https://cdn.nlark.com/yuque/__latex/fca0f00fd0c5f65da962540fd20ec872.svg#card=math&code=S%5E%7Bdislike%7D_%7Bi%2Cj%7D%3D%5C%7Bu%5Cin%7B%5Cchi%7D%7Ci%2Cj%5Cin%7BS%5E%7Bdislike%7D%28u%29%7D%5C%7D&height=32&width=298)
利用上面的定义，我们可以使用下面的公式为（like或dislike的item）获得新的偏差值：
![](https://cdn.nlark.com/yuque/__latex/297b8c879c766fa785c031dc76b88a35.svg#card=math&code=dev_%7Bj%2Ci%7D%5E%7Blike%7D%3D%5Csum_%7Bu%5Cin%7BS%5E%7Blike%7D_%7Bj%2Ci%7D%28%5Cchi%29%7D%7D%5Cfrac%7Bu_j-u_i%7D%7Bcard%28S_%7Bj%2Ci%7D%5E%7Blike%7D%28%5Cchi%29%29%7D&height=69&width=287)
这样可以计算从item i计算得到的预测值：
![](https://cdn.nlark.com/yuque/__latex/ebae6ab7063c71a5afcc6744e4d41a28.svg#card=math&code=p_%7Bj%2Ci%7D%5E%7Blike%7D%3Ddev_%7Bj%2Ci%7D%5E%7Blike%7D%2Bu_i&height=31&width=164) 或者 ![](https://cdn.nlark.com/yuque/__latex/e7865e2d69effeea5f5ddb9b0a26c2f4.svg#card=math&code=p_%7Bj%2Ci%7D%5E%7Bdislike%7D%3Ddev_%7Bj%2Ci%7D%5E%7Bdislike%7D%2Bu_i&height=31&width=203)

最终 Bi-Polar Slope One 的预测公式为
![](https://cdn.nlark.com/yuque/__latex/47eb589afdc3dc701c763e140d8149cb.svg#card=math&code=P%5E%7BbpS1%7D%28u%29_j%3D%5Cfrac%7B%5Csum_%7Bi%5Cin%7BS%5E%7Blike%7D%28u%29-%5C%7Bj%5C%7D%7D%7Dp_%7Bj%2Ci%7D%5E%7Blike%7Dc_%7Bj%2Ci%7D%5E%7Blike%7D%2B%5Csum_%7Bi%5Cin%7BS%5E%7Bdislike%7D%28u%29-%5C%7Bj%5C%7D%7D%7Dp_%7Bj%2Ci%7D%5E%7Bdislike%7Dc_%7Bj%2Ci%7D%5E%7Bdislike%7D%7D%7B%5Csum_%7Bi%5Cin%7BS%5E%7Blike%7D%28u%29-%5C%7Bj%5C%7D%7D%7Dc_%7Bj%2Ci%7D%5E%7Blike%7D%2B%5Csum_%7Bi%5Cin%7BS%5E%7Bdislike%7D%28u%29-%5C%7Bj%5C%7D%7D%7Dc_%7Bj%2Ci%7D%5E%7Bdislike%7D%7D&height=72&width=588)，
其中![](https://cdn.nlark.com/yuque/__latex/027cef81a6f2badedf72699b3a699cd5.svg#card=math&code=c_%7Bj%2Ci%7D%5E%7Blike%7D%3Dcard%28S_%7Bj%2Ci%7D%5E%7Blike%7D%29&height=31&width=156)，![](https://cdn.nlark.com/yuque/__latex/37f95790876af1a46dd7929bbc2181e4.svg#card=math&code=c_%7Bj%2Ci%7D%5E%7Bdislike%7D%3Dcard%28S_%7Bj%2Ci%7D%5E%7Bdislike%7D%29&height=31&width=196)
