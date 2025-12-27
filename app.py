import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# 1. Word List Setup
THIRD_GRADE_WORDS = [
    "unicorn", "faraway", "heater", "pirates", "understand", "wooden", "leaning", 
    "breakfast", "window", "acrobat", "message", "chocolate", "forepaw", "elephant", 
    "hedgehog", "recipe", "garbage", "surprise", "mermaid", "bombarded", "disability", 
    "incredible", "nervous", "raise", "leather", "peppercorn", "weather", "countess", 
    "cartwheel", "zooming", "attacked", "turnout", "eaten", "streetlights", "journey", 
    "courtyard", "shouting", "asleep", "curious", "dinosaur", "brilliant", "vacuum", 
    "gorgeous", "monsoon", "dangerous", "avocado", "valentine", "February", "formation", "especially"
]

ONE_BEE = [
    "tag", "twigs", "insects", "moment", "send", "taffy", "teeth", "ajar", "deck", "comfy", "shortcut", "basil",
    "stuck", "stretch", "bait", "triple", "snug", "tight", "lure", "satin", "fish", "candy", "cluster", "ahoy",
    "hold", "scrunch", "forest", "signal", "mind", "ruby", "hollow", "answer", "stay", "close", "spinning", "shuffle",
    "scrub", "tackle", "baffling", "dollop", "draw", "wire", "sizzling", "minnows", "brown", "skater", "hoist", "silver",
    "cozy", "giant", "search", "before", "bucket", "remind", "circus", "tint", "chance", "mango", "writing", "milk",
    "baskets", "coral", "kitchen", "yawn", "tender", "jangle", "sugar", "tank", "paste", "shimmer", "awkward", "want",
    "melon", "blossoms", "seep", "crowd", "farmer", "swampy", "sweet", "pond", "parent", "studded", "wheels", "skirt",
    "tail", "focus", "faint", "sharks", "hockey", "distress", "fruit", "quilt", "slime", "lessons", "roam", "goats",
    "disability", "avocado", "woozy", "incredible", "valentine", "limbs", "leather", "February", "ahead", "countess",
    "formation", "señor", "nervous", "especially", "unicorn", "peppercorn", "faraway", "cartwheel", "heater", "raise",
    "pirates", "weather", "understand", "zooming", "wooden", "attacked", "leaning", "turnout", "breakfast", "eaten",
    "window", "streetlights", "acrobat", "journey", "chocolate", "message", "courtyard", "shouting", "forepaw", "asleep",
    "elephant", "curious", "hedgehog", "dinosaur", "recipe", "brilliant", "garbage", "vacuum", "surprise", "gorgeous",
    "mermaid", "monsoon", "bombarded", "dangerous"
]

TWO_BEE = [
    "hesitate", "Buffalo", "dubious", "dissolving", "scorcher", "sequins", "ebony", "nomad", "scavenger", "fragments",
    "gallop", "fabulous", "foreign", "billowed", "paltry", "skewer", "deflated", "lanky", "verdict", "Berlin", "unleash",
    "fluently", "garbled", "lunacy", "ration", "mysterious", "encourages", "conjure", "cosmetics", "brandished",
    "imitation", "bracken", "crawdad", "sardines", "miniature", "noggin", "frustration", "anguish", "receptionist",
    "neon", "unruly", "conical", "preamble", "rakish", "mascot", "rickety", "plausible", "hypnosis", "aroma", "lilt",
    "reprimanding", "rotunda", "moustache", "pediatric", "commotion", "gusto", "porridge", "oblivion", "toiletries",
    "artifacts", "democracy", "immigrants", "gleaned", "rummage", "steeple", "jeered", "perfume", "beige", "spectators",
    "winsome", "sinister", "ancestral", "lanyards", "prattling", "tuxedo", "grimace", "suspicious", "galore", "discoveries",
    "gaunt", "parchment", "emporium", "lurches", "enormous", "ramshackle", "atrium", "language", "geranium", "fugitive",
    "eccentric", "prognosis", "nautical", "heron", "savant", "almanac", "talcum", "hippies", "samosas", "tranquilizer",
    "equestrian", "chignon", "pheromone", "campaign", "plaited", "galleon", "magnanimous", "pistachio", "monsieur",
    "chartreuse", "mosque", "manticores", "wainscoting", "zombielike", "prestigious", "Nehru", "warlock", "fraidycat",
    "colossus", "guttural", "convulsively", "lo mein", "dimensional", "courier", "garishly", "sans serif", "graffitist",
    "psyche", "Everest", "stucco", "dexterity", "Frankenstein", "cavorting", "schema", "marauder", "et cetera", "conscience",
    "vidimus", "battlements", "delphine", "deferential", "slough", "albatross", "archipelago", "khaki", "serape",
    "opalescent", "asphalt", "puissance", "Yiddish", "pinioning"
]

THREE_BEE = [
    "gangly", "comrades", "ultimatum", "swaggering", "sporadic", "whinnying", "prototype", "cravenly", "chimneys",
    "promenade", "squalor", "mulberry", "riveted", "repugnant", "memoirs", "hypocritical", "plaid", "invincible",
    "cylinders", "chlorine", "dirge", "renowned", "ominous", "traumatic", "zeal", "parachute", "muffler", "receipts",
    "whittled", "laborious", "syndrome", "solemnly", "depots", "appointment", "premises", "begrudge", "fiberglass",
    "foreseeable", "safari", "contentious", "salvaged", "ratify", "lasagna", "precocious", "fissures", "scalpel",
    "substantially", "ensemble", "enthusiastic", "reclusive", "mercantile", "cadre", "discipline", "compassionate",
    "formidable", "lye", "unfamiliar", "bulletin", "propaganda", "belfry", "scurrying", "alfalfa", "marquee", "lacrosse",
    "dignitaries", "officially", "proficient", "sluice", "pizzeria", "crematorium", "compunction", "cajolery", "dismissal",
    "bayonet", "emphatically", "vigilance", "skittish", "amicable", "hyperventilated", "residuals", "careened", "exuberant",
    "ostracism", "boutique", "nomination", "beautician", "onslaught", "peroxide", "opportunist", "equations", "ruefully",
    "aristocracy", "dictatorship", "assignment", "misanthrope", "apocalypse", "tuberculosis", "patriarchs", "boll weevil",
    "barricade", "chandelier", "camphor", "confreres", "dulce", "Tucson", "Oswego", "diphtheria", "baklava", "anonymously",
    "concierge", "paparazzi", "corbels", "unparalleled", "latticework", "pumpernickel", "trebuchets", "barrette", "hibiscus",
    "pogrom", "Kilimanjaro", "chassis", "tamale", "bursitis", "fräulein", "junket", "maracas", "pâtisserie", "protégé",
    "quandary", "gyroplane", "cycads", "hors d'oeuvres", "Erie", "burpees", "sarsaparilla", "maquisards", "gingham",
    "Adriatic", "maître d'", "Aubusson", "silhouette", "piccolo", "cannelloni", "Charolais", "auxiliary", "au revoir",
    "boulangerie", "thesaurus", "tulle", "bronchitis"
]

def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

st.set_page_config(page_title="School Spelling Bee", page_icon="🐝")
st.title("🐝 Spelling Bee Game")

# Initialize Session State
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_round = 0
    st.session_state.score = 0
    st.session_state.wrong_words = []
    st.session_state.game_words = []

# Game Mode Selection
if not st.session_state.game_started:
    st.subheader("Select Your Game Mode:")
    game_mode = st.radio("Choose a level:", ["3rd Grade Spelling Bee", "School Spelling Bee: One Bee", "School Spelling Bee: Two Bee", "School Spelling Bee: Three Bee"])
    
    if st.button("Start Game"):
        if game_mode == "3rd Grade Spelling Bee":
            pool = THIRD_GRADE_WORDS
        elif game_mode == "School Spelling Bee: One Bee":
            pool = ONE_BEE
        elif game_mode == "School Spelling Bee: Two Bee":
            pool = TWO_BEE
        else:
            pool = THREE_BEE
            
        st.session_state.game_words = random.sample(pool, 25)
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
        
        audio_base64 = get_audio_base64(target_word)
        audio_html = f'<audio autoplay src="data:audio/mp3;base64,{audio_base64}">'
        st.markdown(audio_html, unsafe_allow_html=True)
        
        if st.button("🔊 Replay Word"):
            st.rerun()

        user_input = st.text_input("Type the word here:", key=f"input_{st.session_state.current_round}").strip().lower()

        if st.button("Submit"):
            if user_input == target_word.lower():
                st.success("Correct! You are doing great! 🌟")
                st.session_state.score += 1
            else:
                st.error(f"Keep trying! The correct spelling was: {target_word}")
                st.session_state.wrong_words.append(target_word)
            
            st.session_state.current_round += 1
            st.rerun()
    
    else:
        st.balloons()
        st.header("🎉 Well Done!")
        st.write(f"Your Final Score: **{st.session_state.score} / 25**")
        
        if st.session_state.score >= 20:
            st.write("🌈 Incredible work! You're a spelling superstar!")
        else:
            st.write("💖 Wonderful effort! Practice makes perfect, and you're doing great!")

        if st.session_state.wrong_words:
            if st.checkbox("Show words to review"):
                st.write("Review these words to get even better:")
                for word in st.session_state.wrong_words:
                    st.write(f"- {word}")
        
        if st.button("Play Again"):
            st.session_state.game_started = False
            st.rerun()
