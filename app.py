import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# --- 1. FULL WORD DATA & POOLS ---
# Definitions and examples added for a sample; this structure must be used for all 450 words.
WORD_DATA = {
    "unicorn": ["A mythical animal with a single horn on its forehead.", "The storybook featured a majestic white unicorn."],
    "faraway": ["At a great distance; remote.", "She dreamed of traveling to faraway lands."],
    "heater": ["A device for warming the air or water.", "We turned on the electric heater during the cold night."],
    "pirates": ["Robbers who travel by sea.", "The pirates searched the island for buried treasure."],
    "verdict": ["A decision made by a jury in a court of law.", "The judge read the verdict to the quiet courtroom."],
    "syndrome": ["A group of symptoms that occur together.", "The doctor explained the rare syndrome to the family."],
    "promenade": ["A paved public walk, typically one along a waterfront.", "Families enjoyed a sunset stroll along the beach promenade."],
    # ... Include all other words from the 450-word list here following this format
}

# Word Pools extracted from your documents [cite: 9-56, 68, 140-296, 307-462]
ONE_BEE_POOL = ["tag", "twigs", "insects", "moment", "send", "taffy", "teeth", "ajar", "deck", "comfy", "shortcut", "basil", "stuck", "stretch", "bait", "triple", "snug", "tight", "lure", "satin", "fish", "candy", "cluster", "ahoy", "hold", "scrunch", "forest", "signal", "mind", "ruby", "hollow", "answer", "stay", "close", "spinning", "shuffle", "scrub", "tackle", "baffling", "dollop", "draw", "wire", "sizzling", "minnows", "brown", "skater", "hoist", "silver", "cozy", "giant", "search", "before", "bucket", "remind", "circus", "tint", "chance", "mango", "writing", "milk", "baskets", "coral", "kitchen", "yawn", "tender", "jangle", "sugar", "tank", "paste", "shimmer", "awkward", "want", "melon", "blossoms", "seep", "crowd", "farmer", "swampy", "sweet", "pond", "parent", "studded", "wheels", "skirt", "tail", "focus", "faint", "sharks", "hockey", "distress", "fruit", "quilt", "slime", "lessons", "roam", "goats", "disability", "avocado", "woozy", "incredible", "valentine", "limbs", "leather", "February", "ahead", "countess", "formation", "señor", "nervous", "especially", "unicorn", "peppercorn", "faraway", "cartwheel", "heater", "raise", "pirates", "weather", "understand", "zooming", "wooden", "attacked", "leaning", "turnout", "breakfast", "eaten", "window", "streetlights", "acrobat", "journey", "chocolate", "message", "courtyard", "shouting", "forepaw", "asleep", "elephant", "curious", "hedgehog", "dinosaur", "recipe", "brilliant", "garbage", "vacuum", "surprise", "gorgeous", "mermaid", "monsoon", "bombarded", "dangerous"]
TWO_BEE_POOL = ["hesitate", "Buffalo", "dubious", "dissolving", "scorcher", "sequins", "ebony", "nomad", "scavenger", "fragments", "gallop", "fabulous", "foreign", "billowed", "paltry", "skewer", "deflated", "lanky", "verdict", "Berlin", "unleash", "fluently", "garbled", "lunacy", "ration", "mysterious", "encourages", "conjure", "cosmetics", "brandished", "imitation", "bracken", "crawdad", "sardines", "miniature", "noggin", "frustration", "anguish", "receptionist", "neon", "unruly", "conical", "preamble", "rakish", "mascot", "rickety", "plausible", "hypnosis", "aroma", "lilt", "reprimanding", "rotunda", "moustache", "pediatric", "commotion", "gusto", "porridge", "oblivion", "toiletries", "artifacts", "democracy", "immigrants", "gleaned", "rummage", "steeple", "jeered", "perfume", "beige", "spectators", "winsome", "sinister", "ancestral", "lanyards", "prattling", "tuxedo", "grimace", "suspicious", "galore", "discoveries", "gaunt", "parchment", "emporium", "lurches", "enormous", "ramshackle", "atrium", "language", "geranium", "fugitive", "eccentric", "prognosis", "nautical", "heron", "savant", "almanac", "talcum", "hippies", "samosas", "tranquilizer", "equestrian", "chignon", "pheromone", "campaign", "plaited", "galleon", "magnanimous", "pistachio", "monsieur", "chartreuse", "mosque", "manticores", "wainscoting", "zombielike", "prestigious", "Nehru", "warlock", "fraidycat", "colossus", "guttural", "convulsively", "lo mein", "dimensional", "courier", "garishly", "sans serif", "graffitist", "psyche", "Everest", "stucco", "dexterity", "Frankenstein", "cavorting", "schema", "marauder", "et cetera", "conscience", "vidimus", "battlements", "delphine", "deferential", "slough", "albatross", "archipelago", "khaki", "serape", "opalescent", "asphalt", "puissance", "Yiddish", "pinioning"]
THREE_BEE_POOL = ["gangly", "comrades", "ultimatum", "swaggering", "sporadic", "whinnying", "prototype", "cravenly", "chimneys", "promenade", "squalor", "mulberry", "riveted", "repugnant", "memoirs", "hypocritical", "plaid", "invincible", "cylinders", "chlorine", "dirge", "renowned", "ominous", "traumatic", "zeal", "parachute", "muffler", "receipts", "whittled", "laborious", "syndrome", "solemnly", "depots", "appointment", "premises", "begrudge", "fiberglass", "foreseeable", "safari", "contentious", "salvaged", "ratify", "lasagna", "precocious", "fissures", "scalpel", "substantially", "ensemble", "enthusiastic", "reclusive", "mercantile", "cadre", "discipline", "compassionate", "formidable", "lye", "unfamiliar", "bulletin", "propaganda", "belfry", "scurrying", "alfalfa", "marquee", "lacrosse", "dignitaries", "officially", "proficient", "sluice", "pizzeria", "crematorium", "compunction", "cajolery", "dismissal", "bayonet", "emphatically", "vigilance", "skittish", "amicable", "hyperventilated", "residuals", "careened", "exuberant", "ostracism", "boutique", "nomination", "beautician", "onslaught", "peroxide", "opportunist", "equations", "ruefully", "aristocracy", "dictatorship", "assignment", "misanthrope", "apocalypse", "tuberculosis", "patriarchs", "boll weevil", "barricade", "chandelier", "camphor", "confreres", "dulce", "Tucson", "Oswego", "diphtheria", "baklava", "anonymously", "concierge", "paparazzi", "corbels", "unparalleled", "latticework", "pumpernickel", "trebuchets", "barrette", "hibiscus", "pogrom", "Kilimanjaro", "chassis", "tamale", "bursitis", "fräulein", "junket", "maracas", "pâtisserie", "protégé", "quandary", "gyroplane", "cycads", "hors d'oeuvres", "Erie", "burpees", "sarsaparilla", "maquisards", "gingham", "Adriatic", "maître d'", "Aubusson", "silhouette", "piccolo", "cannelloni", "Charolais", "auxiliary", "au revoir", "boulangerie", "thesaurus", "tulle", "bronchitis"]

# 3rd Grade Subset (50 words specifically) [cite: 9-56]
THIRD_GRADE_POOL = ["unicorn", "faraway", "heater", "pirates", "understand", "wooden", "leaning", "breakfast", "window", "acrobat", "message", "chocolate", "forepaw", "elephant", "hedgehog", "recipe", "garbage", "surprise", "mermaid", "bombarded", "disability", "incredible", "nervous", "raise", "leather", "peppercorn", "weather", "countess", "cartwheel", "zooming", "attacked", "turnout", "eaten", "streetlights", "journey", "courtyard", "shouting", "asleep", "curious", "dinosaur", "brilliant", "vacuum", "gorgeous", "monsoon", "dangerous", "avocado", "valentine", "February", "formation", "especially"]

# --- 2. HELPERS ---
def get_audio_base64(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

st.set_page_config(page_title="School Spelling Bee", page_icon="🐝")
st.title("🐝 Scripps Spelling Bee Trainer")

# --- 3. SESSION STATE ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_round = 0
    st.session_state.score = 0
    st.session_state.wrong_words = []
    st.session_state.game_words = []
    st.session_state.audio_key = 0 # Unique key to force audio replay

# --- 4. GAME START SCREEN ---
if not st.session_state.game_started:
    st.subheader("Select Your Challenge:")
    mode = st.radio("Choose Game Mode:", ["3rd Grader Spelling Bee", "School Spelling Bee: One Bee", "School Spelling Bee: Two Bee", "School Spelling Bee: Three Bee"])
    
    if st.button("Start Game"):
        # Set lengths and pools based on selection
        if "3rd Grader" in mode:
            st.session_state.game_words = random.sample(THIRD_GRADE_POOL, 20)
        elif "One Bee" in mode:
            st.session_state.game_words = random.sample(ONE_BEE_POOL, 20)
        elif "Two Bee" in mode:
            st.session_state.game_words = random.sample(TWO_BEE_POOL, 10)
        else: # Three Bee
            st.session_state.game_words = random.sample(THREE_BEE_POOL, 10)
            
        st.session_state.game_started = True
        st.session_state.current_round = 0
        st.session_state.score = 0
        st.session_state.wrong_words = []
        st.rerun()

# --- 5. GAME INTERFACE ---
else:
    total_words = len(st.session_state.game_words)
    if st.session_state.current_round < total_words:
        target_word = st.session_state.game_words[st.session_state.current_round]
        st.subheader(f"Word {st.session_state.current_round + 1} of {total_words}")
        
        # Audio Player (Fixed with unique key for Replay)
        audio_b64 = get_audio_base64(target_word)
        st.markdown(f'<audio key="{st.session_state.audio_key}" autoplay src="data:audio/mp3;base64,{audio_b64}">', unsafe_allow_html=True)
        
        if st.button("🔊 Replay Word"):
            st.session_state.audio_key += 1 # Forces Streamlit to re-render the audio component
            st.rerun()

        user_input = st.text_input("Spelling:", key=f"in_{st.session_state.current_round}").strip().lower()

        if st.button("Submit Answer"):
            if user_input == target_word.lower():
                st.success("Correct! You're a spelling superstar! 🌟")
                st.session_state.score += 1
            else:
                st.error(f"Keep trying! The word was: {target_word}")
                st.session_state.wrong_words.append(target_word)
            
            st.session_state.current_round += 1
            st.rerun()

    # --- 6. RESULTS & REVIEW (FIXED ISSUE #1) ---
    else:
        st.balloons()
        st.header("Results")
        st.metric("Final Score", f"{st.session_state.score} / {total_words}")
        st.write("Fantastic effort! Your practice is paying off! 🌈")
        
        if st.session_state.wrong_words:
            st.subheader("Study Your Missed Words:")
            for word in st.session_state.wrong_words:
                # Look up definition/example or provide placeholder if missing
                info = WORD_DATA.get(word.lower(), ["Definition not yet in database.", "Example not yet in database."])
                with st.expander(f"Review: {word}"):
                    st.write(f"📖 **Meaning:** {info[0]}")
                    st.write(f"📝 **Example:** *{info[1]}*")
        
        if st.button("New Game"):
            st.session_state.game_started = False
            st.rerun()
