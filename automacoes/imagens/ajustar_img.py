#!/usr/bin/env python3
"""
Comprimir imagens, exige Pillow (pip install Pillow).

"""

import argparse
import io
import math
import os
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def load_image(path: Path) -> Image.Image:
    img = Image.open(path)
    if img.mode == "P":
        img = img.convert("RGBA")
    return img


def ensure_mode_for_format(img: Image.Image, fmt: str) -> Image.Image:
    fmt = fmt.upper()
    if fmt in ("JPEG", "JPG"):
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1])
            return bg
        if img.mode not in ("RGB",):
            return img.convert("RGB")
    elif fmt == "WEBP":
        pass
    else:
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    return img


def bytes_of_save(img: Image.Image, fmt: str, quality: int = 85, **save_kwargs) -> bytes:
    buf = io.BytesIO()
    kwargs = dict(save_kwargs)
    fmt_u = fmt.upper()
    if fmt_u in ("JPEG", "JPG"):
        kwargs.setdefault("optimize", True)
        kwargs.setdefault("quality", quality)
        kwargs.setdefault("progressive", True)
        img.save(buf, format="JPEG", **kwargs)
    elif fmt_u == "WEBP":
        kwargs.setdefault("quality", quality)
        kwargs.setdefault("method", 6)  
        kwargs.setdefault("lossless", False)
        img.save(buf, format="WEBP", **kwargs)
    else:
        if "quality" in Image.SAVE:
            kwargs.setdefault("quality", quality)
        img.save(buf, format=fmt_u, **kwargs)
    return buf.getvalue()


def binary_search_quality(img: Image.Image, fmt: str, target_bytes: int, q_min=5, q_max=95, max_iters=8, **save_kwargs):

    best = None
    lo, hi = q_min, q_max
    for _ in range(max_iters):
        mid = (lo + hi) // 2
        data = bytes_of_save(img, fmt, quality=mid, **save_kwargs)
        size = len(data)
        if size <= target_bytes:
            best = (data, mid)
            lo = mid + 1 
        else:
            hi = mid - 1  
    if best is None:
        data = bytes_of_save(img, fmt, quality=q_min, **save_kwargs)
        if len(data) <= target_bytes:
            return data, q_min
        return None, None
    return best


def scale_by_factor(img: Image.Image, factor: float) -> Image.Image:
    w, h = img.size
    new_w = max(1, int(w * factor))
    new_h = max(1, int(h * factor))
    if (new_w, new_h) == (w, h):
        new_w = max(1, w - 1)
        new_h = max(1, h - 1)
    return img.resize((new_w, new_h), Image.LANCZOS)


def compress_to_target(
    input_path: Path,
    output_path: Path,
    target_kb: int = 70,
    fmt: str = "JPEG",
    max_width: int | None = None,
    quality_min: int = 5,
    quality_max: int = 95,
    max_passes: int = 6,
    **save_kwargs,
) -> tuple[Path, int, tuple[int, int], int]:
    img = load_image(input_path)
    fmt = fmt.upper()
    img = ensure_mode_for_format(img, fmt)

    if max_width is not None and img.width > max_width:
        factor = max_width / float(img.width)
        img = scale_by_factor(img, factor)

    target_bytes = target_kb * 1024

    data_quality, q_used = binary_search_quality(img, fmt, target_bytes, q_min=quality_min, q_max=quality_max, **save_kwargs)
    if data_quality is not None:
        output_path.write_bytes(data_quality)
        return output_path, len(data_quality) // 1024, img.size, q_used

    data_low = bytes_of_save(img, fmt, quality=quality_min, **save_kwargs)
    current_bytes = len(data_low)

    passes = 0
    cur_img = img
    while current_bytes > target_bytes and passes < max_passes:
        factor = math.sqrt(target_bytes / current_bytes) * 0.98  
        factor = min(factor, 0.95)
        factor = max(factor, 0.5)
        cur_img = scale_by_factor(cur_img, factor)
        data_quality, q_used = binary_search_quality(cur_img, fmt, target_bytes, q_min=quality_min, q_max=quality_max, **save_kwargs)
        if data_quality is not None:
            output_path.write_bytes(data_quality)
            return output_path, len(data_quality) // 1024, cur_img.size, q_used
        data_low = bytes_of_save(cur_img, fmt, quality=quality_min, **save_kwargs)
        current_bytes = len(data_low)
        passes += 1

    output_path.write_bytes(data_low)
    return output_path, len(data_low) // 1024, cur_img.size, quality_min


def main():
    parser = argparse.ArgumentParser(description="Compress an image to a target size (KB).")
    parser.add_argument("input", type=Path, help="Path to input image (jpg/png/webp/...)")
    parser.add_argument("--out", type=Path, default=None, help="Output file path. Defaults to <input>_compressed.<ext>")
    parser.add_argument("--target", type=int, default=70, help="Target size in KB (default: 70)")
    parser.add_argument("--format", type=str, default="JPEG", help="Output format: JPEG or WEBP (default: JPEG)")
    parser.add_argument("--max-width", type=int, default=None, help="Optional max width to downscale before compressing")
    parser.add_argument("--quality-min", type=int, default=5, help="Minimum quality bound (default: 5)")
    parser.add_argument("--quality-max", type=int, default=95, help="Maximum quality bound (default: 95)")
    args = parser.parse_args()

    input_path: Path = args.input
    output_fmt = args.format.upper()
    if args.out is None:
        stem = input_path.with_suffix("").name + "_compressed"
        ext = ".jpg" if output_fmt in ("JPEG", "JPG") else ".webp" if output_fmt == "WEBP" else f".{output_fmt.lower()}"
        output_path = input_path.with_name(stem + ext)
    else:
        output_path = args.out

    output_path.parent.mkdir(parents=True, exist_ok=True)

    out_path, size_kb, final_size, q = compress_to_target(
        input_path,
        output_path,
        target_kb=args.target,
        fmt=output_fmt,
        max_width=args.max_width,
        quality_min=args.quality_min,
        quality_max=args.quality_max,
    )

    print(f"✅ Gerado: {out_path}")
    print(f"   Tamanho final: {size_kb} KB (alvo: {args.target} KB)")
    print(f"   Dimensões: {final_size[0]}x{final_size[1]}")
    print(f"   Qualidade usada: {q} ({output_fmt})")


if __name__ == "__main__":
    main()
