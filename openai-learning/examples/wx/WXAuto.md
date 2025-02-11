# WXAuto
支持微信 RPA 的Python 库。这个 Python 库支持所有的微信代理操作，比如搜索群名搜索、读取群列表、读取群消息列表、模拟按键操作等。

搭建 AI 微信机器人的实现思路：当程序接收到新的 @AI 广告的消息内容后，AI 广告机器人程序调用 GPT 的接口获得回复，最后调用 RPA 把内容回复到群里并 @用户。

一次 GPT 操作就是一个标准的 GPT 大模型接口调用:
```python
import os
import requests


def get_chatgpt_response(prompt: str) -> str:
    api_key = os.getenv('OPENAI_API_KEY')  # 从环境变量中获取 API 密钥
    url = 'https://api.openai.com/v1/completions'  # OpenAI API 的端点
    headers = {
        'Authorization': f'Bearer {api_key}',  # 设置授权头
        'Content-Type': 'application/json'  # 设置内容类型
    }
    data = {
        'model': 'gpt-3.5-turbo-instruct',  # 使用 gpt-3.5-turbo-instruct 模型
        'prompt': prompt,  # 提供给模型的提示
        'max_tokens': 1500,  # 设置生成的最大 tokens 数
        'temperature': 0.7,  # 控制输出的随机性
        'n': 1,  # 返回一个结果
        'stop': None  # 可以设置停止标志
    }
    response = requests.post(url, headers=headers, json=data)  # 发送 POST 请求
    result = response.json()  # 获取 JSON 响应
    return result['choices'][0]['text'].strip()  # 提取并返回生成的文本


# 示例对话
prompt = """
请你写一则广告，主题是推广一款新的AI软件 
"""


# 调用函数
response = get_chatgpt_response(prompt)
print(response)  # 打印响应
```
这里注意，如果是单次操作这段代码并没有问题，但是要支持用户带历史消息的会话功能，则需要保存历史会话内容，并且每次的 prompt 提示词都要带上整个历史消息。


## 难点
### 定时轮询群消息优化
由于 RPA 的基本原理是模拟界面操作，根据之前的流程，为了尽快的处理消息，即使群里完全没有新消息，RPA 也要定时轮询群消息。但是，一旦群的数量增加，这种轮询的效率会越来越低。这时候，如何高效轮询，如何减少轮询的次数，就成为了最关键的问题。

为了减少不必要的搜索和群界面操作，可以利用微信消息列表的一个特点：当某个群有新消息的时候，这个群会出现在消息列表的顶部。所以，我们只需要读取消息列表，从上到下检查消息列表，直到遇到没有新消息的群则停止。

更进一步，将所有 AI 相关的群做了置顶操作，这样只需要读取最新的、有消息的 AI 群就可以了。如果轮询时段内没有消息，则只要读第一个群就停止了，如果有消息则正好读完有消息的群就停止，做到了性能和效率最大化。

### 消息可靠性问题
通过 RPA 读取群消息列表完成了消息读取。其中最大的问题就是微信消息列表不提供消息 ID 和时间戳，这让从消息列表里分解出最新消息变得非常困难。

如果存储和比对整个消息列表，那对计算量和数据的要求都会过高。注意到微信消息列表中一段时间的消息会有一个总的时间戳，它本身也是一条消息，我们利用了这个时间戳消息，存储消息列表里最新时间戳之后的消息，并逐个比对，这样就得到了可靠的最新消息。

### 微信 RPA 稳定性问题
基于 RPA 的微信操作需要定期登录，这对运营来说是一定的挑战。我们的微信 AI 一直是企业内部试用和测试，所以问题不大。如果正式对外，应该用微信官方推荐的企业微信的接口。

## 降本
- GPT价格过高，可以换为DeepSeek
- 私有化部署DeepSeek