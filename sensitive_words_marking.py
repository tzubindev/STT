from text_processing import TextProcessing
from textblob import TextBlob
import spacy
import re


class SensitiveWordsMarking:
    def __init__(self, processed_sentence) -> None:
        self.processed_sentence = processed_sentence.split()
        self.result = dict()
        self.nlp = spacy.load("en_core_web_lg")

    def checkMatchedWords(self):

        sentence = " ".join([key for key, value in self.result.items()]).strip()

        blob = TextBlob(sentence)

        for key, val in self.result.items():
            oldVal = val
            newVal = []
            self.result[key] = None
            for item in oldVal:
                item = str(item)
                sizeItem = len(item.split(" "))
                foundWord = []
                if sizeItem > 1:
                    for comb in blob.ngrams(n=sizeItem):
                        foundWord += re.findall(" ".join(comb), item)
                else:
                    foundWord += re.findall(key, item)

                if len(foundWord) > 0 and foundWord[0] not in newVal:
                    newVal += foundWord

            self.result[key] = newVal

    def mark(self):
        for key, val in self.result.items():
            if val == True or val == False:
                continue

            if len(val) > 1:
                for item in val:
                    items = str(val[0]).split(" ")
                    if len(items) == 1:
                        self.result[key] = True
                    else:
                        for i in items:
                            self.result[i] = True
            else:
                if len(val) == 1:
                    items = str(val[0]).split(" ")
                    if len(items) == 1:
                        self.result[key] = True
                    else:
                        for i in items:
                            self.result[i] = True
                else:
                    self.result[key] = False

    def getMarkedObj(self):
        sWords = None
        with open("./data/sensitive_words.txt") as f:
            sWords = [line.strip() for line in f.readlines()]

        SIZE = int(len(sWords) / 7)

        for word in self.processed_sentence:
            a = self.nlp(word)
            sensitive_words = []

            for i in range(0, SIZE):

                similarities = dict()

                for j in range(7):
                    foo = self.nlp(sWords[SIZE * j + i])
                    if foo.vector_norm:
                        similarities[foo] = a.similarity(foo)

                for key, value in similarities.items():
                    if value >= 0.8:
                        sensitive_words.append(key)

            self.result[word] = sensitive_words

        self.checkMatchedWords()
        self.mark()
        return self.result
