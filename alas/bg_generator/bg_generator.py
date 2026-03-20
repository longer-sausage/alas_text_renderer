import cv2
import numpy as np
import os
from pathlib import Path
import random

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))


def get_orange_color():
    r = random.randint(200, 255)
    g = random.randint(100, 160)
    b = random.randint(0, 50)
    return r, g, b


def get_blue_color():
    r = random.randint(0, 50)
    g = random.randint(0, 100)
    b = random.randint(200, 255)
    return r, g, b


def get_gray_color():
    base = random.randint(50, 200)
    r = np.clip(base + random.randint(-10, 10), 0, 255)
    g = np.clip(base + random.randint(-10, 10), 0, 255)
    b = np.clip(base + random.randint(-10, 10), 0, 255)
    return int(r), int(g), int(b)


def get_white_color():
    base = random.randint(230, 245)
    r = np.clip(base + random.randint(-10, 10), 0, 255)
    g = np.clip(base + random.randint(-10, 10), 0, 255)
    b = np.clip(base + random.randint(-10, 10), 0, 255)
    return int(r), int(g), int(b)


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def generate(num_images=100, save_dir=CURRENT_DIR / "output", width=600, height=64):
    os.makedirs(save_dir, exist_ok=True)

    color_generators = [
        get_orange_color,
        get_blue_color,
        get_gray_color,
        get_white_color,
        get_random_color,
    ]

    gen_list = []
    num_per_cat = num_images // len(color_generators)
    for i in range(len(color_generators)):
        gen_list.extend([color_generators[i]] * num_per_cat)

    # Add remaining images
    remaining = num_images - len(gen_list)
    for i in range(remaining):
        gen_list.append(random.choice(color_generators))

    random.shuffle(gen_list)

    for i in range(num_images):
        color_gen = gen_list[i]
        r, g, b = color_gen()

        # OpenCV 默认使用 BGR 通道顺序
        img = np.full((height, width, 3), (b, g, r), dtype=np.uint8)

        # 深色背景上的噪点如果波动太大容易失真，这里稍微控制一下噪点强度
        sigma = random.randint(15, 30)
        noise = np.random.normal(0, sigma, img.shape)

        # 叠加并保存
        noisy_img = img + noise
        noisy_img = np.clip(noisy_img, 0, 255).astype(np.uint8)

        save_path = os.path.join(save_dir, f"bg_{i:04d}.jpg")
        cv2.imwrite(save_path, noisy_img)

    print(f"成功生成 {num_images} 张背景图，保存在 {save_dir}！")


if __name__ == "__main__":
    generate(num_images=500)