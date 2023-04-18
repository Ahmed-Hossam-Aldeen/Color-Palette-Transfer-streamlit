# Color-Palette-Transfer-streamlit

Color Palette Transfer is a Python-based web application that allows users to transfer the color palette from one image to another. It uses k-means clustering to extract dominant colors from images and applies color transfer techniques to transfer the color palette from a source image to a target image.

Features:

- Upload two images (source and target) for color transfer
- Extract color palettes from the source and target images
- Transfer the color palette from the source image to the target image
- Display the transferred image with the new color palette

Dependencies:

- Python 3.6 or higher
- OpenCV
- NumPy
- Streamlit
- Matplotlib

Usage:

1. Run the Streamlit app:

   streamlit run app.py

2. Access the application in your web browser at http://localhost:8501.

3. Follow the instructions in the web application to upload a source image and a target image.

4. The color palette from the source image will be extracted and displayed. Click on the "Transfer" button to transfer the color palette to the target image.

5. The transferred image with the new color palette will be displayed. You can download the transferred image for further use.
