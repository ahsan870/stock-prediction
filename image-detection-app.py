import streamlit as st
from PIL import Image
import io
import base64  # Add this import for base64


# Streamlit app
def main():
    st.title("Image Frame Adder")

    # File uploader for image
    uploaded_image = st.file_uploader("Choose an image:", type=["jpg", "jpeg", "png"])

    # Select a frame style
    frame_style = st.selectbox("Select a Frame Style:", ["Classic", "Modern", "Vintage"])

    framed_img = None

    # Button to add frame to the image
    if uploaded_image is not None:
        # Open the uploaded image
        img = Image.open(uploaded_image)

        # Add frame to the image
        framed_img = add_frame(img, frame_style)

        # Display the framed image
        st.image(framed_img, caption="Image with Frame", use_column_width=True)

    # Download link for the framed image
    if framed_img is not None:
        download_framed_image(framed_img)


def add_frame(img, frame_style):
    # Choose frame color based on style
    if frame_style == "Classic":
        frame_color = "black"
    elif frame_style == "Modern":
        frame_color = "white"
    elif frame_style == "Vintage":
        frame_color = "brown"

    # Calculate frame size
    frame_size = min(img.width, img.height) // 10

    # Create a new image with the frame
    framed_img = Image.new("RGB", (img.width + 2 * frame_size, img.height + 2 * frame_size), frame_color)

    # Paste the original image onto the framed image
    framed_img.paste(img, (frame_size, frame_size))

    return framed_img


def download_framed_image(framed_img):
    # Save the framed image to a BytesIO buffer
    img_buffer = io.BytesIO()
    framed_img.save(img_buffer, format="PNG")

    # Convert BytesIO buffer to bytes
    img_bytes = img_buffer.getvalue()

    # Create a download link for the framed image
    st.markdown(get_binary_file_downloader_html(img_bytes, 'framed_image.png', 'Download Framed Image'),
                unsafe_allow_html=True)


def get_binary_file_downloader_html(bin_file, file_label='File', button_label='Download'):
    with io.BytesIO(bin_file) as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">{button_label}</a>'
    return href


if __name__ == "__main__":
    main()
