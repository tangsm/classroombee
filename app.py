import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# 1. Word List Setup
WORDS = [
    "unicorn", "faraway", "heater", "pirates", "understand", "wooden", "leaning", 
    "breakfast", "window", "acrobat", "message", "chocolate", "forepaw", "elephant", 
    "hedgehog", "recipe", "garbage", "surprise", "mermaid", "bombarded", "disability", 
    "incredible", "nervous", "raise", "leather", "peppercorn", "weather", "countess", 
    "cartwheel", "zooming", "attacked", "turnout", "eaten", "streetlights", "journey", 
    "courtyard", "shouting", "asleep", "curious", "dinosaur", "brilliant", "vacuum", 
    "gorgeous", "monsoon", "dangerous", "avocado", "valentine", "February", "formation", "especially"
]

def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

st.set_page_config(page_title="3rd Grade Spelling Bee", page_icon="🐝")
st.title("🐝 3rd Grade Spelling Bee")

# Initialize Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_round = 0
    st.session_state.score = 0
    st.session_state.wrong_words = []
    st.session_state.game_words = []

# Start Game
if not st.session_state.game_started:
    st.write("Welcome! Are you ready to practice your spelling?")
    if st.button("Start Game (25 Random Words)"):
        st.session_state.game_words = random.sample(WORDS, 25)
        st.session_state.game_started = True
        st.session_state.current_round = 0
        st.session_state.score = 0
        st.session_state.wrong_words = []
        st.rerun()

# Game Interface
else:
    if st.session_state.current_round < 25:
        target_word = st.session_state.game_words[st.session_state.current_round]
        
        st.subheader(f"Word {st.session_state.current_round + 1} of 25")
        
        # Audio Playback
        audio_base64 = get_audio_base64(target_word)
        audio_html = f'<audio autoplay src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_html, unsafe_allow_html=True)
        
        if st.button("🔊 Replay Word"):
            st.rerun()

        user_input = st.text_input("Type the word here:", key=f"input_{st.session_state.current_round}").strip().lower()

        if st.button("Submit"):
            if user_input == target_word.lower():
                st.success("Correct! Great job!")
                st.session_state.score += 1
            else:
                st.error(f"Not quite! The correct spelling was: {target_word}")
                st.session_state.wrong_words.append(target_word)
            
            st.session_state.current_round += 1
            st.rerun()
    
    # End Results
    else:
        st.balloons()
        st.header("🎉 Game Over!")
        st.write(f"Your Final Score: **{st.session_state.score} / 25**")
        
        # Encouraging messages
        if st.session_state.score == 25:
            st.write("🌟 Absolutely Incredible! You are a Spelling Master!")
        elif st.session_state.score > 20:
            st.write("✨ Fantastic effort! You're doing amazing!")
        else:
            st.write("🌈 Great practice! Keep it up and you'll be a pro in no time!")

        if st.session_state.wrong_words:
            if st.checkbox("Show words to review"):
                st.write("Here are the words to practice:")
                for word in st.session_state.wrong_words:
                    st.write(f"- {word}")
        
        if st.button("Play Again"):
            st.session_state.game_started = False
            st.rerun()
