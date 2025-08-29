# import numpy as np
# import cv2
# import matplotlib.pyplot as plt
# import rasterio

# def calculate_ndvi(red_band_path, nir_band_path):
#     with rasterio.open(red_band_path) as red_src:
#         red = red_src.read(1).astype('float32')
#     with rasterio.open(nir_band_path) as nir_src:
#         nir = nir_src.read(1).astype('float32')

#     ndvi = (nir - red) / (nir + red)
#     ndvi = np.clip(ndvi, -1, 1)
#     return ndvi

# def classify_vegetation(ndvi):
#     healthy = ndvi > 0.5
#     moderate = (ndvi > 0.2) & (ndvi <= 0.5)
#     unhealthy = ndvi <= 0.2
#     return healthy, moderate, unhealthy

# def get_stats(ndvi, healthy, moderate, unhealthy):
#     total_pixels = ndvi.size
#     return {
#         'ndvi_min': float(np.nanmin(ndvi)),
#         'ndvi_max': float(np.nanmax(ndvi)),
#         'healthy_pct': round(np.sum(healthy) / total_pixels * 100, 2),
#         'moderate_pct': round(np.sum(moderate) / total_pixels * 100, 2),
#         'unhealthy_pct': round(np.sum(unhealthy) / total_pixels * 100, 2),
#         'healthy_pixels': int(np.sum(healthy)),
#         'moderate_pixels': int(np.sum(moderate)),
#         'unhealthy_pixels': int(np.sum(unhealthy))
#     }

# def draw_contours_on_ndvi(ndvi, healthy, moderate, unhealthy):
#     healthy_uint8 = healthy.astype(np.uint8)
#     moderate_uint8 = moderate.astype(np.uint8)
#     unhealthy_uint8 = unhealthy.astype(np.uint8)

#     healthy_contours, _ = cv2.findContours(healthy_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     moderate_contours, _ = cv2.findContours(moderate_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     unhealthy_contours, _ = cv2.findContours(unhealthy_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     ndvi_rgb = plt.cm.RdYlGn((ndvi + 1) / 2)[:, :, :3]
#     ndvi_rgb = (ndvi_rgb * 255).astype(np.uint8)

#     for contour in healthy_contours:
#         cv2.drawContours(ndvi_rgb, [contour], -1, (0, 255, 0), 1)
#     for contour in moderate_contours:
#         cv2.drawContours(ndvi_rgb, [contour], -1, (255, 255, 0), 1)
#     for contour in unhealthy_contours:
#         cv2.drawContours(ndvi_rgb, [contour], -1, (255, 0, 0), 1)

#     return ndvi_rgb
# # 

import numpy as np
import cv2
import matplotlib.pyplot as plt
import rasterio

def calculate_ndvi(red_band_path, nir_band_path):
    with rasterio.open(red_band_path) as red_src:
        red = red_src.read(1).astype('float32')
        transform = red_src.transform  # for pixel size
    with rasterio.open(nir_band_path) as nir_src:
        nir = nir_src.read(1).astype('float32')

    ndvi = (nir - red) / (nir + red)
    ndvi = np.clip(ndvi, -1, 1)
    return ndvi, transform

def classify_vegetation(ndvi):
    healthy = ndvi > 0.5
    moderate = (ndvi > 0.2) & (ndvi <= 0.5)
    unhealthy = ndvi <= 0.2
    return healthy, moderate, unhealthy

def get_stats(ndvi, healthy, moderate, unhealthy, transform):
    pixel_width = transform[0]
    pixel_height = -transform[4]  # usually negative
    pixel_area_m2 = abs(pixel_width * pixel_height)

    total_pixels = ndvi.size
    return {
        'ndvi_min': float(np.nanmin(ndvi)),
        'ndvi_max': float(np.nanmax(ndvi)),
        'healthy_pct': round(np.sum(healthy) / total_pixels * 100, 2),
        'moderate_pct': round(np.sum(moderate) / total_pixels * 100, 2),
        'unhealthy_pct': round(np.sum(unhealthy) / total_pixels * 100, 2),
        'pixel_area_m2': round(total_pixels * pixel_area_m2, 2),
        'healthy_pixels': int(np.sum(healthy)),
        'moderate_pixels': int(np.sum(moderate)),
        'unhealthy_pixels': int(np.sum(unhealthy))
    }

def draw_contours_on_ndvi(ndvi, healthy, moderate, unhealthy):
    healthy_uint8 = healthy.astype(np.uint8)
    moderate_uint8 = moderate.astype(np.uint8)
    unhealthy_uint8 = unhealthy.astype(np.uint8)

    healthy_contours, _ = cv2.findContours(healthy_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    moderate_contours, _ = cv2.findContours(moderate_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    unhealthy_contours, _ = cv2.findContours(unhealthy_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ndvi_rgb = plt.cm.RdYlGn((ndvi + 1) / 2)[:, :, :3]
    ndvi_rgb = (ndvi_rgb * 255).astype(np.uint8)

    for contour in healthy_contours:
        cv2.drawContours(ndvi_rgb, [contour], -1, (0, 255, 0), 1)
    for contour in moderate_contours:
        cv2.drawContours(ndvi_rgb, [contour], -1, (255, 255, 0), 1)
    for contour in unhealthy_contours:
        cv2.drawContours(ndvi_rgb, [contour], -1, (255, 0, 0), 1)

    return ndvi_rgb
