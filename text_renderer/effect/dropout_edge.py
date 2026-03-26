import random
from typing import Tuple

import numpy as np
from scipy import ndimage

from text_renderer.utils.bbox import BBox
from text_renderer.utils.types import PILImage

from .base_effect import Effect


class DropoutEdge(Effect):
    def __init__(self, p=0.5, dropout_p=(0.2, 0.4), iterations=1):
        """
        Drop pixels only at the edges of the text.

        Parameters
        ----------
        p : float
            Probability of applying this effect.
        dropout_p : Tuple[float, float]
            The percentage range of pixels to be discarded among the edge pixels.
        iterations : int
            The width of the edge in pixels to consider for dropout.
        """
        super().__init__(p)
        self.dropout_p = dropout_p
        self.iterations = iterations

    def apply(self, img: PILImage, text_bbox: BBox) -> Tuple[PILImage, BBox]:
        pim = img.load()
        
        # Get alpha channel mask
        # img is PILImage, convert to numpy array to get alpha channel
        img_array = np.array(img).astype(np.uint8)
        if img_array.shape[2] < 4:
            # If no alpha channel, cannot determine text edges reliably 
            # unless we assume some color is background. 
            # In this project, text rendering usually has RGBA.
            return img, text_bbox

        alpha_channel = img_array[:, :, 3]
        mask = (alpha_channel > 0).astype(np.bool_)
        
        # Find inner part by erosion
        # Use a default 3x3 footprint for binary_erosion
        inner_mask = ndimage.binary_erosion(mask, iterations=self.iterations)
        
        # Edge pixels are in original mask but not in inner mask
        edge_mask = mask & (~inner_mask)
        edge_idxes = np.argwhere(edge_mask)
        
        edge_count = edge_idxes.shape[0]
        if edge_count == 0:
            return img, text_bbox
            
        random_dropout_count = random.randint(
            int(edge_count * self.dropout_p[0]),
            int(edge_count * self.dropout_p[1]),
        )
        
        if random_dropout_count == 0:
            return img, text_bbox
            
        # Shuffle indices to randomly pick pixels to drop
        shuffled = np.random.permutation(edge_count)
        shuffled = shuffled[:random_dropout_count]

        for i in shuffled:
            y, x = edge_idxes[i]
            col = int(x)
            row = int(y)
            # rand_pick reduces pixel values randomly, including alpha
            self.rand_pick(pim, col, row)

        return img, text_bbox
