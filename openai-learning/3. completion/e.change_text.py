
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

prefix = """在这个快节奏的现代社会中，我们每个人都面临着各种各样的挑战和困难。
在这些挑战和困难中，有些是由外部因素引起的，例如经济萧条、全球变暖和自然灾害等。\n"""
# 试试去掉 Suffix 一开始的换行符号
suffix = """\n面对这些挑战和困难，我们需要采取积极的态度和行动来克服它们。
这意味着我们必须具备坚韧不拔的意志和创造性思维，以及寻求外部支持的能力。
只有这样，我们才能真正地实现自己的潜力并取得成功。"""

def insert_text(prefix, suffix):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prefix,
        suffix=suffix,
        max_tokens=1024,
        )
    return response

response = insert_text(prefix, suffix)
print(response["choices"][0]["text"])

'''
实际会根据prefix和suffix给出一段话，介于prefix和suffix之间,比如：
另一些是内部因素，例如事业难以发展、无法解决的个人和家庭矛盾等。
'''
