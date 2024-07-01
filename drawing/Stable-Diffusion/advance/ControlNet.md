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