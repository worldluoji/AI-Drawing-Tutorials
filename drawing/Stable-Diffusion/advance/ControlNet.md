# ControlNet
AI 绘画生成的图像在手部和脸部细节存在瑕疵有哪些解决方式？ControlNet 就可以解决这个问题，对图像结构做出一定的限制，比如手部的关键点信息、五官信息等。

最初的 ControlNet 主要用于线稿上色、图像风格化、可控姿态的人体生成等任务。如今各路网友脑洞大开，使用 ControlNet 做出了创意二维码、将文字自然地融入照片等趣味效果。

## 初识 ControlNet
prompt 是对于 AI 绘画模型指令级的控制，ControlNet 无疑是构图级的控制。

我们可以通过图像边缘提取算法获取图像轮廓。把这个轮廓图作为 ControlNet 的输入，同时使用这样一句 prompt “a high-quality, detailed, and professional image”生成图片，便可以得到右侧的四张图片。

<img src="../images/Control Net example1.webp" />

这里有两个要点值得我们关注：
- 第一，我们的 prompt 中并不包括任何描述图像内容的信息，便可以得到四张不同鹿的照片。
- 第二，生成的四张照片都满足我们输入的轮廓限制，并且效果各异。


再比如，我们随手画一个草图，比如简单几笔勾勒出乌龟、奶牛和热气球，同样是配合上我们随手写出的 prompt，便可以生成精美的图片。

<img src="../images/Control Net example2.webp" />


ControlNet 可用的控制条件还远不止这些。比如后面这些图，展示的就是使用 HED 边缘、人体姿态点、图像分割结果作为控制条件，配合上各种不同 prompt 生成的图像效果。

<img src="../images/Control Net example4.webp" />

<img src="../images/Control Net example3.webp" />


## ControlNet 原理
ControlNet 要和 SD 结合起来使用，所以我们先回顾下 SD 模型（为了描述方便，我们接下来都用 SD 来指代 Stable Diffusion）的图像生成过程。VAE 编码器输出的潜在表示，经过一个 UNet 模型结构便可以完成当前时间步 t 的噪声预测。对于 SD1.x 系列，输入的潜在表示和预测得到的噪声都是一个 64x64x4 的向量。

ControlNet 并没有改变 SD 模型的 VAE、CLIP 文本编码器和 UNet 结构，而是在这个方案的基础上多加了一些东西。

<img src="../images/ControlNet Princical.png" />

红框中 SD 模型部分展示的是我们熟悉的 UNet 结构，我们能看到，这里的 UNet 由 12 个编码器模块、1 个中间模块和 12 个解码器模块构成。Prompt 的文本表征和时间步 t 的编码都直接作用于这些模块。

为了能够对齐控制信号和 SD 特征之间的维度，**ControlNet 部分直接拷贝了 UNet 的 12 个编码器模块和中间模块的权重，并加入了 14 个名为零卷积（zero convolution）的层**。需要注意的是，prompt 的文本表征和时间步 t 的编码同样作用于 ControlNet 部分的 UNet 编码模块。

我们再来看第二个问题，ControlNet 的控制条件该如何输入。我们知道，SD 模型 UNet 部分的输入是潜在表示，而 **ControlNet 的输入是我们使用的控制条件**，比如图像轮廓、手绘线稿等。
潜在表示是经过 VAE 编码器处理后的特征，分辨率是 64x64x4。而 ControlNet 的输入，比如我们提供的目标轮廓线，通常是 512x512 这样的图像。这样 ControlNet 的控制信号和 SD 模型就不一致了，因此我们需要使用一个小型深度学习网络，将 512x512 维度的控制条件转换为 64x64 维度的特征。

我们再来看第三个问题，处理 ControlNet 和 SD 模型之间的信息交互。仔细观察 ControlNet 的方案图你会发现，ControlNet 输入的特征经过一层零卷积层计算后，就会与 SD 模型输入的潜在表示相加。这样，SD 模型便将潜在表示传递给了 ControlNet 模块。而 ControlNet 后面 13 个零卷积层的输出特征，直接和 SD 模型 UNet 部分对应的特征相加，这么做是为了将控制条件引入到 SD 模型。

所谓零卷积，就是初始化权重为零的卷积算子。
之所以要将权重初始化为零，是为了在 ControlNet 训练的第一步，无论控制条件是什么，经过全零卷积后得到的数值都为零。这样，ControlNet 后面 13 个零卷积层的输出特征也全为零，和 SD 模型 UNet 部分对应的特征相加便没有任何效果。

因为原始的 SD 模型已经在海量数据上充分训练过了，ControlNet 使用零卷积在一开始不会对 SD 产生任何影响，这样一来，引入新的 ControlNet 权重仍可以最大程度保留 SD 模型的 AI 绘画能力。

## 训练 ControlNet
训练过程可以分为两步。
- 第一，根据你要使用的控制方法，在你的数据集上生成这些控制条件，比如提取图像边缘轮廓或者提取人体姿态点。
- 第二，按照标准的 SD 模型训练流程进行训练，UNet 的输入包括带噪声的潜在表示、时间步 t 的编码、prompt 文本表征和 ControlNet 的控制信号。

与常规 SD 模型的训练不同，UNet 的输入多了一个 ControlNet 的控制信号。值得一提的是，标准 SD 训练过程中使用无分类器引导，一般有 10% 的概率会将训练的 prompt 设置为空字符串。而 ControlNet 的训练中，这个概率是 50%！

这是为了让 SD 模型在预测噪声时，有更多信号源自 ControlNet 的控制信号，而不是 prompt 文本表征。说到底，还是为了**加强控制**。

## ControlNet 的持续进化
指令级修图首先是指令级修图的 ControlNet。比如后面这张风景图片，我们希望转换图片里的季节，就可以通过 prompt 写下“make it winter”。图中的五个冬季效果是使用不同随机种子得到的。

<img src="../images/ControlNet xt.webp" />

再比如后面这个例子，原始照片是一张人像照，我们可以利用 prompt 把绿衬衫的男人换成钢铁侠。可以看到，ControlNet 保持了原始人像轮廓，生成了钢铁侠的效果。

<img src="../images/ControlNet xt2.webp" />

有了这个功能，我们不用复杂的 PS，写个 prompt 就能修图。[背后原理](https://github.com/lllyasviel/ControlNet-v1-1-nightly/tree/main#controlnet-11-instruct-pix2pix)其实也并不复杂，只不过在训练 ControlNet 的时候使用了特殊的成对数据，我们看个例子就明白了。

<img src="../images/ControlNet pair.webp" />

图片中的文本就是训练 ControlNet 用的 prompt，原始图像作为 ControlNet 的输入条件，而指令修图后的图像作为 SD 模型的目标输出。


## Tile 功能
Tile 在中文里是瓷砖的意思，字面理解是将图片切分成棋盘格的样式分别处理再拼接。这个功能很强大，因为它可以帮我们补充图像中的细节。

比如后面这张图，输入图像是一张 64x64 分辨率的小狗，使用 Tile 功能配合上“dog on grassland”这个 prompt，可以轻松实现图像的 8 倍超分，得到 512x512 分辨率的效果。

<img src="../images/ControlNet tiles.webp" />