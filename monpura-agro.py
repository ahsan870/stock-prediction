import streamlit as st
from PIL import Image, ExifTags, ImageDraw, ImageFont
import io
import base64
from PIL import UnidentifiedImageError

# Streamlit app
def main():
    st.title("Image Frame Adder")

    # File uploader for image
    uploaded_image = st.file_uploader("Choose an image:", type=["jpg", "jpeg", "png"])

    # Product details
    product_id = st.text_input("Product ID:")
    price = st.text_input("Price:")

    # Select a custom frame (replace 'path/to/your/frame.png' with the actual path)
    custom_frame_path = 'images/firm1.png'

    framed_img = None

    try:
        # Button to add frame to the image
        if uploaded_image is not None:
            # Open the uploaded image
            img = Image.open(uploaded_image)

            # Add custom frame and product details to the image
            framed_img = add_frame(img, custom_frame_path, product_id, price)

            # Display the framed image
            st.image(framed_img, caption="Image with Custom Frame", use_column_width=True)

        # Download link for the framed image
        if framed_img is not None:
            download_framed_image(framed_img)

    except UnidentifiedImageError:
        st.error("Error: Unable to identify the image. Please make sure it is a valid image file.")

def add_frame(img, custom_frame_path, product_id, price):
    # Open the custom frame image
    custom_frame = Image.open(custom_frame_path).convert("RGBA")

    # Resize the frame to match the dimensions of the input image
    custom_frame = custom_frame.resize((img.width, img.height))

    # Ensure proper orientation of the input image
    img = fix_orientation(img)

    # Create a copy of the original image
    framed_img = img.copy()

    # Paste the custom frame onto the new image
    framed_img.paste(custom_frame, (0, 0), custom_frame)

    # Draw product details on the framed image
    draw = ImageDraw.Draw(framed_img)

    # Use default font for text drawing
    font_size = 100
    font = ImageFont.load_default()

    text = f"Product ID: {product_id}\nPrice BDT: {price}"

    # Calculate text size using draw.textbbox method
    text_width, text_height = calculate_text_size(draw, text, font)

    draw.text(((framed_img.width - text_width) // 8, framed_img.height - text_height - 40), text, font=font, fill=(255, 255, 255, 255))


    return framed_img


def calculate_text_size(draw, text, font):
    # Calculate text size using draw.textbbox method
    dummy_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    dummy_draw = ImageDraw.Draw(dummy_img)
    text_bbox = dummy_draw.textbbox((0, 0), text, font=font)

    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    return text_width, text_height

def fix_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No EXIF data, or certain keys not present
        pass

    return img

def download_framed_image(framed_img):
    # Save the framed image to a BytesIO buffer
    img_buffer = io.BytesIO()
    framed_img.save(img_buffer, format="PNG")

    # Convert BytesIO buffer to bytes
    img_bytes = img_buffer.getvalue()

    # Create a download link for the framed image
    st.markdown(get_binary_file_downloader_html(img_bytes, 'framed_image.png', 'Download Framed Image'), unsafe_allow_html=True)

def get_binary_file_downloader_html(bin_file, file_label='File', button_label='Download'):
    with io.BytesIO(bin_file) as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">{button_label}</a>'
    return href

if __name__ == "__main__":
    main()
