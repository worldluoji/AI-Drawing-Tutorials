# prompt basic

最简单的prompt, 仅进行文字描述，示例如下：

<img src="./images/simple prompt structure.png" />

进阶的prompt如下：

<img src="./images/advanced prompt.png" />

The prompt is divided into three parts. The first part is the Image, which is optional and can be included or excluded.

Let's talk about what the Image URL is used for. There are many ways to use it, such as merging two images into one.

Please note:
- You input the URL address of the image, and it must be a publicly accessible URL.
- The supported image formats are png, gif, and jpg.
- You can include the URLs of up to two images, or one image URL + a piece of text.

if you don't want to upload the images to image hosting servers, you can also use Discord's image hosting service. You can privately message Midjourney Bot and upload the image to Discord first. Then, right-click on the image and copy the image link.

<br>

## common parameters
In simple terms, you can think of these parameters as official fixed prompt templates, which include special characters **that ensure 100% consistency** of the output results of the model and improve the accuracy and efficiency of the prompt.

以下是MidJourney常用参数的总结表格，包括参数名称、简写、功能描述及注意事项：

| 参数名称         | 简写  | 功能描述                                                                                          | 注意事项                                                     |
|-----------------|------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| 微调细节参数     | --chaos/-c | 影响生成结果的变化程度。数值范围：0-100，默认值为0。数值越高，生成结果的多样性和不可预测性越大。       | 数值越低，生成图像风格和构图越稳定。                         |
| 提示词权重参数   | ::   | 用于分隔和指定提示词中不同部分的重要性权重。                                                       | 可以平衡或强调不同概念在生成图像中的体现。                   |
| 图片权重参数     | --iw  | 控制上传垫图与提示词之间的比重。                                                                   | 数值调整垫图影响程度。                                       |
| 负向权重参数     | --no  | 指定不想在生成图像中出现的元素。                                                                     | 可以指定多个元素，用逗号分隔。                               |
| 风格化权重参数   | --stylize  | 使生成图像更具有艺术性、特定风格或形式。                                                         | 较低的值会使生成图像更贴近提示词的描述，而较高的值则会增加艺术元素，但可能会降低与提示词的关联度。                                                             |
| 风格参数         | -style  | 在特定版本模型下切换不同的生成风格。如`-style raw`减少默认审美影响，更适合高级摄影图像。         | 版本间有差异，如MG 5.1支持`-style raw`，Niji模型有独特风格选项。 |
| 宽高比参数       | --aspect/--ar | 更改生成图像的宽高比，格式为冒号分隔的两个整数，如7:4。默认为1:1。                                   | 数值必须为整数，长宽比可能因放大而有微小变化。               |
| 模型版本参数     | --v/--version | 切换不同的Midjourney模型版本，如V5。不同版本擅长领域不同。                                           | 不是版本越大越好，需根据需求选择。                           |
| 动漫风格参数     | --niji  | 针对动漫和二次元风格优化的模型。                                                                   | 适用于动漫主题创作。                                         |

--ar宽高比说明:
- 5:4 is commonly used for traditional printing
- 3:2 is often used for photo printing
- 7:4 is a ratio similar to HD TV or smartphone screens

<br>

## --seed
在Midjourney图像生成中，`--seed` 参数扮演了一个关键角色，用于控制生成图像的随机性并确保结果的可复现性。具体来说，它的作用包括：

1. **初始化随机性**：`--seed` 是一个整数值，用于设定生成图像时所用随机数生成器的起点。这个值影响图像生成过程中的初始噪声图案，类似于电视屏幕上的静态噪声，是生成图像的基础。

2. **生成相似图像**：当你提供一个具体的 `--seed` 值，Midjourney 将利用这个值来确定图像生成的起点，从而使得使用相同文本提示（prompt）、模型版本以及其他设置的情况下，能够生成具有相似构图、颜色和细节的图像。这对于创造一系列风格或主题一致的图像特别有用。

3. **可复现性**：如果想要在未来重现完全相同的生成结果，记录下之前使用的 `seed` 值至关重要。这使得艺术家或创作者能够在不同的时间点回到相同的创意起点，无论是为了继续编辑还是分享特定的视觉效果。

4. **范围与限制**：`--seed` 接受的整数范围通常是 0 到 4294967295。不同模型版本对 `seed` 的响应可能有所不同，例如，模型版本1、2、3、test和testp通常会生成相似但不完全相同的图像，而版本4、5和niji可能会因为seed相同而产生几乎完全相同的图像。

5. **未指定时的随机性**：如果不指定 `--seed`，Midjourney 会自动分配一个随机种子，导致每次生成的图像都不同，增加了结果的多样性。

综上所述，通过精细调整 `--seed` 参数，用户可以在探索创意空间的同时，保持对生成内容一定程度的控制和可复现性。

<br>

## reference
https://learningprompt.wiki/docs/midjourney/mj-tutorial-basics/midjourney-common-parameters