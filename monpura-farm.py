import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Load the predefined farm logo

logo_path = "images/logo1.png"  # Path to your predefined logo file
logo = Image.open(logo_path)

# Convert logo to RGBA mode to handle transparency
logo = logo.convert("RGBA")

# Streamlit app title
st.title("Animal Farm Image Customizer")

# Upload animal image
uploaded_file = st.file_uploader("Upload an image of the animal", type=["jpg", "jpeg", "png"])

# Inputs for price, weight, and tag
price = st.text_input("Enter the price")
weight = st.text_input("Enter the weight (in kg)")
tag = st.text_input("Enter the animal tag")

if uploaded_file:
    # Open uploaded image
    image = Image.open(uploaded_file)

    if price and weight and tag:
        # Resize the logo to fill the bottom width of the image
        logo_width = image.width  # Make the logo as wide as the image
        logo_ratio = logo.width / logo.height
        logo_height = int(logo_width / logo_ratio)
        logo = logo.resize((logo_width, logo_height))

        # Create space for the logo and text at the bottom of the image
        total_height = image.height + logo.height + 100  # Adding 100px for text space
        new_image = Image.new("RGBA", (image.width, total_height), (255, 255, 255, 255))
        new_image.paste(image, (0, 0))

        # Paste the logo onto the bottom-left corner of the new image
        new_image.paste(logo, (0, image.height), logo)

        # Draw text (price, weight, tag) under the logo
        draw = ImageDraw.Draw(new_image)

        # Define font size and load a TTF font
        font_size = 40
        font = ImageFont.truetype("arial.ttf", font_size)  # Use a TTF font like Arial

        # Define the text content
        text = f"Price: {price}\nWeight: {weight} kg\nTag: {tag}"

        # Get the text size and draw background rectangle
        bbox = draw.textbbox((0, 0), text, font=font)  # Get bounding box
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]  # Calculate text width and height

        # Draw a rectangle as background for the text
        background_color = (255, 255, 255, 255)  # White background
        draw.rectangle(
            [0, image.height + logo.height, image.width, image.height + logo.height + text_height + 20],
            fill=background_color
        )

        # Draw the text on top of the background
        draw.text((10, image.height + logo.height + 10), text, font=font, fill="black")

        # Display the final image with the logo and text
        st.image(new_image, caption="Customized Animal Image", use_column_width=True)

        # Option to download the modified image
        img_name = f"{tag}_customized_image.png"
        new_image.save(img_name)
        with open(img_name, "rb") as img_file:
            st.download_button(label="Download Image", data=img_file, file_name=img_name, mime="image/png")
    else:
        st.warning("Please provide price, weight, and tag for the animal.")
