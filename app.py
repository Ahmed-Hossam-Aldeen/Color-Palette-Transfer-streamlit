import numpy as np
import cv2
import os
import streamlit as st
import matplotlib.pyplot as plt
import io

st.markdown("<h1 style='text-align: center; color: white;'>🎨 Color Palette Transfer 🖌️</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size:17px; text-align: center; color: white;'>Upload 2 images first is the target image, second is the source image</h1>", unsafe_allow_html=True)
#############################################################################
def read_file(sn, tn):
    global col1, col2
    col1, col2 = st.columns(2)
    col1.image(sn, caption='Target Image', use_column_width=True)
    extract_color_palette(sn, colPlace=1)
    s = cv2.cvtColor(sn, cv2.COLOR_RGB2LAB)
    
    
    col2.image(tn, caption='Source Image', use_column_width=True)
    extract_color_palette(tn, colPlace=2)
    t = cv2.cvtColor(tn, cv2.COLOR_RGB2LAB)
    
    return s, t

def extract_color_palette(image, num_colors=5, colPlace=-1):   
    # Flatten the image into a 2D array of pixels
    pixels = image.reshape(-1, 3).astype(np.float32)

    # Use k-means clustering to extract dominant colors
    _, _, center = cv2.kmeans(pixels, num_colors, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10, cv2.KMEANS_RANDOM_CENTERS)
    colors = center.astype(int)

    # Convert RGB values to tuples
    colors = [tuple(color) for color in colors]

    # Plot the color palette
    fig, ax = plt.subplots(figsize=(8, 2)) # Adjust figure size here
    plt.axis('off')
    plt.tight_layout()
    ax.imshow([colors])
    ## Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    img_data = buf.read()
    plt.close()
    
    # Display color palette in Streamlit
    if colPlace == 1:
        col1.image(img_data, use_column_width=True)
    elif colPlace == 2:
        col2.image(img_data, use_column_width=True)   
    return colors

def get_mean_and_std(x):
    x_mean, x_std = cv2.meanStdDev(x)
    x_mean = np.hstack(np.around(x_mean, 2))
    x_std = np.hstack(np.around(x_std, 2))
    return x_mean, x_std

def color_transfer(src,tar): ### Image to be edited, Image color source
    s,t = read_file(src,tar)
    s_mean, s_std = get_mean_and_std(s)
    t_mean, t_std = get_mean_and_std(t)

    height, width, channel = s.shape
    for i in range(0, height):
        for j in range(0, width):
            for k in range(0, channel):
                x = s[i, j, k]
                x = ((x - s_mean[k]) * (t_std[k] / s_std[k])) + t_mean[k]
                # round or +0.5
                x = round(x)
                # boundary check
                x = 0 if x < 0 else x
                x = 255 if x > 255 else x
                s[i, j, k] = x

    s = cv2.cvtColor(s, cv2.COLOR_LAB2BGR)
    image3 = cv2.cvtColor(s, cv2.COLOR_BGR2RGB)
    st.image(image3, use_column_width=True)

##############################################################################
image_files = st.file_uploader("", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
if image_files is not None and len(image_files) == 2:
    source = np.asarray(bytearray(image_files[0].read()))
    source = cv2.imdecode(source, cv2.IMREAD_COLOR)
    source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)

    target = np.asarray(bytearray(image_files[1].read()))
    target = cv2.imdecode(target, cv2.IMREAD_COLOR)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)

    with st.spinner('Wait for it...'):
        color_transfer(source,target)
    st.success('Done!')

#########################################################
st.markdown("<h1 style='font-size:15px; text-align: center; color: red; font-family:SansSerif;'>Made with 💖 By Ahmed Hossam</h1>", unsafe_allow_html=True)
st.markdown("[My Github](https://github.com/Ahmed-Hossam-Aldeen)")
st.markdown("[Buy me a coffe!](https://www.buymeacoffee.com/ahmed01899a)")
st.image('https://www.buymeacoffee.com/assets/img/guidelines/download-assets-2.svg', width=200)