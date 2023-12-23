import streamlit as st
import time

def birthday_card():
    st.title("Happy Birthday!")
    # Style the text
    st.markdown(
        "<h2 style='text-align: center; color: #FF69B4;'>Wishing you a fantastic birthday filled with joy and laughter!</h2>",
        unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px;'>🎉🎂🎁</p>", unsafe_allow_html=True)
    # Button to toggle the birthday card
    if st.button("Toggle Birthday Card"):
        st.session_state.show_card = not st.session_state.get("show_card", False)

        # Add some animation when showing the card
        if st.session_state.show_card:
            st.balloons()

    # Display the birthday card if the button is clicked
    if st.session_state.get("show_card", False):
        # Replace "IMAGE_URL" with the actual URL of the image you want to use
        image_url = "images/black-birthday-with-balloonsCard.png"
        st.image(image_url, caption="Celebration Time", use_column_width=True)
if __name__ == "__main__":
    birthday_card()
