import string
import nltk
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

wnl = WordNetLemmatizer()
tags = dict()
validLem = ["noun", "verb", "adverb", "adjective"]
validLem_code = ["n", "v", "r", "a"]
isTag = True
pair_key = None

# preload tags
with open("./data/tags.json", "r") as f:
    for line in f:
        line = line.strip()
        if line[0] not in ["[", "]", "{", "}"]:
            data = " ".join(line.split('"tag":')).replace('"', "")

            if isTag:
                data = " ".join(line.split('"tag":')).replace('"', "").strip()
                pair_key = data[:-1]
            else:
                data = (
                    " ".join(line.split('"meaning":'))
                    .replace('"', "")
                    .strip()
                    .replace(",", "")
                )
                tags[pair_key] = data
            isTag = not isTag


class TextProcessing:
    def __init__(self, sentence) -> None:
        nltk.download("stopwords")
        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(sentence)
        self.s = " ".join([w for w in word_tokens if w.lower() not in stop_words])

    def getProcessedSentence(self):
        label = self.s
        label = (
            label.replace("'m", " am")
            .replace("n't", " not")
            .replace("'s", "")
            .replace("'ve", " have")
        )
        # print(label)
        new_label = ""
        for char in label:
            if char in string.punctuation:
                new_label += " " + char + " "
            else:
                new_label += char

        words = nltk.pos_tag(WhitespaceTokenizer().tokenize(new_label))
        processed_sentence = ""
        new_label = new_label.lower()  # remove CAPT

        for comb in words:
            # print(comb)
            word, tag = comb

            word = word.strip("0123456789")  # remove NUM
            word = word.strip(string.punctuation)  # remove PUNC

            tags_sep = tags[tag].split()
            target = None
            for v in validLem:
                if v in tags_sep:

                    for i in range(4):
                        if validLem[i] in tags_sep:
                            target = validLem_code[i]
                    word = wnl.lemmatize(word.lower(), target)
            processed_sentence += f"{word} "

        processed_sentence = " ".join(processed_sentence.strip().split())
        return processed_sentence

    def getWordCounts(self):
        from textblob import TextBlob

        blob = TextBlob(self.s)
        counts = dict()
        for word in blob.words:
            word = str(word).lower()
            counts[word] = blob.word_counts[word]

        return counts
