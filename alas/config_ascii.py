import os
from pathlib import Path
from text_renderer.effect import *
from text_renderer.corpus import EnumCorpus, EnumCorpusCfg
from text_renderer.config import RenderCfg, GeneratorCfg, SimpleTextColorCfg

ALAS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

bg_dir = ALAS_DIR / 'bg_generator/output'

base_dir = ALAS_DIR / 'base'
SourceHanSans_dir = ALAS_DIR / 'SourceHanSans'
research1_dir = ALAS_DIR / 'research1'
research2_dir = ALAS_DIR / 'research2'
numbers_dir = ALAS_DIR / 'numbers'

def get_config(num_image, dir):
    return GeneratorCfg(
        num_image=num_image,
        save_dir=ALAS_DIR / "output",
        render_cfg=RenderCfg(
            bg_dir=bg_dir,
            gray=False,
            corpus=EnumCorpus(
                EnumCorpusCfg(
                    text_paths=[dir / "text" / "corpus.txt"],
                    font_dir=dir / "fonts",
                    font_size=(30, 35),
                    filter_by_chars=False,
                    text_color_cfg=SimpleTextColorCfg(),
                )
            ),
            corpus_effects=Effects([
                DropoutRand(p=0.5, dropout_p=(0.01, 0.05))
            ])
        )
    )

configs = [
    # 科研代码特化训练
    get_config(1000, research2_dir),

    # 数字训练
    get_config(9000, numbers_dir)
]