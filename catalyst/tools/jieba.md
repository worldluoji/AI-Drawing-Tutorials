# jieba
可以用 Python 的分词库 jieba 库，提取专有名词。

例：根据用户提问的问题，用分词技术提取出产品名
```python
import jieba.posseg as pseg


def extract_english_names(sentence):
    words = pseg.cut(sentence)
    
    # 提取词性为英文的单词
    english_names = [word for word, flag in words if flag == 'eng']
    
    return " ".join(english_names)


# 示例
sentence = "帮我写一个AirPure Pro 智能空气净化器的文案"
english_name = extract_english_names(sentence)
print(f"提取的英文名称: {english_name}")
```
这样一个AI应用的流程如下：
- 提取产品名称。
- 向量查询产品信息。
- 将字段组合为提示词。
- 用提示词访问大模型输出文章。