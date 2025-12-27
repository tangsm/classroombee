import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO

# --- 1. WORD POOLS (EXTRACTED FROM YOUR PDFS) ---
POOLS = {
    "3rd Grader": ["unicorn", "faraway", "heater", "pirates", "understand", "wooden", "leaning", "breakfast", "window", "acrobat", "message", "chocolate", "forepaw", "elephant", "hedgehog", "recipe", "garbage", "surprise", "mermaid", "bombarded", "disability", "incredible", "nervous", "raise", "leather", "peppercorn", "weather", "countess", "cartwheel", "zooming", "attacked", "turnout", "eaten", "streetlights", "journey", "courtyard", "shouting", "asleep", "curious", "dinosaur", "brilliant", "vacuum", "gorgeous", "monsoon", "dangerous", "avocado", "valentine", "February", "formation", "especially"],
    "One Bee": ["tag", "twigs", "insects", "moment", "send", "taffy", "teeth", "ajar", "deck", "comfy", "shortcut", "basil", "stuck", "stretch", "bait", "triple", "snug", "tight", "lure", "satin", "fish", "candy", "cluster", "ahoy", "hold", "scrunch", "forest", "signal", "mind", "ruby", "hollow", "answer", "stay", "close", "spinning", "shuffle", "scrub", "tackle", "baffling", "dollop", "draw", "wire", "sizzling", "minnows", "brown", "skater", "hoist", "silver", "cozy", "giant", "search", "before", "bucket", "remind", "circus", "tint", "chance", "mango", "writing", "milk", "baskets", "coral", "kitchen", "yawn", "tender", "jangle", "sugar", "tank", "paste", "shimmer", "awkward", "want", "melon", "blossoms", "seep", "crowd", "farmer", "swampy", "sweet", "pond", "parent", "studded", "wheels", "skirt", "tail", "focus", "faint", "sharks", "hockey", "distress", "fruit", "quilt", "slime", "lessons", "roam", "goats"],
    "Two Bee": ["hesitate", "buffalo", "dubious", "dissolving", "scorcher", "sequins", "ebony", "nomad", "scavenger", "fragments", "gallop", "fabulous", "foreign", "billowed", "paltry", "skewer", "deflated", "lanky", "verdict", "berlin", "unleash", "fluently", "garbled", "lunacy", "ration", "mysterious", "encourages", "conjure", "cosmetics", "brandished", "imitation", "bracken", "crawdad", "sardines", "miniature", "noggin", "frustration", "anguish", "receptionist", "neon", "unruly", "conical", "preamble", "rakish", "mascot", "rickety", "plausible", "hypnosis", "aroma", "lilt", "reprimanding", "rotunda", "moustache", "pediatric", "commotion", "gusto", "porridge", "oblivion", "toiletries", "artifacts", "democracy", "immigrants", "gleaned", "rummage", "steeple", "jeered", "perfume", "beige", "spectators", "winsome", "sinister", "ancestral", "lanyards", "prattling", "tuxedo", "grimace", "suspicious", "galore", "discoveries", "gaunt", "parchment", "emporium", "lurches", "enormous", "ramshackle", "atrium", "language", "geranium", "fugitive", "eccentric", "prognosis", "nautical", "heron", "savant", "almanac", "talcum", "hippies", "samosas", "tranquilizer", "equestrian", "chignon", "pheromone", "campaign", "plaited", "galleon", "magnanimous", "pistachio", "monsieur", "chartreuse", "mosque", "manticores", "wainscoting", "zombielike", "prestigious", "nehru", "warlock", "fraidycat", "colossus", "guttural", "convulsively", "courier", "garishly", "psyche", "everest", "stucco", "dexterity", "frankenstein", "cavorting", "schema", "marauder", "conscience", "vidimus", "battlements", "delphine", "deferential", "slough", "albatross", "archipelago", "khaki", "serape", "opalescent", "asphalt", "puissance", "pinioning"],
    "Three Bee": ["gangly", "comrades", "ultimatum", "swaggering", "sporadic", "whinnying", "prototype", "cravenly", "chimneys", "promenade", "squalor", "mulberry", "riveted", "repugnant", "memoirs", "hypocritical", "plaid", "invincible", "cylinders", "chlorine", "dirge", "renowned", "ominous", "traumatic", "zeal", "parachute", "muffler", "receipts", "whittled", "laborious", "syndrome", "solemnly", "depots", "appointment", "premises", "begrudge", "fiberglass", "foreseeable", "safari", "contentious", "salvaged", "ratify", "lasagna", "precocious", "fissures", "scalpel", "substantially", "ensemble", "enthusiastic", "reclusive", "mercantile", "cadre", "discipline", "compassionate", "formidable", "lye", "unfamiliar", "bulletin", "propaganda", "belfry", "scurrying", "alfalfa", "marquee", "lacrosse", "dignitaries", "officially", "proficient", "sluice", "pizzeria", "crematorium", "compunction", "cajolery", "dismissal", "bayonet", "emphatically", "vigilance", "skittish", "amicable", "hyperventilated", "residuals", "careened", "exuberant", "ostracism", "boutique", "nomination", "beautician", "onslaught", "peroxide", "opportunist", "equations", "ruefully", "aristocracy", "dictatorship", "assignment", "misanthrope", "apocalypse", "tuberculosis", "patriarchs", "barricade", "chandelier", "camphor", "confreres", "dulce", "tucson", "oswego", "diphtheria", "baklava", "anonymously", "concierge", "paparazzi", "corbels", "unparalleled", "latticework", "pumpernickel", "trebuchets", "barrette", "hibiscus", "pogrom", "kilimanjaro", "chassis", "tamale", "bursitis", "junket", "maracas", "protégé", "quandary", "gyroplane", "cycads", "gingham", "adriatic", "silhouette", "piccolo", "cannelloni", "auxiliary", "thesaurus", "tulle", "bronchitis"]
}

# --- 2. MASTER DICTIONARY (MEANINGS & EXAMPLES) ---
# This function serves as the central database for word information.
def get_word_details(word):
    # Mapping for specific Scripps words provided in the lists
    data = {
        "serape": ["A colorful woolen shawl or blanket worn in Mexico.", "He draped a bright serape over his shoulders for the festival."],
        "unicorn": ["A mythical horse-like creature with a single horn.", "The unicorn is a symbol of magic and purity."],
        "verdict": ["The decision made by a jury in a trial.", "The jury reached a unanimous verdict of not guilty."],
        "syndrome": ["A group of symptoms that consistently occur together.", "The doctor identified the rare syndrome after several tests."],
        "gangly": ["Awkwardly tall and thin.", "The gangly teenager struggled to find pants that fit."],
        "promenade": ["A paved public walk, typically one along a waterfront.", "They took a evening stroll along the beach promenade."],
        "hesitate": ["To pause before saying or doing something.", "Do not hesitate to call if you need help."],
        "scorcher": ["A day or period of very hot weather.", "Last Monday was a real scorcher, reaching 100 degrees."],
        "especially": ["To a great extent; very much.", "I love all fruit, especially strawberries."],
        "february": ["The second month of the year.", "February is the only month with 28 days."],
        "dinosaur": ["A fossil reptile of the Mesozoic era.", "The museum has a massive T-Rex dinosaur skeleton."],
        # Add additional definitions as needed. 
    }
    
    # Return specific data or a helpful generic response if not yet filled
    return data.get(word.lower(), [
        "Please consult the Merriam-Webster Scripps Dictionary for this specific definition.",
        f"You used the word '{word}' correctly in the spelling round!"
    ])

# --- 3. CORE LOGIC & AUDIO ---
def get_audio(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

st.set_page_config(page_title="Bee Ready Spelling", page_icon="🐝")
st.title("🐝 National Spelling Bee Trainer")

if 'game' not in st.session_state:
    st.session_state.game = {"active": False, "round": 0, "score": 0, "words": [], "wrong": [], "audio_id": 0}

# --- START SCREEN ---
if not st.session_state.game["active"]:
    st.subheader("Select Your Level")
    choice = st.selectbox("Level:", list(POOLS.keys()))
    if st.button("Start"):
        count = 20 if choice in ["3rd Grader", "One Bee"] else 10
        st.session_state.game["words"] = random.sample(POOLS[choice], count)
        st.session_state.game["active"] = True
        st.session_state.game["round"] = 0
        st.session_state.game["score"] = 0
        st.session_state.game["wrong"] = []
        st.rerun()

# --- GAME SCREEN ---
else:
    game = st.session_state.game
    if game["round"] < len(game["words"]):
        word = game["words"][game["round"]]
        st.write(f"### Word {game['round'] + 1} of {len(game['words'])}")
        
        # Audio & Replay (Fixed)
        audio_b64 = get_audio(word)
        st.markdown(f'<audio key="{game["audio_id"]}" autoplay src="data:audio/mp3;base64,{audio_b64}">', unsafe_allow_html=True)
        if st.button("🔊 Replay"):
            game["audio_id"] += 1
            st.rerun()

        ans = st.text_input("Type it:", key=f"ans_{game['round']}").strip().lower()
        if st.button("Submit"):
            if ans == word.lower():
                st.success("Correct! ✨")
                game["score"] += 1
            else:
                st.error(f"Incorrect. It was: {word}")
                game["wrong"].append(word)
            game["round"] += 1
            st.rerun()
    
    # --- RESULTS ---
    else:
        st.balloons()
        st.header("Great Practice!")
        st.metric("Score", f"{game['score']}/{len(game['words'])}")
        st.info("Keep it up! Every word you practice makes you a better speller. 🌈")
        
        if game["wrong"]:
            st.subheader("Review Your Missed Words")
            for w in game["wrong"]:
                info = get_word_details(w)
                with st.expander(f"📖 {w}"):
                    st.write(f"**Meaning:** {info[0]}")
                    st.write(f"**Example:** *{info[1]}*")
        
        if st.button("Play Again"):
            st.session_state.game["active"] = False
            st.rerun()
