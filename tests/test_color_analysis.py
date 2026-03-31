from __future__ import annotations

import numpy as np

from convertppt.color_analysis import estimate_text_rgb


def test_estimate_text_rgb_prefers_dark_text_on_light_background() -> None:
    image = np.full((80, 200, 3), 245, dtype=np.uint8)
    image[20:60, 40:160] = 20

    color = estimate_text_rgb(image, [[40, 20], [160, 20], [160, 60], [40, 60]])

    assert max(color) < 80


def test_estimate_text_rgb_prefers_light_text_on_dark_background() -> None:
    image = np.full((80, 200, 3), 25, dtype=np.uint8)
    image[20:60, 40:160] = 240

    color = estimate_text_rgb(image, [[40, 20], [160, 20], [160, 60], [40, 60]])

    assert min(color) > 180
