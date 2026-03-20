import os
from pathlib import Path
import json
import random

ALAS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

JSON_PATH = ALAS_DIR / 'output/labels.json'
TRAIN_TXT_PATH = ALAS_DIR / 'output/train.txt'
VAL_TXT_PATH = ALAS_DIR / 'output/val.txt'
SPLIT_RATIO = 0.9 # 90% 训练，10% 验证

def convert_labels():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取所有图片名和对应的标签
    # 注意：text_renderer 的 labels.json 结构通常是 {"labels": {"img.jpg": "text", ...}} 或直接是字典
    labels_dict = data.get("labels", data) if isinstance(data, dict) else data
    
    items = list(labels_dict.items())
    random.shuffle(items) # 打乱数据
    
    split_index = int(len(items) * SPLIT_RATIO)
    train_items = items[:split_index]
    val_items = items[split_index:]
    
    # 写入训练集 (注意必须是 \t 分隔)
    with open(TRAIN_TXT_PATH, 'w', encoding='utf-8') as f:
        for img_name, text in train_items:
            # 记录相对于数据集根目录的路径，或者直接写图片名（取决于你后续怎么配 yml）
            f.write(f"{img_name}.jpg\t{text}\n")
            
    # 写入验证集
    with open(VAL_TXT_PATH, 'w', encoding='utf-8') as f:
        for img_name, text in val_items:
            f.write(f"{img_name}.jpg\t{text}\n")
            
    print(f"转换成功！训练集: {len(train_items)} 张，验证集: {len(val_items)} 张。")

if __name__ == "__main__":
    convert_labels()
    os.remove(JSON_PATH)
    os.rename(ALAS_DIR / 'output/images', ALAS_DIR / 'output/imgs')
    os.rename(ALAS_DIR / 'output', ALAS_DIR / 'sets')