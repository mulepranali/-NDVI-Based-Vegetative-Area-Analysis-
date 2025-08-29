# import streamlit as st
# import tempfile
# import os
# import matplotlib.pyplot as plt
# from ndvi_utils import calculate_ndvi, classify_vegetation, get_stats, draw_contours_on_ndvi

# st.set_page_config(page_title="NDVI Analyzer", layout="wide")

# st.title("🌾 Satellite NDVI Vegetation Analyzer")

# st.write("Upload **Red (B04)** and **NIR (B08)** band TIFF files below:")

# red_file = st.file_uploader("Upload Red Band (B04)", type=["tif", "tiff"])
# nir_file = st.file_uploader("Upload NIR Band (B08)", type=["tif", "tiff"])

# if red_file and nir_file:
#     # Write uploaded files to temporary files
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_red, \
#          tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_nir:
#         tmp_red.write(red_file.read())
#         tmp_nir.write(nir_file.read())
#         red_path = tmp_red.name
#         nir_path = tmp_nir.name

#     st.success("Files uploaded successfully!")

#     # Process NDVI
#     ndvi = calculate_ndvi(red_path, nir_path)
#     healthy, moderate, unhealthy = classify_vegetation(ndvi)
#     stats = get_stats(ndvi, healthy, moderate, unhealthy)
#     bordered_image = draw_contours_on_ndvi(ndvi, healthy, moderate, unhealthy)

#     # Display statistics
#     st.subheader("📈 NDVI Stats")
#     st.write(f"Min NDVI: {stats['ndvi_min']:.2f}")
#     st.write(f"Max NDVI: {stats['ndvi_max']:.2f}")
#     st.write(f"Healthy Pixels: {stats['healthy_pixels']} ({stats['healthy_pct']}%)")
#     st.write(f"Moderate Pixels: {stats['moderate_pixels']} ({stats['moderate_pct']}%)")
#     st.write(f"Unhealthy Pixels: {stats['unhealthy_pixels']} ({stats['unhealthy_pct']}%)")

#     # Display image
#     st.subheader("🖼️ NDVI Map with Health Zones")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.imshow(bordered_image)
#     ax.axis('off')
#     st.pyplot(fig)

#     # Safely remove temp files
#     try:
#         os.unlink(red_path)
#         os.unlink(nir_path)
#     except Exception as e:
#         st.warning(f"Temporary file deletion failed: {e}")

import streamlit as st
import tempfile
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ndvi_utils import calculate_ndvi, classify_vegetation, get_stats, draw_contours_on_ndvi
import rasterio

st.set_page_config(page_title="NDVI Analyzer", layout="wide")

st.title("🌾 Satellite NDVI Vegetation Analyzer")
st.write("Upload **Red (B04)** and **NIR (B08)** band TIFF files below:")

def enhance_resolution(tif_path, scale_factor=2):
    """Upscale TIFF preserving reflectance values."""
    with rasterio.open(tif_path) as src:
        image = src.read(1)  # Single band
        profile = src.profile

    # Get new dimensions
    new_w = int(image.shape[1] * scale_factor)
    new_h = int(image.shape[0] * scale_factor)

    # Upscale with OpenCV while preserving float/uint16 values
    upscaled = cv2.resize(
        image, 
        (new_w, new_h), 
        interpolation=cv2.INTER_LANCZOS4
    )

    # Save back to temp file with original metadata
    tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".tif")
    profile.update(width=new_w, height=new_h)
    with rasterio.open(tmp_out.name, 'w', **profile) as dst:
        dst.write(upscaled.astype(profile['dtype']), 1)

    return tmp_out.name


red_file = st.file_uploader("Upload Red Band (B04)", type=["tif", "tiff"])
nir_file = st.file_uploader("Upload NIR Band (B08)", type=["tif", "tiff"])

if red_file and nir_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_red, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".tif") as tmp_nir:
        tmp_red.write(red_file.read())
        tmp_nir.write(nir_file.read())
        red_path = tmp_red.name
        nir_path = tmp_nir.name

    st.success("Files uploaded successfully! Enhancing resolution...")

    # Enhance both images
    red_path = enhance_resolution(red_path, scale_factor=2)
    nir_path = enhance_resolution(nir_path, scale_factor=2)

    # Process NDVI
    ndvi = calculate_ndvi(red_path, nir_path)
    healthy, moderate, unhealthy = classify_vegetation(ndvi)
    stats = get_stats(ndvi, healthy, moderate, unhealthy)
    bordered_image = draw_contours_on_ndvi(ndvi, healthy, moderate, unhealthy)

    # Display statistics
    st.subheader("📈 NDVI Stats")
    st.write(f"Min NDVI: {stats['ndvi_min']:.2f}")
    st.write(f"Max NDVI: {stats['ndvi_max']:.2f}")
    st.write(f"Healthy Pixels: {stats['healthy_pixels']} ({stats['healthy_pct']}%)")
    st.write(f"Moderate Pixels: {stats['moderate_pixels']} ({stats['moderate_pct']}%)")
    st.write(f"Unhealthy Pixels: {stats['unhealthy_pixels']} ({stats['unhealthy_pct']}%)")

    # Display image
    st.subheader("🖼️ NDVI Map with Health Zones")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(bordered_image)
    ax.axis('off')
    st.pyplot(fig)

    # Cleanup
    try:
        os.unlink(red_path)
        os.unlink(nir_path)
    except Exception as e:
        st.warning(f"Temporary file deletion failed: {e}")
