
import os,openai,backoff
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")
dynasties= ['唐', '宋', '元', '明', '清', '汉', '魏', '晋', '南北朝']
super_powers = ['隐形', '飞行', '读心术', '瞬间移动', '不死之身', '喷火']
story_types = ['轻松', '努力', '艰难']

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def gpt35(prompt, max_tokens=2048, temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty)
    return response["choices"][0]["text"]


# 我们定义了一系列朝代、超能力和故事的类型。然后通过三重循环，让 AI 根据这三者的组合来生成一系列故事。这些生成出来的故事，也就构成了我们用来微调模型的训练数据。
# 因为数据量不大，我就直接用 CSV 把它存下来了。在这个过程中，数据是一条条生成的，比较慢，也比较消耗 Token
def prepare_stories(dynasties, super_powers, story_types, output_file="data/ultraman_stories.csv"):
    df = pd.DataFrame()
    repeat = 3
    for dynasty in dynasties:
        for super_power in super_powers:
            for story_type in story_types:
                   for i in range(repeat):
                        prompt = f"""请你用中文写一段300字的故事，情节跌宕起伏，讲述一位{dynasty}朝时期的英雄人物，穿越到现代，拥有了{super_power}这样的超能力，通过{story_type}的战斗，帮助奥特曼一起打败了怪兽的故事。"""
                        story = gpt35(prompt)
                        row = {"dynasty": dynasty, "super_power": super_power, "story_type": story_type, "story": story}
                        row = pd.DataFrame([row])
                        df = pd.concat([df, row], axis=0, ignore_index=True)

    df.to_csv("data/ultraman_stories.csv")

# prepare_stories(dynasties, super_powers, story_types)


# 把对应的 CSV 格式的数据转换成微调模型所需要的 JSONL 格式的文件

df = pd.read_csv("data/ultraman_stories.csv")
# 对于微调，我们使用的 Prompt 不再是一个完整的句子，而是只用了“朝代”+“超能力”+“故事类型”拼接在一起的字符串，中间用逗号隔开
df['sub_prompt'] = df['dynasty'] + "," + df['super_power'] + "," + df['story_type']
prepared_data = df.loc[:,['sub_prompt','story']]
prepared_data.rename(columns={'sub_prompt':'prompt', 'story':'completion'}, inplace=True)
prepared_data.to_csv('data/prepared_data.csv', index=False)

import subprocess

'''
通过 subprocess 调用了命令行里的 OpenAI 工具，把上面的 CSV 文件，转化成了一个 JSONL 格式的文件, 内容如下:
{"prompt":"唐,隐形,轻松 ->","completion":" \n\n一位叫做李明的英雄人物，出生在唐朝时期。他是一个勇敢的将军，在他的一生中，他打败了许多敌人，为自己的国家和人民做出了许多贡献。\n\n一天，李明意外被一道神秘的光束穿越到了现代。他发现自己拥有了超能力，可以隐形，可以飞行，可以发射光束，可以放出火焰，可以穿墙而过等等。\n\n李明发现，在现代，怪兽们正在摧毁地球，他决定和奥特曼一起，用自己的超能力，帮助奥特曼消灭怪兽们。\n\n于是，李明和奥特曼开始了一场艰苦的战斗，他们用自己的超能力，一招一式，击退了怪兽们，最终成功地拯救了地球。\n\n在这场战斗之后，地球上的人们都对李明充满了敬佩，他从此成为了一位英雄，他的事迹也被传颂了很久。李明也因此被永远铭记在人们心中，成为了一位不朽的英雄。."}
{"prompt":"唐,隐形,轻松 ->","completion":" \n\n这是一个关于英雄的故事，发生在唐朝时期的中国。一个叫李自成的勇士，他拥有过人的勇气，英勇的行为让他成为当时最受尊敬的人物。\n\n一天，李自成被一道神秘的光芒笼罩住，他突然发现自己似乎穿越时空，来到了现代。他惊讶地发现，自己竟然拥有了一种超能力，可以让自己隐形。\n\n李自成接受了这种超能力，他发现这种能力可以让自己变得更加强大，他决定利用这种能力来帮助人们。\n\n一次，李自成发现有一群怪兽正在破坏城市，他决定和奥特曼一起出动，利用自己的超能力，把怪兽一个个击败，最终成功拯救了城市，令众人欢呼雀跃。\n\n自此，李自成受到了众人的尊敬，他成为了这个城市的英雄，他也把自己的超能力用在了正义的事业上，为人们做出了许多贡献，他也成为了一个英雄。."}

转换后的数据文件，在 Prompt 的最后，多了一个“->”符号。而在 Completion 的开头，多了两个“\n\n”的换行，结尾则是多了一个“.”。
这是为了方便我们后续在使用这个模型生成数据的时候，控制生成结果。未来在使用模型的时候，Prompt 需要以“->\n”这个提示符结束，并且将 stop 设置成“.”。
这样，模型就会自然套用我们微调里的模式来生成文本。
'''
subprocess.run('openai tools fine_tunes.prepare_data --file data/prepared_data.csv --quiet'.split())

# 通过 subprocess 调用 OpenAI 的命令行工具，来提交微调的指令
# 在这个微调的指令里面，我们指定了三个参数，分别是用来训练的数据文件prepared_data_prepared.jsonl、一个基础模型curie，以及生成模型的后缀ultraman。
subprocess.run('openai api fine_tunes.create --training_file data/prepared_data_prepared.jsonl --model curie --suffix "ultraman"'.split())

# 通过下面的 fine_tunes.list 指令，找出所有我们微调的模型
subprocess.run('openai api fine_tunes.list'.split())


# 这个模型的使用方法，和我们使用 text-davinci-003 之类的模型是一样的，只要在 API 里面把对应的 model 字段换掉就好了
openai.api_key = os.getenv("OPENAI_API_KEY")

def write_a_story(prompt):
    response = openai.Completion.create(
        model="curie:ft-bothub-ai:ultraman-2023-04-04-03-03-26",
        prompt=prompt,
        temperature=0.7,
        max_tokens=2000,
        top_p=1,
        stop=["."])
    return response["choices"][0]["text"]

story = write_a_story("宋,发射激光,艰难 ->\n")
print(story)

# 对于模型微调的效果，我们也可以通过一个 OpenAI 提供的命令 fine_tunes.results 来看。对应的，我们需要提供给它一个微调任务的 id。这个 id，可以在 fine_tunes.list 列出的 fine_tunes 模型的 id 参数里找到
subprocess.run('openai api fine_tunes.results -i ft-3oxkr1zBVB4fJWogJDDjQbr0'.split())


# 如果有了新的数据，可以继续进行微调
'''
与上面原有的微调相比，修改了两个参数。
第一个是 model 参数，我们把 Curie 换成了我们刚才微调之后的模型 curie:ft-bothub-ai:ultraman-2023-04-04-03-03-26。
第二个是 learning_rate_multiplier，这个参数的默认值是根据你的样本数量在 0.05 到 0.2 不等。如果你继续微调的样本数要比之前微调的数据量小很多，你就可以调得大一点。
'''
subprocess.run('openai api fine_tunes.create --training_file data/prepared_data_more_prepared.jsonl --model curie:ft-bothub-ai:ultraman-2023-04-04-03-03-26 --suffix "ultraman" --learning_rate_multiplier 0.2'.split())
