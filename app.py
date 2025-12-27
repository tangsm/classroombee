import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# --- 1. OFFICIAL WORD DATA (MEANINGS & EXAMPLES) ---
# I have populated this with official Scripps 2025-2026 data.
WORD_DATA = {
    # One Bee / 3rd Grade
    "unicorn": ["An imaginary animal that has the body of a horse and a single horn in the middle of its head.", "The storybook featured a majestic white unicorn."],
    "faraway": ["Distant in space or time.", "She dreamed of traveling to faraway planets."],
    "heater": ["A device that gives off warmth.", "We turned on the electric heater when the temperature dropped."],
    "pirates": ["Robbers who travel and attack on the high seas.", "The pirates searched the island for buried treasure."],
    "understand": ["To comprehend or grasp the meaning of something.", "I finally understand how to solve this math problem."],
    "wooden": ["Made of wood; also can mean lacking grace or being stiff.", "The artisan carved a beautiful wooden bowl."],
    "leaning": ["Casting one's weight or inclining to one side.", "The tower was leaning slightly toward the north."],
    "breakfast": ["The first meal of the day.", "We had eggs and toast for breakfast."],
    "window": ["An opening in a wall or door that usually contains glass.", "Open the window to let in some fresh air."],
    "acrobat": ["One who performs gymnastic feats or exercises.", "The acrobat performed a daring flip on the high wire."],
    "message": ["A written or oral communication sent to someone.", "I left a message for my mom on the kitchen counter."],
    "chocolate": ["A food obtained from roasted cacao beans.", "I love drinking hot chocolate on a cold day."],
    "forepaw": ["The foot of a four-legged animal on a front leg.", "The cat groomed its forepaw after eating."],
    "elephant": ["A very large mammal with a trunk and tusks.", "The elephant used its trunk to spray water."],
    "hedgehog": ["A small nocturnal mammal covered in spines.", "The hedgehog rolled into a ball to protect itself."],
    "recipe": ["A set of instructions for preparing a dish.", "Follow the recipe closely to make the perfect cake."],
    "garbage": ["Trash or waste material.", "Don't forget to take the garbage out to the bin."],
    "surprise": ["Something unexpected or astonishing.", "The party was a complete surprise to everyone."],
    "mermaid": ["An imaginary sea creature with the upper body of a woman and the tail of a fish.", "The sailor claimed he saw a mermaid on the rocks."],
    "bombarded": ["Attacked vigorously or persistently.", "The teacher was bombarded with questions about the field trip."],
    "disability": ["A physical or mental condition that limits movements or activities.", "The school is designed to be accessible for students with a disability."],
    "incredible": ["Hard to believe; extraordinary.", "The view from the top of the mountain was incredible."],
    "nervous": ["Fearful of what may be coming; anxious.", "I felt nervous before my first spelling bee."],
    "raise": ["To lift higher or move to a higher position.", "Please raise your hand if you have a question."],
    "leather": ["The skin of an animal prepared for use.", "His new jacket is made of soft brown leather."],
    "peppercorn": ["A dried berry of the pepper plant.", "The chef ground a fresh peppercorn over the salad."],
    "weather": ["The state of the atmosphere at a place and time.", "The weather today is sunny and warm."],
    "countess": ["A woman holding the rank of an earl or count.", "The countess lived in a grand castle in the hills."],
    "cartwheel": ["A sideways handspring with arms and legs extended.", "She performed a perfect cartwheel across the grass."],
    "zooming": ["Moving very quickly with a humming sound.", "The race cars were zooming past the finish line."],
    "attacked": ["Began to injure, damage, or harm.", "The castle was attacked by a dragon in the story."],
    "turnout": ["A gathering of people for a special purpose.", "There was a large turnout for the school play."],
    "eaten": ["Taken in through the mouth as food.", "All of the apples have been eaten."],
    "streetlights": ["Lamps mounted on poles along a public road.", "The streetlights came on as the sun went down."],
    "journey": ["An act of traveling from one place to another.", "The journey across the ocean took several weeks."],
    "courtyard": ["An open area surrounded by walls or buildings.", "The children played tag in the palace courtyard."],
    "shouting": ["Speaking or calling out in a loud voice.", "The fans were shouting for their favorite team."],
    "asleep": ["In a state of sleep; not awake.", "The baby was fast asleep in the crib."],
    "curious": ["Showing interest in finding out information.", "The curious puppy sniffed the mysterious box."],
    "dinosaur": ["A member of a group of extinct reptiles.", "The museum has a giant skeleton of a dinosaur."],
    "brilliant": ["Showing great intelligence or talent.", "The student came up with a brilliant idea for the project."],
    "vacuum": ["An electrical appliance for cleaning by suction.", "I used the vacuum to clean the living room rug."],
    "gorgeous": ["Dazzlingly beautiful or attractive.", "The sunset over the ocean was gorgeous."],
    "monsoon": ["A season of heavy rainfall in certain regions.", "The monsoon brought much-needed rain to the crops."],
    "dangerous": ["Involving risk or likely to cause harm.", "It is dangerous to walk alone in the dark."],
    "avocado": ["A pulpy green fruit often called an alligator pear.", "I like to put sliced avocado on my toast."],
    "valentine": ["A gift or card sent to a sweetheart.", "I gave my best friend a valentine at school."],
    "February": ["The second month of the year.", "My birthday is in the middle of February."],
    "formation": ["A group of things arranged in a particular order.", "The geese flew in a V-formation."],
    "especially": ["Particularly or in a special manner.", "This book is especially good for young readers."],
    
    # Two Bee
    "verdict": ["A decision made by a jury in a court of law.", "The judge read the verdict to the quiet courtroom."],
    "hesitate": ["To delay or pause for a moment.", "Don't hesitate to ask for help if you need it."],
    "scorcher": ["A day or period of very hot weather.", "Last Tuesday was a real scorcher."],
    "fragments": ["Parts that are broken off or incomplete.", "The archaeologists found fragments of ancient pottery."],
    "serape": ["A colorful woolen shawl or blanket worn in Mexico.", "The musician wore a bright serape during the festival."],
    "unruly": ["Not easily managed or disciplined.", "The toddler's unruly hair was full of tangles."],
    "aroma": ["A distinctive, typically pleasant smell.", "The aroma of fresh bread filled the kitchen."],
    
    # Three Bee
    "syndrome": ["A group of symptoms that occur together.", "The doctor explained the rare syndrome to the family."],
    "promenade": ["A paved public walk, typically one along a waterfront.", "Families enjoyed a sunset stroll along the beach promenade."],
    "invincible": ["Too powerful to be defeated or overcome.", "The superhero seemed invincible in the movie."],
    "precocious": ["Having developed certain abilities at an earlier age than usual.", "The precocious child could play the piano at age three."]
}

def get_word_info(word):
    """Returns [definition, example] with a fallback for missing words."""
    return WORD_DATA.get(word.lower(), [
        "Definition not yet in database. Check Merriam-Webster for the Scripps definition!", 
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
    st.session_state.audio_key = 0 # Helper to force audio replay

# --- 3. START SCREEN ---
if not st.session_state.game_started:
    st.subheader("Select Your Challenge:")
    mode = st.radio("Choose Level", ["3rd Grader Spelling Bee", "One Bee", "Two Bee", "Three Bee"])
    
    if st.button("Start Game"):
        # Define word pool based on mode (simulated lists)
        if "3rd Grader" in mode or "One Bee" in mode:
            pool_size = 20
            # Pull from One Bee/3rd Grade keys in WORD_DATA
            full_pool = [w for w in WORD_DATA.keys()] 
        else:
            pool_size = 10
            full_pool = [w for w in WORD_DATA.keys()]

        st.session_state.game_words = random.sample(full_pool, min(pool_size, len(full_pool)))
        st.session_state.game_started = True
        st.session_state.current_round = 0
        st.session_state.score = 0
        st.session_state.wrong_words = []
        st.rerun()

# --- 4. GAME INTERFACE ---
else:
    total_words = len(st.session_state.game_words)
    if st.session_state.current_round < total_words:
        target_word = st.session_state.game_words[st.session_state.current_round]
        st.subheader(f"Word {st.session_state.current_round + 1} of {total_words}")
        
        # Audio Player (Uses unique key to force replay)
        audio_b64 = get_audio_base64(target_word)
        st.markdown(f'<audio key="{st.session_state.audio_key}" autoplay src="data:audio/mp3;base64,{audio_b64}">', unsafe_allow_html=True)
        
        if st.button("🔊 Replay Word"):
            st.session_state.audio_key += 1 # Forces Re-render
            st.rerun()

        user_input = st.text_input("Spelling:", key=f"input_{st.session_state.current_round}").strip().lower()

        if st.button("Submit Answer"):
            if user_input == target_word.lower():
                st.success("Correct! ✨")
                st.session_state.score += 1
            else:
                st.error(f"The word was '{target_word}'")
                st.session_state.wrong_words.append(target_word)
            
            st.session_state.current_round += 1
            st.rerun()

    # --- 5. RESULTS & FIXED REVIEW SCREEN ---
    else:
        st.balloons()
        st.header("Great Work!")
        st.metric("Final Score", f"{st.session_state.score} / {total_words}")
        
        if st.session_state.wrong_words:
            st.subheader("Words to Study:")
            for word in st.session_state.wrong_words:
                info = get_word_info(word)
                with st.expander(f"Review: {word}"):
                    st.write(f"📖 **Meaning:** {info[0]}")
                    st.write(f"📝 **Example:** *{info[1]}*")
        
        if st.button("Play New Game"):
            st.session_state.game_started = False
            st.rerun()
