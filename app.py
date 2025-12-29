import streamlit as st
import random
from gtts import gTTS
import base64
from io import BytesIO
import time

# --- 1. THE COMPLETE WORD POOLS (450+ WORDS) ---
# 3rd Grade Level (Exactly 50 words from the 3rd Grade PDF)
POOL_3RD = [
    "unicorn", "faraway", "heater", "pirates", "understand", "wooden", "leaning", "breakfast", "window", "acrobat", 
    "message", "chocolate", "forepaw", "elephant", "hedgehog", "recipe", "garbage", "surprise", "mermaid", "bombarded", 
    "disability", "incredible", "nervous", "raise", "leather", "peppercorn", "weather", "countess", "cartwheel", "zooming", 
    "attacked", "turnout", "eaten", "streetlights", "journey", "courtyard", "shouting", "asleep", "curious", "dinosaur", 
    "brilliant", "vacuum", "gorgeous", "monsoon", "dangerous", "avocado", "valentine", "february", "formation", "especially"
]

# One Bee Level (Full 150 words from the 450-word School List)
POOL_ONE = [
    "tag", "send", "deck", "stuck", "snug", "fish", "hold", "mind", "stay", "scrub", "draw", "brown", "cozy", "tint", "milk", 
    "yawn", "tank", "want", "crowd", "pond", "skirt", "sharks", "quilt", "twigs", "taffy", "comfy", "stretch", "tight", "candy", 
    "scrunch", "ruby", "close", "tackle", "wire", "skater", "giant", "bucket", "chance", "baskets", "tender", "paste", "melon", 
    "farmer", "parent", "tail", "hockey", "slime", "insects", "teeth", "shortcut", "bait", "lure", "cluster", "forest", "hollow", 
    "spinning", "baffling", "sizzling", "hoist", "search", "remind", "mango", "coral", "jangle", "shimmer", "blossoms", "swampy", 
    "studded", "focus", "distress", "lessons", "moment", "ajar", "basil", "triple", "satin", "ahoy", "signal", "answer", "shuffle", 
    "dollop", "minnows", "silver", "before", "circus", "writing", "kitchen", "sugar", "awkward", "seep", "sweet", "wheels", "faint", 
    "fruit", "roam", "goats", "woke", "gate", "path", "rock", "luck", "shop", "grin", "boat", "flag", "song", "help", "ship", "glad", 
    "frog", "nest", "hand", "best", "last", "keep", "feet", "bath", "rush", "wish", "jump", "doll", "page", "kite", "bike", "ride", 
    "blue", "green", "pink", "high", "low", "long", "soft", "loud", "look", "book", "good", "food", "play", "rain", "day", "night"
]

# Two Bee & Three Bee Pools (truncated for brevity)
POOL_TWO = [
        "hesitate", "scorcher", "scavenger", "fragments", "deflated", "unleash", "ration", "cosmetics", "crawdad", 
        "frustration", "unruly", "mascot", "aroma", "moustache", "artifacts", "buffalo", "sequins", "gallop", "fabulous", "lanky", 
        "fluently", "mysterious", "brandished", "sardines", "anguish", "conical", "rickety", "lilt", "pediatric", 
        "porridge", "democracy", "rummage", "beige", "ancestral", "grimace", "gaunt", "enormous", "geranium", 
        "nautical", "dubious", "ebony", "foreign", "paltry", "verdict", "garbled", "encourages", "imitation", 
        "miniature", "receptionist", "preamble", "plausible", "reprimanding", "commotion", "oblivion", "immigrants", 
        "steeple", "spectators", "lanyards", "suspicious", "parchment", "ramshackle", "fugitive", "heron", "dissolving", 
        "nomad", "billowed", "skewer", "berlin", "lunacy", "conjure", "bracken", "noggin", "neon", "rakish", "hypnosis", 
        "rotunda", "gusto", "toiletries", "gleaned", "jeered", "winsome", "prattling", "galore", "emporium", "atrium", 
        "eccentric", "savant", "almanac", "talcum", "hippies", "samosas", "tranquilizer", "equestrian", "chignon", 
        "pheromone", "campaign", "plaited", "galleon", "magnanimous", "pistachio", "monsieur", "chartreuse", "mosque", 
        "manticores", "wainscoting", "prestigious", "nehru", "warlock", "fraidycat", "colossus", "guttural", 
        "convulsively", "courier", "garishly", "psyche", "everest", "stucco", "dexterity", "frankenstein", "cavorting", 
        "schema", "marauder", "conscience", "vidimus", "battlements", "delphine", "deferential", "slough", "albatross", 
        "archipelago", "khaki", "serape", "opalescent", "asphalt", "puissance", "pinioning"
    ]

POOL_THREE = [
        "gangly", "comrades", "ultimatum", "swaggering", "sporadic", "whinnying", "prototype", "cravenly", "chimneys", 
        "promenade", "squalor", "mulberry", "riveted", "repugnant", "memoirs", "hypocritical", "plaid", "invincible", 
        "cylinders", "chlorine", "dirge", "renowned", "ominous", "traumatic", "zeal", "parachute", "muffler", "receipts", 
        "whittled", "laborious", "syndrome", "solemnly", "depots", "appointment", "premises", "begrudge", "fiberglass", 
        "foreseeable", "safari", "contentious", "salvaged", "ratify", "lasagna", "precocious", "fissures", "scalpel", 
        "substantially", "ensemble", "enthusiastic", "reclusive", "mercantile", "cadre", "discipline", "compassionate", 
        "formidable", "lye", "unfamiliar", "bulletin", "propaganda", "belfry", "scurrying", "alfalfa", "marquee", 
        "lacrosse", "dignitaries", "officially", "proficient", "sluice", "pizzeria", "crematorium", "compunction", 
        "cajolery", "dismissal", "bayonet", "emphatically", "vigilance", "skittish", "amicable", "hyperventilated", 
        "residuals", "careened", "exuberant", "ostracism", "boutique", "nomination", "beautician", "onslaught", 
        "peroxide", "opportunist", "equations", "ruefully", "aristocracy", "dictatorship", "assignment", "misanthrope", 
        "apocalypse", "tuberculosis", "patriarchs", "barricade", "chandelier", "camphor", "confreres", "dulce", "tucson", 
        "oswego", "diphtheria", "baklava", "anonymously", "concierge", "paparazzi", "corbels", "unparalleled", 
        "latticework", "pumpernickel", "trebuchets", "barrette", "hibiscus", "pogrom", "kilimanjaro", "chassis", "tamale", 
        "bursitis", "junket", "maracas", "protégé", "quandary", "gyroplane", "cycads", "gingham", "adriatic", 
        "silhouette", "piccolo", "cannelloni", "auxiliary", "thesaurus", "tulle", "bronchitis", "Charolais"
    ]

def chunk_words(word_list, chunk_size=50):
    return [word_list[i:i + chunk_size] for i in range(0, len(word_list), chunk_size)]

# Assuming you have your full pools: pool_one, pool_two, pool_three
chunks_one = chunk_words(POOL_ONE)
chunks_two = chunk_words(POOL_TWO)
chunks_three = chunk_words(POOL_THREE)

# --- 2. MASTER DICTIONARY ---
# To avoid the "generic info" bug, every word above must map to a dictionary entry here.
# Below is the logic that ensures the definitions are useful.
WORD_DATA = {
    "acrobat": ["A person who performs gymnastic feats.", "The acrobat walked across the high wire with ease."],
    "adriatic": ["The sea between Italy and the Balkan Peninsula.", "The cruise ship sailed across the blue Adriatic sea."],
    "ahead": ["In a forward direction.", "Keep looking ahead to see the finish line."],
    "ahoy": ["A call used to greet someone or attract attention.", "The sailor shouted 'Ahoy!' to the passing ship."],
    "ajar": ["Slightly open.", "The cat squeezed through the door that was left ajar."],
    "albatross": ["A very large oceanic bird.", "An albatross followed the fishing boat for miles."],
    "alfalfa": ["A plant with clover-like leaves used for fodder.", "The farmer harvested the alfalfa to feed the cows."],
    "almanac": ["A book published every year that contains information about the weather and sun.", "He checked the farmer's almanac to see when the first frost would arrive."],
    "amicable": ["Characterized by friendliness and goodwill.", "The two neighbors reached an amicable agreement about the fence."],
    "ancestral": ["Belonging to or inherited from ancestors.", "She visited her ancestral home in Ireland."],
    "anguish": ["Severe mental or physical pain or suffering.", "The loss of his dog caused him great anguish."],
    "anonymously": ["Without being named or identified.", "The donor gave ten thousand dollars to the charity anonymously."],
    "answer": ["A thing said, written, or done to deal with a question.", "She raised her hand to give the correct answer."],
    "apocalypse": ["The complete final destruction of the world.", "Many movies depict a world after the apocalypse."],
    "appointment": ["An arrangement to meet someone at a particular time.", "I have a dentist appointment at three o'clock."],
    "archipelago": ["A group of islands.", "The archipelago consisted of over a hundred tiny islands."],
    "aristocracy": ["The highest class in certain societies, especially those holding titles.", "The grand ballroom was filled with members of the aristocracy."],
    "aroma": ["A distinctive, typically pleasant smell.", "The aroma of fresh bread filled the kitchen."],
    "artifacts": ["Objects made by humans, typically of historical interest.", "The museum displayed ancient artifacts found in the desert."],
    "asleep": ["In a state of sleep.", "The baby finally fell asleep in the crib."],
    "asphalt": ["A dark bitumen used for surfacing roads.", "The workers poured hot asphalt to fix the highway."],
    "assignment": ["A task or piece of work assigned to someone.", "The teacher collected the writing assignment on Friday."],
    "atrium": ["An open-roofed entrance hall or central court.", "The hotel lobby featured a beautiful atrium with plants."],
    "attacked": ["Set upon by someone or something in a forceful way.", "The castle was attacked at dawn by the enemy."],
    "aubusson": ["A fine hand-woven tapestry or carpet.", "The palace floor was covered with a beautiful Aubusson rug."],
    "auxiliary": ["Providing supplementary or additional help and support.", "The ship has an auxiliary engine in case the main one fails."],
    "avocado": ["A pear-shaped fruit with green skin and a large stone.", "She spread mashed avocado on her toast for breakfast."],
    "awkward": ["Causing or feeling embarrassment or inconvenience.", "There was an awkward silence after the mistake."],
    "baffling": ["Impossible to understand; perplexing.", "The mystery of the missing key was completely baffling."],
    "bait": ["Food used to entice fish or other animals as prey.", "He put a worm on the hook to use as bait."],
    "baklava": ["A dessert made of layers of filo pastry filled with nuts and honey.", "They served sweet baklava and coffee after dinner."],
    "barrette": ["A clip for holding a person's hair in place.", "She wore a shiny silver barrette in her hair."],
    "barricade": ["An improvised barrier erected to block a road.", "The police set up a barricade to keep the crowd back."],
    "basil": ["An aromatic plant of the mint family used in cooking.", "The recipe calls for fresh basil and tomatoes."],
    "baskets": ["Containers used for carrying or holding things.", "The children filled their baskets with apples."],
    "battlements": ["Parapets at the top of a wall, usually of a castle.", "The guards watched for enemies from the castle battlements."],
    "bayonet": ["A blade that may be fixed to the muzzle of a rifle.", "The soldier attached a bayonet to his rifle."],
    "beautician": ["A person whose job is to give people beauty treatments.", "The beautician styled her hair and applied her makeup."],
    "before": ["During the period of time preceding an event.", "Wash your hands before you eat."],
    "begrudge": ["To envy someone the possession or enjoyment of something.", "You shouldn't begrudge him his success."],
    "beige": ["A pale sandy yellowish-brown color.", "The walls of the living room were painted a soft beige."],
    "belfry": ["The part of a bell tower in which bells are housed.", "A family of owls lived in the church belfry."],
    "berlin": ["The capital city of Germany.", "They visited the historic gate in Berlin."],
    "billowed": ["Filled with air and swelled outward.", "The sails billowed as the wind picked up."],
    "blossoms": ["Flowers that bloom on a plant or tree.", "The cherry blossoms looked beautiful in the spring."],
    "bombarded": ["Attacked continuously with bombs or questions.", "The reporters bombarded the actor with questions."],
    "boulangerie": ["A bakery that specializes in bread.", "The smell of fresh baguettes floated from the boulangerie."],
    "boutique": ["A small shop selling fashionable clothes or items.", "She bought a unique dress at a small boutique downtown."],
    "bracken": ["A tall fern with coarse lobed fronds.", "The deer hid in the thick bracken of the forest."],
    "brandished": ["Waved something as a threat or in anger or excitement.", "The pirate brandished his sword and shouted."],
    "breakfast": ["The first meal of the day.", "We had eggs and toast for breakfast."],
    "brilliant": ["Exceptionally clever or talented.", "The student came up with a brilliant idea for the project."],
    "bronchitis": ["Inflammation of the mucous membrane in the bronchial tubes.", "His cough got worse when he developed bronchitis."],
    "brown": ["A color produced by mixing orange and black.", "The leaves turned brown and fell from the trees."],
    "bucket": ["A cylindrical container used for carrying liquids.", "He used a bucket to carry water to the garden."],
    "buffalo": ["A heavily built wild ox with backward-curving horns.", "A herd of buffalo roamed across the grassy plains."],
    "bulletin": ["A short official statement or summary of news.", "The school posted a bulletin about the upcoming fair."],
    "burpees": ["A physical exercise consisting of a squat thrust.", "We had to do twenty burpees in gym class."],
    "bursitis": ["Inflammation of a bursa, typically in the shoulder.", "The pitcher had to rest his arm due to bursitis."],
    "cadre": ["A small group of people specially trained for a purpose.", "A cadre of experts was assembled to solve the problem."],
    "cajolery": ["Coaxing or flattery intended to persuade someone.", "Through much cajolery, she got her brother to do the dishes."],
    "campaign": ["An organized course of action to achieve a goal.", "The candidate started her campaign for mayor."],
    "camphor": ["A white substance with an aromatic smell used in medicine.", "The ointment smelled strongly of camphor."],
    "candy": ["A sweet food made with sugar or syrup.", "The shop sold many different kinds of colorful candy."],
    "cannelloni": ["Pasta in the form of tubes, usually stuffed with meat.", "The restaurant is famous for its cheese cannelloni."],
    "careened": ["Moved swiftly and in an uncontrolled way in a specified direction.", "The car careened around the corner on two wheels."],
    "cartwheel": ["A circular sideways gymnastic movement.", "She performed a perfect cartwheel on the grass."],
    "cavorting": ["Jumping or dancing around excitedly.", "The puppies were cavorting in the backyard."],
    "chance": ["A possibility of something happening.", "There is a good chance that it will rain tomorrow."],
    "chandelier": ["A decorative hanging light with branches for several bulbs.", "A crystal chandelier hung from the ceiling of the ballroom."],
    "charolais": ["A breed of large white beef cattle.", "The rancher raised a herd of Charolais cattle."],
    "chartreuse": ["A pale apple-green color.", "The bright chartreuse dress was easy to spot in the crowd."],
    "chassis": ["The base frame of a motor vehicle or other wheeled object.", "The mechanic inspected the chassis of the car for rust."],
    "chignon": ["A knot or coil of hair worn at the back of a woman's head.", "She wore her hair in a elegant chignon for the wedding."],
    "chimneys": ["Structures through which smoke from a fire is carried away.", "Smoke rose from the chimneys of the old houses."],
    "chlorine": ["A chemical element used as a disinfectant in pools.", "The smell of chlorine was strong near the swimming pool."],
    "chocolate": ["A food preparation made from roasted cacao seeds.", "I would like a piece of dark chocolate for dessert."],
    "circus": ["A traveling company of acrobats, clowns, and animals.", "We went to the circus to see the tightrope walkers."],
    "close": ["A short distance away or around.", "Please make sure to close the gate behind you."],
    "cluster": ["A group of similar things or people positioned closely together.", "A cluster of grapes hung from the vine."],
    "colossus": ["A person or thing of enormous size, importance, or ability.", "The statue was a colossus that towered over the harbor."],
    "comfy": ["Comfortable.", "The old armchair was very soft and comfy."],
    "commotion": ["A state of confused and noisy disturbance.", "There was a loud commotion in the street outside."],
    "compassionate": ["Feeling or showing sympathy and concern for others.", "The nurse was very compassionate toward her patients."],
    "compunction": ["A feeling of guilt or moral scruple that prevents or follows a bad deed.", "He felt no compunction about telling a small lie."],
    "comrades": ["Colleagues or a fellow members of an organization.", "The soldiers were loyal comrades who fought together."],
    "concierge": ["A hotel staff member who helps guests with arrangements.", "The concierge helped us book tickets for the show."],
    "confreres": ["Fellow members of a profession.", "The scientist discussed the findings with his confreres."],
    "conical": ["Shaped like a cone.", "The party hats were bright and conical."],
    "conjure": ["To call upon a spirit or ghost to appear.", "The magician seemed to conjure a rabbit out of thin air."],
    "conscience": ["An inner feeling or voice viewed as acting as a guide.", "He followed his conscience and did the right thing."],
    "contentious": ["Causing or likely to cause an argument.", "The new law became a contentious issue in the town."],
    "convulsively": ["In a way that resembles a sudden involuntary movement.", "The patient started shaking convulsively."],
    "coral": ["A hard stony substance secreted by certain marine animals.", "We went snorkeling to see the beautiful coral reef."],
    "corbels": ["Projections of stone or wood jutting from a wall.", "The roof was supported by carved wooden corbels."],
    "cosmetics": ["Products used to improve or alter the appearance of the face.", "She bought new cosmetics at the department store."],
    "countess": ["A woman holding the rank of count or earl.", "The countess lived in a large castle on the hill."],
    "courier": ["A messenger who transports goods or documents.", "The courier delivered the urgent package on his bike."],
    "courtyard": ["An unroofed area that is completely or partially enclosed by walls.", "The palace had a beautiful courtyard with a fountain."],
    "cozy": ["Giving a feeling of comfort, warmth, and relaxation.", "We spent a cozy evening by the fireplace."],
    "cravenly": ["In a way that shows a lack of courage; cowardly.", "The villain cravenly begged for mercy."],
    "crawdad": ["A freshwater crustacean resembling a small lobster.", "We went down to the creek to catch a crawdad."],
    "crematorium": ["A place where a dead person's body is cremated.", "The service was held at the local crematorium."],
    "crowd": ["A large number of people gathered together.", "A huge crowd waited for the concert to begin."],
    "curious": ["Eager to know or learn something.", "The curious kitten explored every corner of the house."],
    "cycads": ["Stout and woody plants that resemble palms or ferns.", "The botanical garden has a collection of ancient cycads."],
    "cylinders": ["Solid geometric figures with straight parallel sides.", "The engine has four large metal cylinders."],
    "dangerous": ["Able or likely to cause harm or injury.", "It is dangerous to walk alone in the dark."],
    "deck": ["A flat surface that forms the floor of a ship.", "We sat on the deck of the boat and watched the waves."],
    "deferential": ["Showing humble submission and respect.", "The young man was always deferential toward his elders."],
    "deflated": ["Let air or gas out of a tire or balloon.", "The basketball was flat because it was deflated."],
    "delphine": ["Relating to or resembling a dolphin.", "The artist painted a beautiful delphine pattern on the wall."],
    "democracy": ["A system of government by the whole population.", "Voting is an important part of a democracy."],
    "depots": ["Places where supplies are stored or where buses stop.", "The supply depots were located along the main road."],
    "dexterity": ["Skill in performing tasks, especially with the hands.", "The surgeon performed the operation with great dexterity."],
    "dictatorship": ["A form of government where one person has absolute power.", "The country struggled under the rule of a dictatorship."],
    "dignitaries": ["People considered to be important because of high rank.", "Local dignitaries attended the opening of the new library."],
    "dimensional": ["Relating to dimensions or measurements.", "The architect drew a three-dimensional model of the house."],
    "dinosaur": ["A fossil reptile of the Mesozoic era.", "The museum has a skeleton of a massive dinosaur."],
    "diphtheria": ["An acute, highly contagious bacterial disease.", "The child was vaccinated against diphtheria."],
    "dirge": ["A lament for the dead, especially one forming part of a funeral.", "The choir sang a solemn dirge at the service."],
    "disability": ["A physical or mental condition that limits movements.", "The building was designed to be accessible for people with a disability."],
    "discipline": ["The practice of training people to obey rules.", "It takes a lot of discipline to practice the piano every day."],
    "discoveries": ["Acts of finding or learning something for the first time.", "The scientists made several important discoveries in the cave."],
    "dismissal": ["The act of ordering or allowing someone to leave.", "We waited for the bell to ring for our dismissal from class."],
    "dissolving": ["Becoming or causing to become incorporated into a liquid.", "The sugar is dissolving in the hot tea."],
    "distress": ["Extreme anxiety, sorrow, or pain.", "The news of the accident caused her much distress."],
    "dollop": ["A shapeless mass or blob of something.", "She added a dollop of whipped cream to her pie."],
    "draw": ["To produce a picture or diagram by making lines and marks.", "I like to draw pictures of animals in my notebook."],
    "dubious": ["Hesitating or doubting.", "He looked dubious when I told him the story."],
    "dulce": ["Sweet; specifically a sweet food or drink.", "The shop sold many different types of dulce and treats."],
    "eaten": ["Consumed food.", "The hungry dog had eaten all of its dinner."],
    "ebony": ["A very dark brown or black color.", "The piano keys were made of white ivory and black ebony."],
    "eccentric": ["Unconventional and slightly strange.", "The inventor was known for his eccentric behavior."],
    "elephant": ["A very large herbivorous mammal with a trunk.", "The elephant used its trunk to pull a branch from the tree."],
    "emphatically": ["In a forceful way.", "She emphatically denied that she had broken the vase."],
    "emporium": ["A large retail store selling a wide variety of goods.", "The toy emporium was filled with dolls and games."],
    "encourages": ["Gives support, confidence, or hope to someone.", "The coach always encourages the team to do their best."],
    "enormous": ["Very large in size, quantity, or extent.", "The giant lived in an enormous castle on the hill."],
    "ensemble": ["A group of musicians, actors, or dancers who perform together.", "The jazz ensemble played until midnight."],
    "enthusiastic": ["Having or showing intense enjoyment or interest.", "The kids were very enthusiastic about the trip to the zoo."],
    "equations": ["Mathematical statements that two expressions are equal.", "The students learned how to solve simple equations."],
    "equestrian": ["Relating to horse riding.", "The equestrian center offered riding lessons for beginners."],
    "erie": ["One of the five Great Lakes of North America.", "We spent our summer vacation on the shores of Lake Erie."],
    "especially": ["Used to single out one person or thing over others.", "I like all fruits, especially strawberries."],
    "everest": ["The highest mountain in the world.", "Climbing Mount Everest is a very difficult challenge."],
    "exuberant": ["Filled with or characterized by a lively energy.", "The exuberant puppy jumped up to greet us."],
    "fabulous": ["Extraordinary, especially extraordinarily good.", "We had a fabulous time at the party."],
    "faint": ["Lacking brightness, vividness, or strength.", "There was a faint smell of perfume in the room."],
    "faraway": ["Distant in space or time.", "The princess lived in a faraway kingdom."],
    "farmer": ["A person who owns or manages a farm.", "The farmer planted rows of corn in the field."],
    "february": ["The second month of the year.", "Valentine's Day is on February 14th."],
    "fiberglass": ["A reinforced plastic material composed of glass fibers.", "The boat's hull was made of durable fiberglass."],
    "fish": ["A limbless cold-blooded vertebrate animal with gills.", "We went to the lake to catch some fish."],
    "fissures": ["Long, narrow openings or cracks.", "The earthquake caused deep fissures in the ground."],
    "fluently": ["In a smooth and easy way.", "She speaks three different languages fluently."],
    "focus": ["The center of interest or activity.", "Please try to focus on your schoolwork."],
    "foreign": ["Of, from, in, or characteristic of a country other than one's own.", "She enjoyed visiting foreign countries and learning new things."],
    "forepaw": ["A front paw of a four-legged animal.", "The cat groomed its forepaw after eating."],
    "foreseeable": ["Able to be predicted or anticipated.", "There are no changes planned for the foreseeable future."],
    "forest": ["A large area covered chiefly with trees and undergrowth.", "The birds built their nests in the thick forest."],
    "formation": ["The action of forming or the process of being formed.", "The planes flew in a tight formation over the city."],
    "formidable": ["Inspiring fear or respect through being impressively large.", "The champion was a formidable opponent on the tennis court."],
    "fragments": ["Small parts broken or separated from something.", "Fragments of the broken glass were scattered on the floor."],
    "fraidycat": ["A person who is easily frightened.", "Don't be a fraidycat and come into the haunted house!"],
    "frankenstein": ["A thing that becomes terrifying to its creator.", "The new project turned into a bit of a Frankenstein."],
    "fruit": ["The sweet and fleshy product of a tree or plant.", "Apples and oranges are my favorite kinds of fruit."],
    "frustration": ["The feeling of being annoyed or upset.", "He shouted in frustration when he couldn't find his keys."],
    "fräulein": ["A title or form of address for an unmarried German-speaking woman.", "The children called their teacher 'Fräulein'."],
    "fugitive": ["A person who has escaped from a place or is in hiding.", "The police searched the woods for the escaped fugitive."],
    "galleon": ["A large sailing ship used by Spain as a warship.", "The pirates searched for a sunken Spanish galleon."],
    "gallop": ["The fastest pace of a horse or other quadruped.", "The horse started to gallop across the open field."],
    "galore": ["In abundance.", "There were games and prizes galore at the fair."],
    "gangly": ["Awkwardly tall and thin.", "The gangly puppy hadn't yet grown into its large paws."],
    "garbage": ["Wasted or spoiled food and other refuse.", "Don't forget to take the garbage out to the curb."],
    "garbled": ["Reproduced in a confused and distorted way.", "The message on the radio was garbled and hard to hear."],
    "garishly": ["In a loud, bright, or gaudy way.", "The room was garishly decorated with bright neon colors."],
    "gaunt": ["Lean and haggard, especially because of suffering or age.", "The old man had a gaunt face and thin hands."],
    "geranium": ["A herbaceous plant with red, pink, or white flowers.", "She planted red geraniums in the window box."],
    "giant": ["A person or thing of unusually great size.", "The giant lived in a house at the top of a beanstalk."],
    "gingham": ["Lightweight plain-woven cotton cloth, typically checked.", "She wore a blue and white gingham dress to the picnic."],
    "gleaned": ["Extracted information from various sources.", "She gleaned a lot of information about the town from the library."],
    "goats": ["Hardy domesticated ruminant mammals.", "The goats climbed high up onto the rocky hills."],
    "gorgeous": ["Beautiful; very attractive.", "The sunset over the ocean was absolutely gorgeous."],
    "graffitist": ["A person who creates graffiti.", "The local graffitist painted a mural on the side of the building."],
    "grimace": ["An ugly, twisted expression on a person's face.", "He made a grimace when he tasted the sour lemon."],
    "gusto": ["Enjoyment or vigor in doing something.", "The hungry boys ate their dinner with great gusto."],
    "guttural": ["Produced in the throat; harsh-sounding.", "The beast made a low guttural sound in its throat."],
    "gyroplane": ["An aircraft that uses a freely rotating rotor to provide lift.", "The pilot flew the small gyroplane over the field."],
    "heater": ["A device for warming the air or water.", "We turned on the heater when the room got cold."],
    "hedgehog": ["A small nocturnal mammal covered in spines.", "The hedgehog rolled into a ball to protect itself."],
    "heron": ["A large bird with long legs and a long neck.", "A gray heron stood still in the shallow water of the pond."],
    "hesitate": ["To pause before saying or doing something.", "Do not hesitate to ask if you have any questions."],
    "hibiscus": ["A plant with large, colorful flowers.", "A bright pink hibiscus bloomed in the garden."],
    "hippies": ["People associated with a subculture of the 1960s.", "The park was filled with hippies wearing tie-dye shirts."],
    "hockey": ["A team sport played on ice or a field.", "He put on his skates to play a game of ice hockey."],
    "hoist": ["To raise or lift something up.", "The workers used a crane to hoist the heavy beam."],
    "hold": ["To grasp, carry, or support with one's arms or hands.", "Please hold the ladder steady while I climb up."],
    "hollow": ["Having a hole or empty space inside.", "The owl lived in the hollow trunk of an old oak tree."],
    "hyperventilated": ["Breathed at an abnormally rapid rate.", "The runner hyperventilated after finishing the long race."],
    "hypnosis": ["The induction of a state of consciousness in which a person loses the power of voluntary action.", "The performer put the volunteer into a deep hypnosis."],
    "hypocritical": ["Behaving in a way that suggests one has higher standards than is the case.", "It would be hypocritical of him to complain about noise."],
    "imitation": ["The action of using someone or something as a model.", "The singer did a funny imitation of a famous actor."],
    "immigrants": ["People who come to live permanently in a foreign country.", "Many immigrants arrived in the city looking for work."],
    "incredible": ["Impossible to believe.", "The magician performed an incredible trick with a deck of cards."],
    "insects": ["Small arthropod animals that have six legs.", "The garden was filled with many different kinds of colorful insects."],
    "invincible": ["Too powerful to be defeated or overcome.", "The team felt invincible after winning ten games in a row."],
    "jangle": ["To make a ringing metallic sound.", "The keys in his pocket started to jangle as he ran."],
    "jeered": ["Made rude and mocking remarks.", "The crowd jeered at the opposing team's mistake."],
    "journey": ["An act of traveling from one place to another.", "The explorers started their long journey across the desert."],
    "junket": ["An extravagant trip or celebration.", "The company sent the executives on a junket to Hawaii."],
    "khaki": ["A textile fabric of a dull brownish-yellow color.", "He wore a pair of khaki pants and a white shirt."],
    "kilimanjaro": ["The highest mountain in Africa.", "They planned an expedition to climb Mount Kilimanjaro."],
    "kitchen": ["A room where food is prepared and cooked.", "The smell of baking cookies came from the kitchen."],
    "laborious": ["Requiring considerable effort and time.", "Digging the deep hole was a laborious task."],
    "lacrosse": ["A team sport played with a ball and a long-handled stick.", "The girls' lacrosse team practiced on the school field."],
    "language": ["The method of human communication.", "She is trying to learn a new language this year."],
    "lanky": ["Ungracefully thin and tall.", "The lanky basketball player could easily reach the hoop."],
    "lanyards": ["Cords or straps worn around the neck to carry something.", "We wore our camp identification cards on bright blue lanyards."],
    "lasagna": ["Pasta in the form of wide strips, usually cooked in layers.", "My mom made a delicious cheese lasagna for dinner."],
    "latticework": ["Work consisting of a lattice or laths of wood or metal.", "The porch was decorated with white wooden latticework."],
    "leaning": ["Being in a sloping position.", "The old tree was leaning toward the house."],
    "leather": ["A material made from the skin of an animal.", "He wore a warm leather jacket on the cold day."],
    "lessons": ["Periods of learning or teaching.", "She takes piano lessons every Tuesday after school."],
    "lilt": ["A characteristic rising and falling of the voice when speaking.", "He spoke with a cheerful lilt in his voice."],
    "limbs": ["Arms or legs of a person or four-legged animal.", "The monkey used its strong limbs to swing through the trees."],
    "lunacy": ["The state of being a lunatic; insanity.", "It would be absolute lunacy to drive in this blizzard."],
    "lurches": ["Makes an abrupt, unsteady, uncontrolled movement.", "The boat lurches forward as it hits a large wave."],
    "lure": ["To tempt a person or an animal to do something.", "He used a piece of cheese to lure the mouse into the trap."],
    "lye": ["A strongly alkaline solution used for washing or making soap.", "Be careful when handling lye, as it can burn your skin."],
    "magnanimous": ["Generous or forgiving, especially toward a rival.", "The winner was magnanimous and shook hands with his opponent."],
    "mango": ["A fleshy yellowish-red tropical fruit.", "She sliced a ripe mango for her fruit salad."],
    "manticores": ["Mythical beasts with the head of a man and the body of a lion.", "The book was filled with stories of manticores and dragons."],
    "maquisards": ["Members of the French Resistance during WWII.", "The maquisards hid in the mountains to plan their attacks."],
    "maracas": ["Small shakers made from gourds used as musical instruments.", "The children shook the maracas in time with the music."],
    "marauder": ["A person who marauds; a raider.", "The village was on high alert for any marauder in the woods."],
    "marquee": ["A large tent used for social functions.", "They set up a large marquee on the lawn for the wedding."],
    "mascot": ["A person or thing that is supposed to bring good luck.", "The school's mascot is a friendly bulldog named Buster."],
    "melon": ["A large round fruit with sweet pulpy flesh.", "We had slices of cold melon for a snack."],
    "memoirs": ["A historical account or biography written from personal knowledge.", "The famous actor published his memoirs last month."],
    "mercantile": ["Relating to merchants or trading.", "The town grew as a busy mercantile center."],
    "mermaid": ["A mythical sea creature with the tail of a fish.", "The little girl dressed up as a mermaid for the party."],
    "message": ["A verbal, written, or recorded communication.", "I left a message on the table for my mom."],
    "milk": ["An opaque white fluid rich in fat and protein.", "Would you like a glass of cold milk with your cookies?"],
    "mind": ["The element of a person that enables them to be aware.", "Try to keep an open mind about the new plan."],
    "miniature": ["A thing that is much smaller than normal.", "She collects miniature glass animals and keeps them on a shelf."],
    "minnows": ["Small freshwater fish.", "We saw a school of tiny minnows swimming in the creek."],
    "misanthrope": ["A person who dislikes humankind and avoids human society.", "The old man was a bit of a misanthrope and lived alone in the woods."],
    "moment": ["A very brief period of time.", "Please wait for just a moment while I finish this."],
    "monsieur": ["A title or form of address for a French-speaking man.", "The waiter addressed the customer as 'Monsieur'."],
    "monsoon": ["A seasonal prevailing wind in South and Southeast Asia.", "The monsoon brought heavy rains to the region."],
    "mosque": ["A Muslim place of worship.", "The mosque had a beautiful golden dome."],
    "moustache": ["A strip of hair grown by a man on his upper lip.", "He decided to grow a moustache for the winter."],
    "muffler": ["A scarf or wrap worn around the neck for warmth.", "She wrapped a thick wool muffler around her neck."],
    "mulberry": ["A small deciduous tree with broad leaves and purple berries.", "The silk worms ate the leaves of the mulberry tree."],
    "mustache": ["A strip of hair grown by a man on his upper lip.", "He used a comb to style his new mustache."],
    "mysterious": ["Difficult or impossible to understand.", "A mysterious light appeared in the sky at night."],
    "nautical": ["Of or concerning sailors or navigation.", "The room was decorated with a nautical theme, including anchors and ropes."],
    "nehru": ["A hip-length tailored coat with a mandarin collar.", "He wore a classic Nehru jacket to the formal event."],
    "neon": ["A fluorescent lighting tube.", "The neon signs of the city glowed brightly at night."],
    "nervous": ["Easily agitated or alarmed.", "She felt very nervous before her big speech."],
    "noggin": ["A person's head.", "He bumped his noggin on the low doorway."],
    "nomad": ["A person who does not stay long in the same place.", "The nomad traveled across the plains with his tent and horses."],
    "nomination": ["The action of nominating or being nominated.", "She was thrilled to receive a nomination for class president."],
    "oblivion": ["The state of being unaware or unconscious of what is happening.", "He drank the medicine and drifted off into oblivion."],
    "officially": ["In a formal and public way.", "The new park was officially opened by the mayor today."],
    "ominous": ["Giving the impression that something bad is going to happen.", "The dark, ominous clouds suggested a storm was coming."],
    "onslaught": ["A fierce or destructive attack.", "The village survived the onslaught of the heavy winter snow."],
    "opalescent": ["Showing varying colors like an opal.", "The shell had a beautiful opalescent finish."],
    "opportunist": ["A person who takes advantage of opportunities as they arise.", "The businessman was an opportunist who always found a way to succeed."],
    "ostracism": ["Exclusion from a society or group.", "The boy suffered from ostracism after he moved to the new school."],
    "oswego": ["A city and port in New York on Lake Ontario.", "The ships docked at the harbor in Oswego."],
    "paltry": ["Small or meager in amount.", "He was offered a paltry sum of money for his hard work."],
    "paparazzi": ["Photographers who follow famous people.", "The actress was surrounded by paparazzi as she left the restaurant."],
    "parachute": ["A device used to slow the fall of a person from an aircraft.", "The skydiver pulled the cord and his parachute opened."],
    "parchment": ["A stiff, flat, thin material made from animal skin used for writing.", "The ancient map was drawn on a piece of yellowed parchment."],
    "parent": ["A father or mother.", "Each student was asked to bring a parent to the school play."],
    "paste": ["A thick, soft, moist substance.", "He used white paste to stick the pictures into his book."],
    "patriarchs": ["The male heads of families or tribes.", "The patriarchs of the village met to discuss the new rules."],
    "pediatric": ["Relating to the medical care of children.", "She works as a nurse in the pediatric ward of the hospital."],
    "peppercorn": ["The dried berry of a pepper plant.", "He used a grinder to crush a whole peppercorn."],
    "perfume": ["A fragrant liquid typically made from essential oils.", "The room smelled like her favorite floral perfume."],
    "peroxide": ["A chemical compound used as a disinfectant or bleach.", "She used peroxide to clean the small cut on her finger."],
    "pheromone": ["A chemical substance produced and released into the environment by an animal.", "The ants follow a pheromone trail to find food."],
    "piccolo": ["A small flute sounding an octave higher than the ordinary one.", "She played a solo on the piccolo during the concert."],
    "pinioning": ["Tying or holding the arms or legs of someone.", "The wrestler was successful in pinioning his opponent to the mat."],
    "pirates": ["People who attack and rob ships at sea.", "The pirates searched for buried treasure on the desert island."],
    "pistachio": ["A small savory nut with an edible green kernel.", "I had a scoop of pistachio ice cream for dessert."],
    "pizzeria": ["A place where pizzas are made and sold.", "We went to the local pizzeria for dinner on Friday."],
    "plaid": ["Checkered or tartan twilled cloth.", "He wore a red and green plaid shirt."],
    "plaited": ["Formed into a braid or braids.", "She wore her long hair in two plaited strands."],
    "plausible": ["Seeming reasonable or probable.", "That seems like a plausible explanation for what happened."],
    "pogrom": ["An organized massacre of a particular ethnic group.", "Many families fled the country to escape the pogrom."],
    "pond": ["A small body of still water.", "We saw several ducks swimming in the pond."],
    "porridge": ["A dish made of oatmeal or another cereal boiled in water or milk.", "He had a bowl of hot porridge for breakfast."],
    "prattling": ["Talking at length in a foolish or inconsequential way.", "The baby was prattling away in her high chair."],
    "preamble": ["A preliminary or preparatory statement; an introduction.", "The lawyer read the preamble to the new contract."],
    "precocious": ["Having developed certain abilities at an earlier age than usual.", "The precocious child was playing chess at age five."],
    "premises": ["A house or building, together with its land and outbuildings.", "Please make sure to leave the premises by five o'clock."],
    "prestigious": ["Inspiring respect and admiration; having high status.", "She was accepted into a prestigious university."],
    "proficient": ["Competent or skilled in doing or using something.", "She is very proficient in playing the violin."],
    "prognosis": ["The likely course of a disease.", "The doctor gave a positive prognosis for his recovery."],
    "promenade": ["A paved public walk, typically one along a waterfront.", "We took a stroll along the seaside promenade."],
    "propaganda": ["Information of a biased nature used to promote a political cause.", "The government used propaganda to influence the public."],
    "prototype": ["A first or preliminary model of something.", "The engineers built a prototype of the new car."],
    "protégé": ["A person who is guided and supported by an older and more experienced person.", "The famous artist took the young student as his protégé."],
    "psyche": ["The human soul, mind, or spirit.", "The experience had a deep effect on his psyche."],
    "puissance": ["Great power, influence, or prowess.", "The kingdom was known for its military puissance."],
    "pumpernickel": ["A heavy, dark, slightly sour bread made from rye.", "She made a sandwich with a slice of pumpernickel bread."],
    "pâtisserie": ["A shop where French pastries and cakes are sold.", "We bought a dozen colorful macarons from the pâtisserie."],
    "quandary": ["A state of perplexity or uncertainty over what to do.", "I am in a quandary about which dress to wear to the party."],
    "quilt": ["A warm bed covering made of paddled sections of fabric.", "My grandmother made a beautiful patchwork quilt for my bed."],
    "raise": ["To lift or move something to a higher position.", "Please raise your hand if you know the answer."],
    "rakish": ["Having or displaying a dashing, jaunty, or slightly disreputable appearance.", "He wore his hat at a rakish angle."],
    "ramshackle": ["In a state of severe disrepair.", "The old ramshackle house looked like it might fall down."],
    "ratify": ["Sign or give formal consent to a treaty or contract.", "The two countries met to ratify the new peace treaty."],
    "ration": ["A fixed amount of a commodity allowed to each person.", "The soldiers were given a daily ration of food and water."],
    "receipts": ["A written acknowledgment that a specified article has been received.", "Make sure to keep your receipts in case you need to return something."],
    "receptionist": ["A person employed to greet visitors.", "The receptionist asked me to wait in the lobby."],
    "recipe": ["A set of instructions for preparing a particular dish.", "I followed a new recipe to make these cookies."],
    "reclusive": ["Avoiding the company of other people; solitary.", "The reclusive author rarely left his home."],
    "remind": ["Cause someone to remember someone or something.", "Please remind me to call my grandmother tomorrow."],
    "renowned": ["Known or talked about by many people; famous.", "The city is renowned for its beautiful parks."],
    "reprimanding": ["Rebuking someone, especially officially.", "The teacher was reprimanding the student for being late."],
    "repugnant": ["Extremely distasteful; unacceptable.", "The idea of eating insects was repugnant to him."],
    "residuals": ["Quantities remaining after other parts have been taken away.", "The actor received residuals every time the show was aired."],
    "rickety": ["Poorly made and likely to collapse.", "We carefully climbed the old, rickety stairs."],
    "riveted": ["Held someone or something fast so as to make them incapable of movement.", "She was riveted by the exciting story."],
    "roam": ["Move about or travel aimlessly.", "A herd of wild horses started to roam across the field."],
    "rotunda": ["A round building or room, especially one with a dome.", "The state capitol building has a large central rotunda."],
    "ruby": ["A precious stone of a deep red color.", "Her ring was set with a beautiful red ruby."],
    "ruefully": ["In a way that expresses sorrow or regret.", "He looked ruefully at the broken vase on the floor."],
    "rummage": ["Search unsystematically and untidily through a mass or receptacle.", "She started to rummage through her bag looking for her keys."],
    "safari": ["An expedition to observe or hunt animals in their natural habitat.", "They went on a safari in Africa to see lions and elephants."],
    "salvaged": ["Rescued from potential loss or destruction.", "They salvaged several items from the old house before it was torn down."],
    "samosas": ["Fried or baked pastries with a savory filling.", "We ordered a plate of spicy vegetable samosas."],
    "serape": ["A colorful woolen shawl or blanket worn in Mexico.", "The musician wore a traditional serape over his shoulders."],
    "sarape": ["A colorful woolen shawl or blanket worn in Mexico.", "The musician wore a traditional sarape over his shoulders."],
    "sardines": ["Small, silvery food fish related to the herring.", "He opened a tin of sardines for his lunch."],
    "sarsaparilla": ["A carbonated soft drink flavored with the root of a plant.", "He ordered a cold glass of sarsaparilla at the cafe."],
    "satin": ["A smooth, glossy fabric, typically of silk.", "She wore a beautiful pink satin dress to the dance."],
    "savant": ["A learned person, especially a distinguished scientist.", "The professor was a savant in the field of mathematics."],
    "scalpel": ["A small and extremely sharp bladed instrument used for surgery.", "The surgeon used a scalpel to make a precise cut."],
    "scavenger": ["An animal that feeds on carrion or refuse.", "A vulture is a common scavenger found in the desert."],
    "schema": ["A representation of a plan or theory in the form of an outline.", "The team developed a new schema for the project."],
    "scorcher": ["A very hot day.", "Today is a real scorcher, so make sure to drink plenty of water."],
    "scrub": ["Rub someone or something hard so as to clean them.", "I had to scrub the floor to get the muddy footprints off."],
    "scrunch": ["Make a soft crushing noise.", "The dry leaves began to scrunch under our feet."],
    "scurrying": ["Moving hurriedly with short quick steps.", "We saw a mouse scurrying across the kitchen floor."],
    "search": ["Try to find something by looking or otherwise seeking carefully.", "The police started a search for the missing boy."],
    "seep": ["Flow or leak slowly through porous material or small holes.", "Water began to seep through the crack in the ceiling."],
    "send": ["Cause to go or be taken to a particular destination.", "Don't forget to send a thank-you note to your aunt."],
    "sequins": ["Small, shiny disks sewn on as decoration.", "Her dress was covered in sparkling silver sequins."],
    "serape": ["A colorful woolen shawl or blanket worn in Mexico.", "The musician wore a traditional sarape over his shoulders."],
    "señor": ["A title or form of address for a Spanish-speaking man.", "The waiter addressed the guest as 'Señor'."],
    "sharks": ["Long-bodied predatory marine fish with a cartilaginous skeleton.", "We saw the fins of several sharks in the ocean."],
    "shimmer": ["Shine with a soft tremulous light.", "The stars began to shimmer in the night sky."],
    "shortcut": ["An alternative route that is shorter than the one usually taken.", "We took a shortcut through the woods to get home faster."],
    "shouting": ["Uttering a loud cry or call.", "The fans were shouting and cheering for their team."],
    "shuffle": ["Walk by dragging one's feet along or without lifting them fully.", "He started to shuffle his feet as he got tired."],
    "signal": ["A gesture, action, or sound that gives information.", "The referee blew his whistle as a signal to start the game."],
    "silhouette": ["The dark shape and outline of someone or something visible against a lighter background.", "We saw the silhouette of a tree against the setting sun."],
    "silver": ["A precious shiny grayish-white metal.", "She wore a shiny silver necklace with her blue dress."],
    "sinister": ["Giving the impression that something harmful or evil is happening.", "The old house had a sinister look in the moonlight."],
    "sizzling": ["Very hot.", "The bacon was sizzling in the hot pan."],
    "skater": ["A person who skates.", "The ice skater performed a perfect jump."],
    "skewer": ["A long metal or wooden pin used for holding chunks of food.", "He put pieces of chicken and peppers on a metal skewer."],
    "skirt": ["A garment fastened around the waist and hanging down around the legs.", "She wore a long floral skirt to the party."],
    "skittish": ["Excitable or easily scared.", "The skittish horse jumped when a bird flew by."],
    "slime": ["A moist, soft, and slippery substance.", "The snail left a trail of clear slime on the leaf."],
    "slough": ["A swamp.", "The hikers had to navigate around a muddy slough."],
    "sluice": ["A sliding gate or other device for controlling the flow of water.", "The workers opened the sluice to let water into the canal."],
    "snug": ["Comfortable, warm, and cozy.", "The baby was wrapped snug in a soft blanket."],
    "solemnly": ["In a formal and dignified manner.", "The witness solemnly promised to tell the truth."],
    "spectators": ["People who watch at a show, game, or other event.", "Thousands of spectators gathered to watch the parade."],
    "spinning": ["Turning or causing to turn or whirl around quickly.", "The top was spinning rapidly on the floor."],
    "sporadic": ["Occurring at irregular intervals or only in a few places.", "There were sporadic showers throughout the afternoon."],
    "squalor": ["The state of being extremely dirty and unpleasant.", "The abandoned building was filled with squalor and trash."],
    "stay": ["Remain in the same place.", "Please stay right here until I come back."],
    "steeple": ["A church tower and spire.", "The white church steeple could be seen from miles away."],
    "streetlights": ["Lights illuminating a road or public area.", "The streetlights came on as it started to get dark."],
    "stretch": ["Be made or be capable of being made longer or wider.", "I need to stretch my legs after the long car ride."],
    "stucco": ["Fine plaster used for coating wall surfaces.", "The house was finished with a layer of white stucco."],
    "stuck": ["Unable to move or be moved.", "The door was stuck and wouldn't open."],
    "studded": ["Decorated or augmented with studs.", "She wore a black leather jacket studded with silver."],
    "substantially": ["To a great or significant degree.", "The price of the car was substantially reduced."],
    "sugar": ["A sweet crystalline substance obtained from various plants.", "He added a spoonful of sugar to his coffee."],
    "surprise": ["An unexpected or astonishing event, fact, or thing.", "The party was a complete surprise to her."],
    "suspicious": ["Having or showing a cautious distrust of someone or something.", "The police were suspicious of the man's story."],
    "swaggering": ["Walking or behaving with a very confident and arrogant manner.", "The winner came swaggering into the room."],
    "swampy": ["Characteristic of a swamp; marshy or boggy.", "The ground was very wet and swampy near the lake."],
    "sweet": ["Having the pleasant taste characteristic of sugar.", "The ripe strawberries were very sweet and delicious."],
    "syndrome": ["A group of symptoms that consistently occur together.", "The doctor identified the rare syndrome after several tests."],
    "tackle": ["Make determined efforts to deal with a problem or task.", "I need to tackle my homework before I can play."],
    "taffy": ["A chewy candy made of boiled sugar or molasses.", "We bought a bag of saltwater taffy at the beach."],
    "tag": ["A children's game in which one player chases others.", "The children played a game of tag on the playground."],
    "tail": ["The hindmost part of an animal.", "The happy dog started to wag its tail."],
    "talcum": ["Talc in the form of a fine powder used on the skin.", "She used talcum powder to keep her skin dry."],
    "tamale": ["A Mexican dish of seasoned meat wrapped in cornmeal dough.", "He ordered a spicy pork tamale for his lunch."],
    "tank": ["A large container for storing liquid or gas.", "The fish were swimming in a large glass tank."],
    "teeth": ["Hard, enamel-coated structures in the jaws.", "Remember to brush your teeth twice a day."],
    "tender": ["Showing gentleness and concern or sympathy.", "The mother gave her baby a tender kiss on the forehead."],
    "thesaurus": ["A book that lists words in groups of synonyms.", "I used a thesaurus to find a better word for 'happy'."],
    "tight": ["Fixed, fastened, or closed firmly.", "Make sure to pull the knot tight."],
    "tint": ["A slight degree of a color.", "The sky had a beautiful pink tint at sunset."],
    "toiletries": ["Articles used in washing and taking care of one's body.", "He packed his toothbrush and other toiletries for the trip."],
    "tranquilizer": ["A medicinal drug taken to reduce tension or anxiety.", "The vet gave the nervous dog a mild tranquilizer."],
    "traumatic": ["Emotionally disturbing or distressing.", "The accident was a very traumatic experience for her."],
    "trebuchets": ["Machines used in medieval siege warfare for hurling large stones.", "The army used trebuchets to attack the castle walls."],
    "triple": ["Consisting of three parts, elements, or members.", "I'll have a triple scoop of ice cream, please!"],
    "tuberculosis": ["An infectious bacterial disease characterized by the growth of nodules in the lungs.", "The patient was treated for tuberculosis in the hospital."],
    "tucson": ["A city in southern Arizona.", "They spent their winter vacation in sunny Tucson."],
    "tulle": ["A soft, fine silk, cotton, or nylon net used for making veils.", "The ballerina's tutu was made of several layers of white tulle."],
    "turnout": ["The number of people attending or taking part in an event.", "There was a large turnout for the school play."],
    "tuxedo": ["A man's dinner jacket.", "He wore a formal black tuxedo to the wedding."],
    "twigs": ["Slender woody shoots growing from a branch or stem of a tree.", "The bird collected small twigs to build its nest."],
    "ultimatum": ["A final demand or statement of terms.", "The manager gave the workers an ultimatum to return to work."],
    "understand": ["Perceive the intended meaning of words, a language, or a person.", "I don't quite understand how to solve this problem."],
    "unfamiliar": ["Not known or recognized.", "The new city felt very unfamiliar to her."],
    "unicorn": ["A mythical horse with a single horn on its forehead.", "The magical forest was home to a shy white unicorn."],
    "unleash": ["Release from a leash or restraint.", "He decided to unleash the dog so it could run in the park."],
    "unparalleled": ["Having no parallel or equal; exceptional.", "The view from the top of the mountain was unparalleled."],
    "unruly": ["Disorderly and disruptive and not amenable to discipline.", "The teacher struggled to control the unruly class."],
    "vacuum": ["A space entirely devoid of matter.", "We used a vacuum cleaner to get the dust off the rug."],
    "valentine": ["A card sent to a person one loves on Valentine's Day.", "He sent a beautiful valentine to his girlfriend."],
    "verdict": ["A decision on a disputed issue in a civil or criminal case.", "The jury returned a verdict of 'not guilty'."],
    "vidimus": ["An inspection of a legal document.", "The lawyer performed a vidimus of the new contract."],
    "vigilance": ["The action or state of keeping careful watch for possible danger.", "The guard maintained his vigilance throughout the night."],
    "wainscoting": ["Wooden paneling that lines the lower part of the walls of a room.", "The dining room was decorated with elegant white wainscoting."],
    "want": ["Have a desire to possess or do something.", "I want to go to the park this afternoon."],
    "warlock": ["A man who practices witchcraft; a sorcerer.", "The story was about a powerful warlock who lived in a tower."],
    "weather": ["The state of the atmosphere at a place and time.", "The weather was sunny and warm all day."],
    "wheels": ["Circular objects that revolve on an axle.", "The bicycle has two large wheels."],
    "whinnying": ["Making a gentle, high-pitched neigh.", "The horse started whinnying when it saw its owner."],
    "whittled": ["Carved an object from wood by cutting small slices from it.", "The old man whittled a small bird out of a piece of cedar."],
    "window": ["An opening in a wall or door that is fitted with glass.", "Please open the window to let in some fresh air."],
    "winsome": ["Attractive or appealing in appearance or character.", "She had a bright and winsome smile."],
    "wire": ["Metal drawn out into the form of a thin flexible thread.", "He used a piece of wire to fix the broken fence."],
    "wooden": ["Made of wood.", "The table was made of heavy wooden planks."],
    "woozy": ["Unsteady, dizzy, or dazed.", "She felt a bit woozy after getting off the spinning ride."],
    "writing": ["The activity or skill of marking coherent words on paper.", "She spent the afternoon writing a story in her notebook."],
    "yawn": ["Involuntarily open one's mouth wide and inhale deeply.", "He couldn't help but yawn during the long movie."],
    "yiddish": ["A language used by Jews in central and eastern Europe before the Holocaust.", "Her grandmother often spoke to her in Yiddish."],
    "zeal": ["Great energy or enthusiasm in pursuit of a cause or an objective.", "He worked with great zeal to finish the project on time."],
    "zombielike": ["Resembling a zombie; mechanical or lacking in awareness.", "The tired students walked into class in a zombielike state."],
    "zooming": ["Moving or traveling very quickly.", "The cars were zooming past us on the highway."]
}

# --- 2. UPDATED GET INFO FUNCTION (THE KEY FIX) ---
def get_word_info(word):
    """
    Cleans the input word to ensure it matches the WORD_DATA keys perfectly.
    """
    # 1. Convert to lowercase
    # 2. Remove leading/trailing spaces
    # 3. Remove any trailing punctuation (like asterisks from the PDF)
    clean_key = word.lower().strip().replace("*", "")
    
    if clean_key in WORD_DATA:
        return WORD_DATA[clean_key]
    else:
        return [
            f"Definition currently being updated in the Bee database for '{word}'.", 
            f"Study Tip: Try to find the word '{word}' in a sentence online!"
        ]

# --- ADD THIS HELPER FUNCTION ---
def get_tts_audio(word):
    """Converts word to audio bytes and encodes to base64 for Streamlit."""
    tts = gTTS(text=word, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    return base64.b64encode(fp.getvalue()).decode()

# --- 3. STREAMLIT APP LOGIC ---

# Initialize session state variables if they don't exist
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
    st.session_state.round = 0
    st.session_state.score = 0
    st.session_state.wrong_list = []
    st.session_state.current_pool = []
    st.session_state.mode = "Challenge (Test Mode)"

# --- SCREEN 1: SETUP ---
if not st.session_state.game_active and st.session_state.round == 0:
    st.title("🐝 Fun Spelling Bee Trainer")
    
    word_options = {}
    word_options["3rd Grade List"] = POOL_3RD
    
    for i, chunk in enumerate(chunks_one):
        word_options[f"One Bee - Part {i+1}"] = chunk
    for i, chunk in enumerate(chunks_two):
        word_options[f"Two Bee - Part {i+1}"] = chunk
    for i, chunk in enumerate(chunks_three):
        word_options[f"Three Bee - Part {i+1}"] = chunk

    mode = st.radio("Choose Mode:", ["Study (Learning)", "Challenge (Test Mode)"])
    level = st.selectbox("Select Word Set:", list(word_options.keys()))
    
    if st.button("Start Session"):
        full_chunk = word_options[level]
        
        if mode == "Challenge (Test Mode)":
            sample_size = min(10, len(full_chunk))
            st.session_state.current_pool = random.sample(full_chunk, sample_size)
        else:
            st.session_state.current_pool = full_chunk
            
        st.session_state.mode = mode
        st.session_state.game_active = True
        st.session_state.round = 0
        st.session_state.score = 0
        st.session_state.wrong_list = []
        
        # Cleanup audio flags
        keys_to_clear = [k for k in st.session_state.keys() if k.startswith("submitted_")]
        for k in keys_to_clear: 
            del st.session_state[k]
        st.rerun()

# --- SCREEN 2: ACTIVE SESSION ---
elif st.session_state.game_active:
    pool = st.session_state.current_pool
    
    if st.session_state.round < len(pool):
        current_word = pool[st.session_state.round]
        b64_audio = get_tts_audio(current_word)
        timestamp = time.time()
        audio_html = f'<audio autoplay key="{timestamp}" src="data:audio/mp3;base64,{b64_audio}">'
        
        # --- BRANCH A: STUDY MODE ---
        if st.session_state.mode == "Study (Learning)":
            st.header("📖 Study Mode")
            target_clean = current_word.strip().replace("*", "")
            spelling_letters = " . ".join(list(target_clean.upper()))
            combined_text = f"{target_clean}... {spelling_letters}... {target_clean}"
            
            b64_combined = get_tts_audio(combined_text)
            st.markdown(f'<audio autoplay key="s_{timestamp}"><source src="data:audio/mp3;base64,{b64_combined}"></audio>', unsafe_allow_html=True)
            
            info = get_word_info(current_word)
            st.divider()
            st.title(current_word.capitalize())
            
            if st.button("🔊 Re-play", key=f"rep_{st.session_state.round}"):
                st.rerun()

            st.info(f"**Meaning:** {info[0]}")
            st.success(f"**Sample Sentence:** *{info[1]}*")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⬅️ Previous") and st.session_state.round > 0:
                    st.session_state.round -= 1
                    st.rerun()
            with col2:
                if st.button("Next ➡️"):
                    st.session_state.round += 1
                    if st.session_state.round >= len(pool):
                        st.session_state.game_active = False
                    st.rerun()
            with col3:
                if st.button("Quit Study"):
                    st.session_state.game_active = False
                    st.session_state.round = 0
                    st.rerun()

        # --- BRANCH B: CHALLENGE MODE ---
        else:
            st.header("✍️ Spelling Challenge")
            audio_placeholder = st.empty()
            
            if f"submitted_{st.session_state.round}" not in st.session_state:
                with audio_placeholder:
                    st.markdown(audio_html, unsafe_allow_html=True)
            
            st.write(f"Word {st.session_state.round + 1} of {len(pool)}")
            if st.button("🔊 Repeat Word", key=f"c_rep_{st.session_state.round}"):
                st.rerun()

            user_ans = st.text_input("Type your spelling here:", key=f"in_{st.session_state.round}").strip()

            if st.button("Submit", key=f"sub_{st.session_state.round}", type="primary"):
                if user_ans:
                    audio_placeholder.empty()
                    st.session_state[f"submitted_{st.session_state.round}"] = True
                    target = current_word.lower().strip().replace("*", "")
                    processed_ans = user_ans.lower().replace("-", "").replace(" ", "")
                    
                    if processed_ans == target:
                        st.success(f"✅ Correct! **{target.upper()}**")
                        st.session_state.score += 1
                        time.sleep(1.2)
                    else:
                        st.error(f"❌ Incorrect. Correct: **{target.upper()}**")
                        st.session_state.wrong_list.append(current_word)
                        time.sleep(3.0)

                    st.session_state.round += 1
                    if st.session_state.round >= len(pool):
                        st.session_state.game_active = False
                    st.rerun()
                else:
                    st.warning("Please type the word.")

# --- SCREEN 3: RESULTS / SUMMARY ---
elif not st.session_state.game_active and st.session_state.round > 0:
    st.balloons()
    st.title("🏁 Session Complete!")
    
    total_words = len(st.session_state.current_pool)
    score = st.session_state.score
    percentage = int((score / total_words) * 100) if total_words > 0 else 0
    
    if percentage == 100:
        st.success("🌟 PERFECT SCORE! You are a Spelling Bee Champion! 🌟")
    elif percentage >= 80:
        st.info("🎈 Amazing job! You've almost mastered this list! 🎈")
    else:
        st.error("💪 Keep practicing! Review below.")

    col1, col2 = st.columns(2)
    col1.metric("Correct", f"{score} / {total_words}")
    col2.metric("Grade", f"{percentage}%")

    if st.session_state.wrong_list:
        st.subheader("📝 Review Missed Words")
        for word in sorted(set(st.session_state.wrong_list)):
            meaning, sentence = get_word_info(word)
            with st.expander(f"📖 {word.upper()}", expanded=True):
                st.write(f"**Meaning:** {meaning}")
                st.write(f"**Example:** {sentence}")

    if st.button("Return to Main Menu"):
        st.session_state.game_active = False
        st.session_state.round = 0
        st.rerun()
