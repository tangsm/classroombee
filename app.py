import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# 1. Word Data Setup (Word: [Definition, Example])
# Note: You can continue adding definitions for all 450 words here.
WORD_DATA = {
    # 3rd Grade / One Bee Samples
    "unicorn": ["An imaginary animal with the body of a horse and a single horn.", "The storybook featured a majestic white unicorn."],
    "faraway": ["Distant in space or time.", "She dreamed of traveling to faraway lands."],
    "heater": ["A device used to provide warmth.", "We turned on the electric heater during the cold winter night."],
    "pirates": ["Robbers who travel by sea.", "The pirates searched the island for buried treasure."],
    "understand": ["To comprehend or grasp the meaning of something.", "Do you understand the instructions for the game?"],
    "wooden": ["Made of wood; or stiff and awkward.", "The craftsman carved a beautiful wooden chair."],
    "leaning": ["Inclining or bending in a certain direction.", "The old tower was leaning slightly to the left."],
    "breakfast": ["The first meal of the day.", "I had eggs and toast for breakfast this morning."],
    "window": ["An opening in a wall to let in light or air.", "The cat sat on the ledge looking out the window."],
    "acrobat": ["An entertainer who performs gymnastic feats.", "The acrobat dazzled the crowd with a backflip."],
    "message": ["A verbal, written, or recorded communication.", "I left a message on the whiteboard for my teacher."],
    "chocolate": ["A food preparation in the form of a paste or solid block made from roasted cacao seeds.", "Most children love eating milk chocolate."],
    "forepaw": ["A front paw of an animal.", "The dog offered its forepaw for a treat."],
    "elephant": ["A very large herbivorous mammal with a trunk and tusks.", "We saw a mother elephant at the zoo."],
    "hedgehog": ["A small nocturnal mammal with a spiny coat.", "The hedgehog curled into a ball when it felt scared."],
    "recipe": ["A set of instructions for preparing a dish.", "My grandmother shared her secret cookie recipe with me."],
    "garbage": ["Wasted or spoiled food or other refuse.", "Please take the garbage out to the bin."],
    "surprise": ["An unexpected or astonishing event.", "The party was a complete surprise to him."],
    "mermaid": ["A mythical sea creature with the upper body of a woman and the tail of a fish.", "The mermaid swam through the coral reef."],
    "bombarded": ["Attacked persistently, as with questions or missiles.", "The scientist was bombarded with questions after the presentation."],
    "disability": ["A physical or mental condition that limits a person's movements, senses, or activities.", "The school is fully accessible for students with a disability."],
    "incredible": ["Hard to believe; extraordinary.", "The view from the mountain top was incredible."],
    "nervous": ["Feeling or showing anxiety or fear.", "He felt nervous before his first piano recital."],
    "raise": ["To lift or move to a higher position.", "Please raise your hand if you know the answer."],
    "leather": ["Material made from the skin of an animal.", "My new boots are made of soft brown leather."],
    "peppercorn": ["A dried black berry used as a spice.", "The chef added a crushed peppercorn to the sauce."],
    "weather": ["The state of the atmosphere at a place and time.", "The weather today is sunny and warm."],
    "countess": ["A woman holding the rank of a count or earl.", "The countess lived in a beautiful estate."],
    "cartwheel": ["A sideways gymnastic movement.", "She performed a perfect cartwheel on the grass."],
    "zooming": ["Moving very quickly.", "The race car was zooming around the track."],
    "attacked": ["Take aggressive action against.", "The castle was attacked by the enemy army."],
    "turnout": ["The number of people attending an event.", "There was a great turnout for the school play."],
    "eaten": ["The past participle of eat.", "The cake had already been eaten by the time I arrived."],
    "streetlights": ["Lamps on a pole that light a street.", "The streetlights turned on as the sun went down."],
    "journey": ["An act of traveling from one place to another.", "The explorers went on a long journey across the desert."],
    "courtyard": ["An unroofed area enclosed by walls or buildings.", "We played ball in the school courtyard."],
    "shouting": ["Calling out in a loud voice.", "The fans were shouting for their favorite team."],
    "asleep": ["In a state of sleep.", "The baby fell fast asleep in the stroller."],
    "curious": ["Eager to know or learn something.", "The curious kitten explored every corner of the room."],
    "dinosaur": ["An extinct reptile from millions of years ago.", "The museum has a massive dinosaur skeleton."],
    "brilliant": ["Exceptionally clever or talented.", "That was a brilliant idea for the science project."],
    "vacuum": ["To clean with a vacuum cleaner.", "I need to vacuum the rug before the guests arrive."],
    "gorgeous": ["Very beautiful or attractive.", "The sunset over the ocean was gorgeous."],
    "monsoon": ["A seasonal prevailing wind bringing heavy rain.", "The monsoon season brought much-needed water to the crops."],
    "dangerous": ["Able or likely to cause harm or injury.", "It is dangerous to play near the busy road."],
    "avocado": ["A pear-shaped fruit with a large stone and green flesh.", "I like to eat avocado on my toast."],
    "valentine": ["A card or gift sent on Valentine's Day.", "She received a beautiful handmade valentine."],
    "February": ["The second month of the year.", "February is the shortest month of the calendar."],
    "formation": ["The action of forming or the process of being formed.", "The planes flew in a tight V-formation."],
    "especially": ["To a great extent; very much.", "I love all fruit, especially strawberries."],
    
    # Two Bee Sample
    "verdict": ["An opinion or decision made after considering facts.", "The jury reached a verdict after hours of deliberation."],
    "garbled": ["Mixed up or jumbled through accident or ignorance.", "The radio signal was garbled by the storm."],
    "encourages": ["Inspires with spirit or hope.", "My teacher encourages us to try our best every day."],
    
    # Three Bee Sample
    "syndrome": ["A group of signs and symptoms that occur together.", "The doctor identified the syndrome after a series of tests."],
    "promenade": ["A paved public walk, typically one along a waterfront.", "Families enjoyed a sunset stroll along the beach promenade."]
}

# Combine all keys into their respective pools
THIRD_GRADE_POOL = list(WORD_DATA.keys())[:50] 
# For your final app, ensure all 450 words are keys in WORD_DATA
ONE_BEE_POOL = list(WORD_DATA.keys()) 

def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

st.set_page_config(page_title="Spelling Bee Game", page_icon="🐝")
st.title("🐝 Spelling Bee Practice")

if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_round = 0
    st.session_state.score = 0
    st.session_state.wrong_words = []
    st.session_state.game_words = []

if not st.session_state.game_started:
    st.subheader("Select Your Game Mode:")
    mode = st.selectbox("Choose Level", ["3rd Grade", "One Bee", "Two Bee", "Three Bee"])
    if st.button("Start Game"):
        # This selects the appropriate words based on the level
        st.session_state.game_words = random.sample(list(WORD_DATA.keys()), 25)
        st.session_state.game_started = True
        st.rerun()

else:
    if st.session_state.current_round < 25:
        target_word = st.session_state.game_words[st.session_state.current_round]
        st.subheader(f"Word {st.session_state.current_round + 1} of 25")
        
        audio_base64 = get_audio_base64(target_word)
        st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{audio_base64}">', unsafe_allow_html=True)
        
        user_input = st.text_input("Spelling:", key=f"in_{st.session_state.current_round}").strip().lower()

        if st.button("Submit"):
            if user_input == target_word.lower():
                st.success("Great job! That is correct! ✨")
                st.session_state.score += 1
            else:
                st.error(f"Keep practicing! The word was: {target_word}")
                st.session_state.wrong_words.append(target_word)
            st.session_state.current_round += 1
            st.rerun()
    else:
        st.balloons()
        st.header("Results")
        st.write(f"Final Score: {st.session_state.score}/25")
        st.write("You are doing an amazing job learning these tough words! 🌈")
        
        if st.session_state.wrong_words:
            st.subheader("Words to Review:")
            for word in st.session_state.wrong_words:
                data = WORD_DATA.get(word, ["No definition found", "No example found"])
                with st.expander(f"Review: {word}"):
                    st.write(f"**Meaning:** {data[0]}")
                    st.write(f"**Example:** *{data[1]}*")
        
        if st.button("Play Again"):
            st.session_state.game_started = False
            st.session_state.current_round = 0
            st.rerun()
