
from sklearn.datasets import fetch_20newsgroups # 常用的 20 newsgroups 数据集，也就是一个带了标注分好类的英文新闻组的数据集。这个数据集，其实不是最自然的自然语言，里面的数据是经过了预处理的，比如去除了标点符号、停用词等等。我们正好可以拿来看看，面对这样其实不太“自然语言”的数据，OpenAI 的 GPT 系列模型处理的效果怎么样。
import pandas as pd

def twenty_newsgroup_to_csv():
    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))

    # https://www.runoob.com/pandas/pandas-dataframe.html
    df = pd.DataFrame([newsgroups_train.data, newsgroups_train.target.tolist()]).T
    df.columns = ['text', 'target']

    targets = pd.DataFrame( newsgroups_train.target_names, columns=['title'])

    # left_on：左侧DataFrame中用作连接键的列名; right_index：使用右则DataFrame中的行索引做为连接键
    out = pd.merge(df, targets, left_on='target', right_index=True)
    out.to_csv('20_newsgroup.csv', index=False)
    
twenty_newsgroup_to_csv()