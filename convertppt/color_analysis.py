from __future__ import annotations

from typing import Sequence

import numpy as np


Box = Sequence[Sequence[float]]
RGBTuple = tuple[int, int, int]
FALLBACK_RGB: RGBTuple = (0, 0, 0)


def _clamp_rgb(color: np.ndarray) -> RGBTuple:
    clipped = np.clip(np.rint(color), 0, 255).astype(np.uint8)
    return int(clipped[0]), int(clipped[1]), int(clipped[2])


def _luminance(color: np.ndarray) -> float:
    return float(0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])


def _crop_box(image_array: np.ndarray, box: Box) -> np.ndarray:
    if image_array.ndim < 2 or not box:
        return np.empty((0, 0, 3), dtype=np.uint8)

    x_coords = [point[0] for point in box]
    y_coords = [point[1] for point in box]
    x1 = max(0, int(min(x_coords)))
    y1 = max(0, int(min(y_coords)))
    x2 = min(image_array.shape[1], int(max(x_coords)))
    y2 = min(image_array.shape[0], int(max(y_coords)))

    if x2 <= x1 or y2 <= y1:
        return np.empty((0, 0, 3), dtype=np.uint8)

    return image_array[y1:y2, x1:x2]


def _downsample_roi(roi: np.ndarray, max_side: int = 64, max_pixels: int = 4096) -> np.ndarray:
    height, width = roi.shape[:2]
    step_y = max(1, int(np.ceil(height / max_side)))
    step_x = max(1, int(np.ceil(width / max_side)))
    sampled = roi[::step_y, ::step_x]

    if sampled.shape[0] * sampled.shape[1] > max_pixels:
        stride = int(np.ceil(np.sqrt((sampled.shape[0] * sampled.shape[1]) / max_pixels)))
        sampled = sampled[::stride, ::stride]

    return sampled


def estimate_text_rgb(image_array: np.ndarray, box: Box) -> RGBTuple:
    roi = _crop_box(image_array, box)
    if roi.size == 0:
        return FALLBACK_RGB

    if roi.ndim == 2:
        roi = np.repeat(roi[:, :, None], 3, axis=2)
    elif roi.shape[2] > 3:
        roi = roi[:, :, :3]

    roi = _downsample_roi(roi)
    pixels = roi.reshape(-1, 3).astype(np.float32)
    if len(pixels) == 0:
        return FALLBACK_RGB

    luminance = 0.299 * pixels[:, 0] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 2]
    spread = float(luminance.max() - luminance.min())
    if spread < 12:
        return _clamp_rgb(pixels.mean(axis=0))

    low_cut = np.percentile(luminance, 25)
    high_cut = np.percentile(luminance, 75)
    dark_pixels = pixels[luminance <= low_cut]
    light_pixels = pixels[luminance >= high_cut]

    scene_color = np.median(pixels, axis=0)
    dark_color = np.median(dark_pixels if len(dark_pixels) else pixels, axis=0)
    light_color = np.median(light_pixels if len(light_pixels) else pixels, axis=0)

    scene_luminance = _luminance(scene_color)
    dark_contrast = abs(_luminance(dark_color) - scene_luminance)
    light_contrast = abs(_luminance(light_color) - scene_luminance)

    if dark_contrast == light_contrast:
        candidate = dark_color if scene_luminance >= 128 else light_color
    else:
        candidate = dark_color if dark_contrast > light_contrast else light_color

    return _clamp_rgb(candidate)
