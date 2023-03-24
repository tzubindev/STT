import string
import nltk
import json
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

wnl = WordNetLemmatizer()
tags = dict()
data = None
validLem = ["noun", "verb", "adverb", "adjective"]
validLem_code = ["n", "v", "r", "a"]
isTag = True
pair_key = None

# preload tags
with open("./data/tags.json") as f:
    data = json.loads(f.read())["tags"]

for tag in data:
    tags[tag["tag"]] = "".join([c for c in tag["meaning"] if c != ","]).lower()


class TextProcessing:
    def __init__(self, sentence) -> None:
        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(sentence)
        self.original_s = sentence
        self.s = " ".join(
            [
                w.lower()
                .replace("'m", " am")
                .replace("n't", " not")
                .replace("'s", "")
                .replace("'ve", " have")
                .strip("0123456789")
                .strip(string.punctuation)
                for w in word_tokens
                if w.lower() not in self.stop_words
            ]
        )

    def getProcessedSentence(self):
        label = self.s

        words = nltk.pos_tag(WhitespaceTokenizer().tokenize(label))
        processed_sentence = ""

        for comb in words:
            # print(comb)
            word, tag = comb

            tags_sep = tags[tag].split()
            target = None
            for v in validLem:
                if v in tags_sep:

                    for i in range(4):
                        if validLem[i] in tags_sep:
                            target = validLem_code[i]
                    word = wnl.lemmatize(word.lower(), target)
            processed_sentence += f"{word} "

        return processed_sentence.strip()

    def getWordCounts(self):
        from textblob import TextBlob

        blob = TextBlob(self.original_s)

        counts = dict()
        for word in [w for w in blob.words if w.lower() not in self.stop_words]:
            counts[word] = blob.word_counts[word]

        return counts
