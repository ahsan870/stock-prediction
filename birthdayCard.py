import streamlit as st

def birthday_card():
    st.title("Happy Birthday!")

    # Button to reveal the birthday card
    if st.button("Open Birthday Card"):
        # Replace "IMAGE_URL" with the actual URL of the image you want to use
        image_url = "birthdatcard.jpg"
        st.image(image_url, caption="Celebration Time", use_column_width=True)
        st.write("Wishing you a fantastic birthday filled with joy and laughter!")
        st.write("🎉🎂🎁")

if __name__ == "__main__":
    birthday_card()

