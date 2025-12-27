import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# --- 1. WORD DATA SOURCE ---
# Ideally, these would be in a JSON file. For now, here is a robust structure.
# I have included a helper to ensure every word gets a definition/example.
WORD_DATA = {
    "unicorn": ["A mythical horse with a single horn.", "The unicorn jumped over the rainbow."],
    "faraway": ["At a great distance.", "She dreamed of visiting faraway planets."],
    "heater": ["A device used to warm a room.", "We turned on the heater when it started to snow."],
    "verdict": ["A decision made by a jury in a court.", "The judge read the verdict to the quiet room."],
    "syndrome": ["A group of symptoms that occur together.", "The doctor explained the rare syndrome to the family."],
    "aberration": ["Something that differs from the norm.", "The cold day in July was a weather aberration."]
    # ... Add others as needed. If a word is missing, the code below handles it gracefully.
}

def get_word_info(word):
    """Returns [definition, example] or generic ones if word is missing from dictionary."""
    return WORD_DATA.get(word.lower(), [
        "Definition not found in database.", 
        "Keep practicing this word to master it!"
    ])

# --- 2. AUDIO HELPER (Fixed for Replay) ---
def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

st.set_page_config(page_title="Spelling Bee Pro", page_icon="🐝")
st.title("🐝 Spelling Bee Master")

# Initialize Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_round = 0
    st.session_state.score = 0
    st.session_state.wrong_words = []
    st.session_state.game_words = []
    st.session_state.replay_id = 0 # Helper for the Replay button

# --- 3. START SCREEN ---
if not st.session_state.game_started:
    st.subheader("Select Your Challenge:")
    mode = st.selectbox("Choose Level", ["3rd Grade", "One Bee", "Two Bee", "Three Bee"])
    if st.button("Start Game"):
        # Logic to pull 25 random words (Simulated here with a sample list)
        # In your full version, replace with the lists from your PDF
        full_pool = ["unicorn", "faraway", "heater", "verdict", "syndrome", "aberration"] * 10 
        st.session_state.game_words = random.sample(full_pool, 25)
        st.session_state.game_started = True
        st.rerun()

# --- 4. GAME INTERFACE ---
else:
    if st.session_state.current_round < 25:
        target_word = st.session_state.game_words[st.session_state.current_round]
        st.subheader(f"Word {st.session_state.current_round + 1} of 25")
        
        # FIX FOR ISSUE #2: Replay Word
        # Adding a unique key to the audio HTML forces the browser to play it again
        audio_b64 = get_audio_base64(target_word)
        audio_tag = f'<audio key="{st.session_state.replay_id}" autoplay src="data:audio/mp3;base64,{audio_b64}">'
        st.markdown(audio_tag, unsafe_allow_html=True)
        
        if st.button("🔊 Replay Word"):
            st.session_state.replay_id += 1 # Change the ID to force replay
            st.rerun()

        user_input = st.text_input("Type the word:", key=f"input_{st.session_state.current_round}").strip().lower()

        if st.button("Submit Answer"):
            if user_input == target_word.lower():
                st.success("Correct! You are brilliant! ✨")
                st.session_state.score += 1
            else:
                st.error(f"Not quite! The word was '{target_word}'")
                st.session_state.wrong_words.append(target_word)
            
            st.session_state.current_round += 1
            st.rerun()

    # --- 5. RESULTS SCREEN (FIX FOR ISSUE #1) ---
    else:
        st.balloons()
        st.header("Great Work!")
        st.metric("Final Score", f"{st.session_state.score} / 25")
        
        st.write("Keep going! Every mistake is just a step toward becoming a spelling pro! 🌈")
        
        if st.session_state.wrong_words:
            st.subheader("Words to Study:")
            for word in st.session_state.wrong_words:
                info = get_word_info(word) # Fetch definition and example
                with st.expander(f"Review: {word}"):
                    st.write(f"📖 **Meaning:** {info[0]}")
                    st.write(f"📝 **Example Use:** *{info[1]}*")
        
        if st.button("Play New Game"):
            st.session_state.game_started = False
            st.session_state.current_round = 0
            st.rerun()
