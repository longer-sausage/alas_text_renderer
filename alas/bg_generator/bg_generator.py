import cv2
import numpy as np
import os
from pathlib import Path
import random
from tqdm import tqdm

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

def get_gray_color(base_min=50, base_max=200, delta=10):
    """生成一个灰度值"""
    base = random.randint(base_min, base_max)
    gray = np.clip(base + random.randint(-delta, delta), 0, 255)
    return int(gray)


def get_white_color(base_min=220, base_max=255, delta=10):
    """生成一个近白色的灰度值"""
    return get_gray_color(base_min, base_max, delta)


def add_long_lines(img):
    """在图片上随机添加大部分贯穿整个图像的长线条"""
    if random.random() < 0.4:
        return

    h, w = img.shape[:2]
    num_lines = random.randint(2, 5)
    for _ in range(num_lines):
        # 通过定义一个长向量来创建长线条
        diag = np.sqrt(h**2 + w**2)
        length = diag * random.uniform(0.8, 1.5)

        # 中心点可以在图像内或略微超出
        cx = random.randint(0, w)
        cy = random.randint(0, h)

        angle = np.deg2rad(random.uniform(0, 360))

        x1 = int(cx - length * np.cos(angle))
        y1 = int(cy - length * np.sin(angle))
        x2 = int(cx + length * np.cos(angle))
        y2 = int(cy + length * np.sin(angle))

        color = (get_gray_color(100, 200),) * 3
        thickness = random.randint(1, 2)

        # cv2.line 可以正确处理超出图像边界的端点
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def add_shadow_effect(img):
    """在图片上随机添加阴影效果"""
    if random.random() < 0.6:
        return

    h, w = img.shape[:2]

    # 创建一个黑色的遮罩
    overlay = np.zeros_like(img, dtype=np.float32)

    num_shapes = random.randint(2, 4)
    for _ in range(num_shapes):
        cx, cy = random.randint(0, w), random.randint(0, h)
        major_axis = random.randint(w // 3, w)
        minor_axis = random.randint(h // 3, h)
        angle = random.randint(0, 90)

        # 在遮罩上画一个白色的椭圆
        color = (255, 255, 255)

        cv2.ellipse(
            overlay, (cx, cy), (major_axis, minor_axis), angle, 0, 360, color, -1
        )

    # 对遮罩进行高斯模糊，以柔化阴影边缘
    kernel_size = int(max(w, h) * random.uniform(0.4, 0.8))
    if kernel_size % 2 == 0:
        kernel_size += 1

    if kernel_size > 1:
        overlay = cv2.GaussianBlur(overlay, (kernel_size, kernel_size), 0)

    # 将遮罩（现在是模糊的白色形状）从原图上减去，形成阴影
    # 通过调整 alpha 控制阴影的强度
    alpha = random.uniform(0.15, 0.45)
    shadow = (overlay * alpha).astype(np.uint8)

    img[:] = cv2.subtract(img, shadow)


def generate(
    num_images,
    save_dir=CURRENT_DIR / "output",
    width=600,
    height=100
):
    os.makedirs(save_dir, exist_ok=True)

    for i in tqdm(range(num_images), desc="Generating background images"):
        # 1. 创建一个基本纯白的背景
        bg_color = (get_white_color(),) * 3
        img = np.full((height, width, 3), bg_color, dtype=np.uint8)

        # 2. 添加阴影效果
        add_shadow_effect(img)

        # 3. 添加长线条
        add_long_lines(img)

        save_path = os.path.join(save_dir, f"bg_{i:04d}.jpg")
        cv2.imwrite(save_path, img)

    print(f"成功生成 {num_images} 张背景图，保存在 {save_dir}！")


if __name__ == "__main__":
    output_dir = CURRENT_DIR / "output"
    generate(500)
