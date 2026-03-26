import os
from pathlib import Path

from text_renderer.config import GeneratorCfg, RenderCfg, RangeTextColorCfg
from text_renderer.corpus import EnumCorpus, EnumCorpusCfg
from text_renderer.effect import Effects, DropoutRand, DropoutEdge

ALAS_DIR = Path(os.path.abspath(os.path.dirname(__file__)))

bg_dir = ALAS_DIR / "bg_generator/output"

base_dir = ALAS_DIR / 'base'
commision_zone_dir = ALAS_DIR / 'commision_zone'
numbers_dir = ALAS_DIR / 'numbers'
research_dir = ALAS_DIR / 'research'
time_level_dir = ALAS_DIR / 'time_level'

def get_config(num_image, dir):
    return GeneratorCfg(
        num_image=num_image,
        save_dir=ALAS_DIR / "output",
        render_cfg=RenderCfg(
            height=-1,
            gray=True,
            bg_dir=bg_dir,
            corpus=EnumCorpus(
                EnumCorpusCfg(
                    text_paths=[dir / "text" / "corpus.txt"],
                    font_dir=dir / "fonts",
                    font_size=(20, 50),
                    filter_by_chars=False,
                    text_color_cfg=RangeTextColorCfg(
                        color_ranges={
                            "black": {
                                "fraction": 1.0,
                                "l_boundary": [0, 0, 0],
                                "h_boundary": [50, 50, 50],
                            }
                        }
                    ),
                )
            ),
            corpus_effects=Effects(
                [
                    DropoutEdge(p=1.0, dropout_p=(0.3, 0.5), iterations=1),
                    DropoutRand(p=0.3, dropout_p=(0.01, 0.05))
                ]
            )
        )
    )