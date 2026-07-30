# -*- coding: utf-8 -*-
"""Open-weights pilot, candidate B: SDXL + ControlNet-Union (all ungated,
commercially clean). Canny edges preserve the composition; an img2img pass
with the style prompt lays the pen-and-wash look. ~10GB VRAM, seconds/image.

Reads /workspace/orig/*-orig.png -> /workspace/out/{name}-sdxl.png
"""
import glob
import os
import time

import cv2
import numpy as np
import torch
from diffusers import (ControlNetModel,
                       StableDiffusionXLControlNetImg2ImgPipeline)
from PIL import Image

ORIG, OUT = "/workspace/orig", "/workspace/out"
os.makedirs(OUT, exist_ok=True)

PROMPT = ("refined pen-and-ink study with a first thin watercolour wash, clean confident linework, "
          "muted colours of the original scene, mostly warm uncoloured cream paper showing through, "
          "traditional book illustration, elegant, unfinished sketch coming into focus")
NEG = ("photograph, photorealistic, 3d render, digital painting, oversaturated, dark, "
       "text, words, letters, watermark, signature, frame, border")

controlnet = ControlNetModel.from_pretrained(
    "xinsir/controlnet-union-sdxl-1.0", torch_dtype=torch.float16)
pipe = StableDiffusionXLControlNetImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet,
    torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda")
pipe.enable_vae_tiling()

def canny(img):
    a = cv2.Canny(np.array(img), 80, 180)
    return Image.fromarray(np.stack([a] * 3, axis=-1))

srcs = sorted(glob.glob(os.path.join(ORIG, "*-orig.png")))
print(f"{len(srcs)} sources", flush=True)
for i, path in enumerate(srcs):
    name = os.path.basename(path).replace("-orig.png", "")
    out = os.path.join(OUT, f"{name}-sdxl.png")
    if os.path.exists(out):
        continue
    img = Image.open(path).convert("RGB")
    img.thumbnail((1152, 1152))
    w, h = (img.width // 8) * 8, (img.height // 8) * 8
    img = img.resize((w, h))
    t = time.time()
    try:
        result = pipe(prompt=PROMPT, negative_prompt=NEG,
                      image=img, control_image=canny(img),
                      strength=0.62, controlnet_conditioning_scale=0.55,
                      num_inference_steps=32, guidance_scale=7.0,
                      generator=torch.Generator("cuda").manual_seed(7)).images[0]
        result.save(out)
        print(f"[{i+1}/{len(srcs)}] {name} ok {time.time()-t:.0f}s", flush=True)
    except Exception as e:
        print(f"[{i+1}/{len(srcs)}] {name} FAILED {str(e)[:110]}", flush=True)
print("done", flush=True)
