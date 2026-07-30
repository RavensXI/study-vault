# -*- coding: utf-8 -*-
"""Open-weights line-and-wash pilot — runs ON THE RENTED POD (Linux, CUDA).

Qwen-Image-Edit (Apache 2.0 — commercially clean) over the 28 pilot heroes,
using the locked refined-study prompt. Reads /workspace/orig/*.png, writes
/workspace/out/{name}-qwen.png. Resumable: existing outputs are skipped.

Setup (once):  pip install -q torch diffusers transformers accelerate safetensors pillow
Run:           python3 _ow_pilot_pod.py
"""
import glob
import os
import sys
import time

import torch
try:  # 2509 ships as "Edit Plus" in newer diffusers; fall back if absent
    from diffusers import QwenImageEditPlusPipeline as QwenImageEditPipeline
except ImportError:
    from diffusers import QwenImageEditPipeline
from PIL import Image

ORIG = "/workspace/orig"
OUT = "/workspace/out"
os.makedirs(OUT, exist_ok=True)

KEEP = ("Keep the SAME composition and layout — every element in the SAME place as the input image. "
        "ABSOLUTELY NO text, words, letters or numbers.")
PROMPT = ("Redraw this exact image as a REFINED study, partway to finished: clean confident pen-and-ink "
          "linework tracing the forms with a first thin watercolour wash of the same colours, still mostly warm "
          "uncoloured paper — as if the picture is coming into focus. " + KEEP)

print("loading Qwen-Image-Edit-2509 (8-bit transformer)…", flush=True)
t0 = time.time()
# 20B bf16 = ~56GB total, which wedged the 50GB-RAM pod via cpu-offload.
# 8-bit transformer (~20GB) + bf16 text encoder (~16GB) + VAE fits the
# A40's 46GB of VRAM outright — no offload, no RAM involvement at all.
from diffusers import PipelineQuantizationConfig
quant = PipelineQuantizationConfig(
    quant_backend="bitsandbytes_8bit",
    quant_kwargs={"load_in_8bit": True},
    components_to_quantize=["transformer"])
pipe = QwenImageEditPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit-2509", torch_dtype=torch.bfloat16,
    quantization_config=quant)
pipe.to("cuda")
print(f"loaded in {time.time()-t0:.0f}s", flush=True)

srcs = sorted(glob.glob(os.path.join(ORIG, "*-orig.png")))
print(f"{len(srcs)} source heroes", flush=True)

for i, path in enumerate(srcs):
    name = os.path.basename(path).replace("-orig.png", "")
    out = os.path.join(OUT, f"{name}-qwen.png")
    if os.path.exists(out):
        print(f"[{i+1}/{len(srcs)}] {name} cached", flush=True)
        continue
    img = Image.open(path).convert("RGB")
    # keep the model's working size sane; upscale gently after if needed
    img.thumbnail((1280, 1280))
    t = time.time()
    try:
        result = pipe(image=img, prompt=PROMPT,
                      negative_prompt=" ",  # required to actually enable true_cfg guidance
                      num_inference_steps=40, true_cfg_scale=4.0,
                      generator=torch.Generator("cuda").manual_seed(7)).images[0]
        result.save(out)
        print(f"[{i+1}/{len(srcs)}] {name} ok {time.time()-t:.0f}s", flush=True)
    except Exception as e:
        print(f"[{i+1}/{len(srcs)}] {name} FAILED {str(e)[:120]}", flush=True)

print("done", flush=True)
