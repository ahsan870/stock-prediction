import streamlit as st
import random

compliments = [
    "Do not marry Sylhety, you have to cut fish.",
    "You're not just a friend; you're a frienemy, and that's special.",
    "If laughter is the best medicine, you're the pharmacy.",
    "You're like a fine wine. The older you get, the more you make everyone else feel good.",
    "I'm not saying you're old, but if you were a dinosaur, you'd be a 'Saur not found.'",
    "You're so awesome that I named a star after you. It's probably a black hole, though.",
]

def generate_compliment():
    return random.choice(compliments)

def main():
    st.markdown(
        "<h1 style='text-align: center; color: red; font-size: 36px;'>It's for you, Dasnim!</h1>",
        unsafe_allow_html=True,
    )
    st.title("Sweet Compliment Generator")

    # Display the compliment
    compliment = st.empty()

    # Button to generate a new compliment
    if st.button("Generate Compliment"):
        new_compliment = generate_compliment()
        compliment.markdown(f"<h2 style='color: #0066cc;'>{new_compliment}</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

