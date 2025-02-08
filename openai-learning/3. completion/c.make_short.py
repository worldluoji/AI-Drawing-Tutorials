import openai
import tiktoken
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

# 使用 Tiktoken 库，把我们不希望出现的“灾害”这个词儿，找到它对应的 Token，然后给它们都赋了一个 -100 的 bias。-100表示不出现，100表示一定出现。一般情况下，设置在 1 到 -1 之间就足够了。设置成 100，你一定要某些字出现，那么整个生成会慢到无法忍受。
encoding = tiktoken.get_encoding('p50k_base')
token_ids = encoding.encode("灾害")
# 虽然灾害只有两个中文汉字，但是我们通过 Tiktoken 去处理的时候，我们打印了对应的 Token 的 id 是什么，实际上有 5 个 Token。这里其实和我们之前看到的英文一样，并不是一个字或者一个单词是一个 Token。事实上，同样含义的中文，目前消耗的 Token 数量是比英文多的。
print(token_ids)

bias_map = {}
for token_id in token_ids:
    bias_map[token_id] = -100

def make_text_short(text):
    messages = []
    messages.append( {"role": "system", "content": "你是一个用来将文本改写得短的AI助手，用户输入一段文本，你给出一段意思相同，但是短小精悍的结果"})
    messages.append( {"role": "user", "content": text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=2048,
        presence_penalty=0, # 如果一个 Token 在前面的内容已经出现过了，那么在后面生成的时候给它的概率一定的惩罚。这样，AI 就会倾向于聊新的话题和内容。在这里，我们把它设置成了默认值 0。
        frequency_penalty=2, # 对于重复出现的 Token 进行概率惩罚。这样，AI 就会尽量使用不同的表述。在这里我们设成了最大的 2，你也可以设置成最小的 -2。但是那样的话，它就更容易说重复的话。
        n=3, # 让 AI 给我们返回 3 个答案供我们选择
        logit_bias = bias_map,
    )
    return response

long_text = """
根据最近的报告，中国的消费者价格指数（CPI）同比增长0.7％，低于2月份1％的增长。
与此同时，上个月生产者价格指数（PPI）同比下降2.5％，低于去年同期下降1.4％。
这表明中国的经济目前正在经历生产者价格的通缩和消费者价格通胀放缓。
在这个快节奏的现代社会中，我们每个人都面临着各种各样的挑战和困难。
在这些挑战和困难中，有些是由外部因素引起的，例如经济萧条、全球变暖和自然灾害等。
还有一些是由内部因素引起的，例如情感问题、健康问题和自我怀疑等。
面对这些挑战和困难，我们需要采取积极的态度和行动来克服它们。
这意味着我们必须具备坚韧不拔的意志和创造性思维，以及寻求外部支持的能力。
"""
short_version = make_text_short(long_text)

index = 1
for choice in short_version["choices"]:
    print(f"version {index}: " + choice["message"]["content"])
    index += 1