from alas.config import *

configs = [
    # 委托和海域名特化训练
    get_config(1500, commision_zone_dir),

    # 数字特化训练
    get_config(1500, numbers_dir),

    # 混合基础语料
    get_config(7000, base_dir)
]