# 让AI讲话
## 1. 使用云语音合成
- [科大讯飞](https://www.xfyun.cn/services/online_tts)
- [阿里云](https://ai.aliyun.com/nls/tts)
- [百度](https://ai.baidu.com/tech/speech/tts)

## 2. 使用开源模型进行语音合成
百度开源的 [PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech/blob/develop/demos/text_to_speech/README_cn.md) 支持语音合成功能
```
pip install paddlepaddle
pip install paddlespeech
```
然后通过 PaddleSpeech 自带的 TTSExecutor，可以将对应的文本内容转换成 WAV 文件。需要注意，这个过程中，PaddleSpeech 需要下载对应的模型，所以第一次运行的时候也要花费一定的时间。
```
from paddlespeech.cli.tts.infer import TTSExecutor

tts_executor = TTSExecutor()

text = "今天天气十分不错，百度也能做语音合成。"
output_file = "./data/paddlespeech.wav"
tts_executor(text=text, output=output_file)
```

PaddleSpeech 的 TTSExecutor，只是把你的文本输入转化成了一个 WAV 文件。要在 Python 里面播放对应的声音，我们还要借助于 PyAudio 这个包。对应的，我们要先安装 PyAudio 依赖的 portaudio 库，然后再安装 PyAudio 包。
```
// MAC
brew install portaudio

// Ubuntu
sudo apt-get install portaudio19-dev
```
只有在 portaudio 安装成功之后，我们才能安装 PyAudio 包，不然会报缺少依赖的错误:
```
pip install pyaudio
```
通过 PyAudio，我们可以直接播放 WAV 文件的内容了:
```
import wave
import pyaudio

def play_wav_audio(wav_file):
    # open the wave file
    wf = wave.open(wav_file, 'rb')

    # instantiate PyAudio
    p = pyaudio.PyAudio()

    # open a stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data from the wave file and play it
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

play_wav_audio(output_file)
```
PaddleSpeech 默认情况下使用的是一个只支持中文的模型。我们可以通过一些参数来指定使用的模型，一样能够做中英文混合的语音合成。
```
tts_executor = TTSExecutor()

text = "早上好, how are you? 百度Paddle Speech一样能做中英文混合的语音合成。"
output_file = "./data/paddlespeech_mix.wav"
tts_executor(text=text, output=output_file, 
             am="fastspeech2_mix", voc="hifigan_csmsc", 
             lang="mix", spk_id=174)

play_wav_audio(output_file)
```
- am，是 acoustic model 的缩写，也就是我们使用的声学模型。我们这里选用的是 fastspeech2_mix。fastspeech2 也是一个基于 Transformer 的语音合成模型，速度快、质量高。这里带了一个 mix，代表这个模型是支持中英文混合生成的。
- voc，是 vocoder 的缩写，叫做音码器。声学模型只是把我们的文本变成了一个声音波形的信号。我们还需要通过音码器，把声学模型给出的波形变成可以播放的音频。我们这里选择的 HiFiGAN_csMSC，是一个高保真（HiFi）、基于对抗生成网络（GAN）技术的模型，它的训练数据用到了 HiFiSinger 和 csMSC，而模型的名字就来自这些关键词的组合。
- lang，代表我们模型支持的语言，这里我们自然应该选 mix。
- spk_id，不同的 spk_id 听起来就是不同的人说的话。