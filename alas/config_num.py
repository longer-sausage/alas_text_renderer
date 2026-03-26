from alas.config import *

configs = [
    # 科研代码特化训练
    get_config(1500, research_dir),

    # 时间和关卡训练
    get_config(1500, time_level_dir),

    # 数字训练
    get_config(7000, numbers_dir)
]