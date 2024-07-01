# Diffusers
## text-2-image
```
pip install diffusers accelerate transformers
```
## 文生图
```
from diffusers import DiffusionPipeline
pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipeline.to("cuda")
image = pipeline("a photograph of an astronaut riding a horse").images[0]
image
```
使用了 Huggingface 的 Diffusers 库，通过 DiffusionPipeline 加载了 RunwayML 的 stable-diffusion-v1-5 的模型。然后，指定了这个 Pipeline 使用 CUDA 也就是利用 GPU 来进行计算。最后向这个 Pipeline 输入了一段文本，通过这段文本我们就生成了一张图片。


## 图生图
```
import torch
from PIL import Image
from io import BytesIO

from diffusers import StableDiffusionImg2ImgPipeline

device = "cuda"
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe = pipe.to(device)

image_file = "./data/sketch-mountains-input.jpg"

init_image = Image.open(image_file).convert("RGB")
init_image = init_image.resize((768, 512))

prompt = "A fantasy landscape, trending on artstation"

images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images

display(init_image)
display(images[0])
```
把 Pipeline 换成了 StableDiffusionImg2ImgPipeline，此外除了输入一段文本之外，我们还提供了一张草稿图。然后，你可以看到对应生成的图片的轮廓，就类似于我们提供的草稿图。而图片的内容风格，则是按照我们文本提示语的内容生成的。

与文圣图唯一的一个区别是，我们其实不是从一个完全随机的噪声开始的，而是把对应的草稿图，通过 VAE 的编码器，变成图像生成信息，又在上面加了随机的噪声。所以，去除噪音的过程中，对应的草稿图的轮廓就会逐步出现了。

## 提升图片的分辨率
通过 Stable Diffusion 来提升图片的分辨率，只不过需要一个单独的模型。这个模型就是专门在一个高低分辨率的图片组合上训练出来的。
```
from diffusers import StableDiffusionUpscalePipeline

# load model and scheduler
model_id = "stabilityai/stable-diffusion-x4-upscaler"
pipeline = StableDiffusionUpscalePipeline.from_pretrained(
    model_id, revision="fp16", torch_dtype=torch.float16
)
pipeline = pipeline.to("cuda")

# let's download an  image
low_res_img_file = "./data/low_res_cat.png"
low_res_img = Image.open(low_res_img_file).convert("RGB")
low_res_img = low_res_img.resize((128, 128))

prompt = "a white cat"

upscaled_image = pipeline(prompt=prompt, image=low_res_img).images[0]

low_res_img_resized = low_res_img.resize((512, 512))

display(low_res_img_resized)
display(upscaled_image)
```