from alas.config import *

configs = [
    # 思源黑体特化训练
    get_config(1000, SourceHanSans_dir),

    # 科研标题特化训练
    get_config(1000, research1_dir),

    # 数字特化训练
    get_config(1000, numbers_dir),

    # 混合基础语料
    get_config(7000, base_dir)
]