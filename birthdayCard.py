import streamlit as st
import time


def birthday_card():
    st.set_page_config(page_title="Birthday Celebration", layout="centered")

    # Predefined name
    birthday_person = "Tasnim Haq"

    # Title
    st.title(f"🎉 Happy Birthday, {birthday_person}! 🎂")

    # Styling
    st.markdown(
        """
        <style>
        body {
            background-color: #fff0f5;
        }
        h1, h2 {
            text-align: center;
        }
        .custom-text {
            color: #FF69B4;
            text-align: center;
            font-size: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Fun message
    st.markdown(
        f"<h2 class='custom-text'>Wishing you all the happiness in the world on your special day, {birthday_person}!</h2>",
        unsafe_allow_html=True
    )
    st.markdown("<p style='text-align: center; font-size: 20px;'>🎈🎁🎉</p>", unsafe_allow_html=True)

    # Button to toggle the birthday card
    if st.button(f"🎁 Open Your Card, {birthday_person}!"):
        st.session_state.show_card = not st.session_state.get("show_card", False)

        # Add festive animation
        if st.session_state.show_card:
            st.balloons()
            st.snow()

    # Display the birthday card if the button is clicked
    if st.session_state.get("show_card", False):
        image_url = "images/balloonsCard.png"
        st.image(image_url, caption=f"🎉 Let's Celebrate, {birthday_person}!", use_container_width=True)

        # Add a predefined birthday message with a funny twist
        st.write(
            f"🎉 {birthday_person}, you're another year older, but don't worry... you're still younger than you'll be next year!")
        st.write(
            f"Also, remember, {birthday_person}, age is just a number... but in your case, it’s a really big one! 😂")

    # Optional: Add a funny quote or meme
    st.markdown(
        """
        <p style='text-align: center; font-size: 18px;'>Here's a funny quote to make you smile:</p>
        <p style='text-align: center; font-size: 18px;'>"You're not getting older, you're just becoming a classic!"</p>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    birthday_card()
