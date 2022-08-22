### Here's the code for the AI generation.

import nltk
from nltk import everygrams
from re import search
from nltk.lm import MLE
import random

nltk_data_path = "assets/nltk_data"
if nltk_data_path not in nltk.data.path:
    nltk.data.path.append(nltk_data_path)
    

def load_data():
    """
    Load text data from a file and produce a list of token lists
    """
    
    sentences = []
    
    with open("plot_training.txt", "r", encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            if search('[a-zA-Z]', line):
                line = nltk.word_tokenize(line.lower())
                sentences.append(line)

    return sentences


def build_vocab(sentences):
    """
    Take a list of sentences and return a vocab
    """
    
    vocab = ['<s>', '</s>']
    
    for sentence in sentences:
        for token in sentence:
            if token not in vocab:
                vocab.append(token)
    
    return vocab



def build_ngrams(n, sentences):
    """
    Take a list of unpadded sentences and create all n-grams as specified by the argument "n" for each sentence
    """
    
    padding_sentences = []

    all_ngrams = []

    start_pad = '<s>'
    end_pad = '</s>'

    for sentence in sentences:
        new_sentence = []
        if n >= 2:
            for x in range(n-1):
                new_sentence.append(start_pad)
        for token in sentence:
            new_sentence.append(token)
        if n >= 2:
            for x in range(n-1):
                new_sentence.append(end_pad)
        padding_sentences.append(new_sentence)

    for pad_sentence in padding_sentences:
        all_ngrams.append(list(everygrams(pad_sentence, min_len=n, max_len=n)))


    return all_ngrams

def bigram_next_token(start_tokens=("<s>", ) * 3):
    """
    Take some starting tokens and produce the most likely token that follows under a bi-gram model
    """
    
    next_token, prob = None, None
    
    data = load_data()
    n=len(start_tokens) + 1
    ngrams = build_ngrams(n, data)

    total_count = 0
    freq_dict_matches ={}
    
    for line in ngrams:
        for x in range(len(line)):
            if start_tokens == (line[x][0:len(start_tokens)]):
                total_count += 1
                if line[x] in freq_dict_matches:
                    freq_dict_matches[line[x]] += 1
                else:
                    freq_dict_matches[line[x]] = 1

    top_value, top_key = (max(zip(freq_dict_matches.values(), freq_dict_matches.keys())))
    prob = top_value/total_count
    next_token = top_key[-1]
    
    
    return next_token, prob

def train_ngram_lm(n):
    """
    Train a n-gram language model as specified by the argument "n"
    """
    
    lm = MLE(n)
    
    data = load_data()
    train = build_ngrams(n, data)
    vocab = build_vocab(data)
    
    lm.fit(train, vocab)
    
    
    return lm

def string_cleaner(str):
    str = str.capitalize()
    
    str = str.replace("""</s>""", """""")
    str = str.replace("""<s>""", """""")
    
    str = str.replace(""" ,""", """,""")
    str = str.replace(""" n't""", """n't""")
    str = str.replace(""" ’""", """'""")
    str = str.replace("""’ """, """'""")
    str = str.replace("""' """, """'""")
    str = str.replace(""" '""", """'""")
    str = str.replace("""` """, """'""")
    str = str.replace(""" `""", """'""")    
    str = str.replace(""" :""", """:""")
    str = str.replace(""" .""", """.""")
    str = str.replace(""" !""", """!""")
    str = str.replace(""" ;""", """;""")
    str = str.replace(""" ?""", """?""")
    str = str.replace(""" )""", """)""")
    str = str.replace("""( """, """(""")
    
    
    str = str.replace("talia", "Talia")
    str = str.replace("mae", "Mae")
    str = str.replace("placer", "Placer")
    str = str.replace("placeholder", "Placeholder")
    str = str.replace("tracey", "Tracey")
    str = str.replace("madeline", "Madeline")
    str = str.replace("nyala", "Nyala")
    str = str.replace("sarah", "Sarah")
    str = str.replace("cadence", "Cadence")
    str = str.replace("dani", "Dani")
    str = str.replace("hib", "Hib")
    str = str.replace("amara", "Amara")
    str = str.replace("estelle", "Estelle")
    
    
    return str

def build_limited_vocab(sentences, exclusions):
    """
    Take a list of sentences and return a vocab
    """
    
    vocab = ['<s>', '</s>']
    
    for sentence in sentences:
        for token in sentence:
            if token not in vocab:
                vocab.append(token)
                
    try:
        for word in exclusions:
            vocab.remove(word)
    except ValueError:
        return vocab
    return vocab


def train_limited_ngram_lm(n, exclusions):
    """
    Train a n-gram language model as specified by the argument "n"
    """
    
    lm = MLE(n)
    
    data = load_data()
    train = build_ngrams(n, data)

    clean_train = []
    for sentence in train:
        new_sentence = [gram for gram in sentence if not any(excl in gram for excl in exclusions)]
        clean_train.append(new_sentence)
    vocab = build_limited_vocab(data, exclusions)
    
    lm.fit(clean_train, vocab)
    
    
    return lm


def multi_plot(num_sentences):
    paragraph = []
    for i in range(num_sentences):
        paragraph.append(two_seed_generator([],[]))
    return (" ".join(paragraph))


def two_seed_generator(feeder, exclusions):
    seed_list = []
    excl_list = []
    
    if feeder != None:
        seed_list = feeder.split()
        
    if exclusions != None:
        excl_list = exclusions.split()
    
    
    if len(seed_list) == 0:
        seed1 = "<s>"
        seed2 = "<s>"
    elif len(seed_list) == 1:
        seed1 = "<s>"
        seed2 = seed_list[0]
    else:
        seed1 = seed_list[0]
        seed2 = seed_list[1]
    
    
    n=3
    num_words=60
    text_seed=[seed1]+[seed2]
    lm = train_limited_ngram_lm(n, excl_list)
    output = []

    if seed1 != "<s>":
        output.append([seed1])
    if seed2 != "<s>":
        output.append([seed2])
        
    success=0
    tries=0
    error_msg= '<:ruri_no:921119263547326515>'
    
    while success==0:
        try:
            line = lm.generate(num_words, text_seed=text_seed)
            success=1
        except ValueError:  # the generation is not always successful. need to capture exceptions
            tries += 1
            if tries < 50:
                continue
            else:
                return error_msg
    
    output.append(line)
    
    out = [item for sublist in output for item in sublist]

    str_out = " ".join(out)
    sent_out = str_out.split('.')[0] +"."
    cleaned = string_cleaner(sent_out)
    
    return cleaned

def string_parser(str="<s>"):
    
    seed_list = []
    excl_list = []

    if '-' in str:
        left, right = str.split("-")

        excl_list = right.split()

        seed_list = left.split()

    else:
        seed_list = str.split()


    return seed_list, excl_list

def plot_better(str):
    seed_list, excl_list = string_parser(str)
    output = two_seed_generator(seed_list, excl_list)
    return output


def verb():
    verbs=[]
    with open("verbs_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            verbs.append(line)
    output = random.choice(verbs)
    return output

def noun():
    noun=[]
    with open("noun_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            noun.append(line)
    output = random.choice(noun)
    return output

def person():
    person=[]
    with open("person_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            person.append(line)
    output = random.choice(person)
    return output

def place():
    place=[]
    with open("places_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            place.append(line)
    output = random.choice(place)
    return output

def adj():
    adj=[]
    with open("adj_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            adj.append(line)
    output = random.choice(adj)
    return output

def adv():
    adv=[]
    with open("adv_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            adv.append(line)
    output = random.choice(adv)
    return output

def color():
    color=[]
    with open("color_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            color.append(line)
    output = random.choice(color)
    return output

def emote():
    emote=[]
    with open("emote_list.txt", "r", encoding="utf8") as f:
        for line in f:
            line = line[:-1]
            emote.append(line)
    output = random.choice(emote)
    return output


def filler(str):
    str_list = str.split()
    out_list = []
    for word in str_list:
        if word.lower() == "verb":
            out_list.append(verb())
        elif word.lower() == "noun":
            out_list.append(noun())
        elif word.lower() == "person":
            out_list.append(person())
        elif word.lower() == "place":
            out_list.append(place())
        elif word.lower() == "adj":
            out_list.append(adj())
        elif word.lower() == "adv":
            out_list.append(adv())
        elif word.lower() == "color":
            out_list.append(color())
        elif word.lower() == "emotion":
            out_list.append(emote())             
        else:
            out_list.append(word)
    str_out = " ".join(out_list)
    
    return str_out


def baka():
    response_list = ['...bakabakka.', 'Baka, baka, minna baka.', "I guess we're *all* idiots.", "...By the way, the enemy's attacking.", "Fools.", "Baka."]
    output = random.choice(response_list)
    return output

def roll(num, sides):
    n = int(num)
    s = int(sides)
    rolls = []
    for i in range(n):
        rolls.append(random.randint(1, s))
    val = sum(rolls)
    if n == 1 and sum(rolls) == 1:
        return("Ouch, crit fail. You rolled a **1**. Better luck next time!")
    else:
        return("Rolling " + str(num) + "d" + str(sides) + ": **" + str(val) + "**")
        
def star(msg):
    with open("starred.txt", "a") as file:
        file.write(msg)
        file.write("\n")
