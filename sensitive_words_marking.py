import spacy
import nltk


class SensitiveWordsMarking:
    def __init__(self, word) -> None:
        self.word = word
        self.result = dict()
        self.nlp = spacy.load("en_core_web_sm")
        self.marking()

    def search(self, wordsArr, character):
        start = 0
        end = len(wordsArr) - 1

        while start <= end:
            mid = start + (end - start) // 2

            if str(wordsArr[mid])[0].lower() > character:
                end = mid - 1
            elif str(wordsArr[mid])[0].lower() < character:
                start = mid + 1
            else:
                return mid

        return -1

    def marking(self):
        sWords = None
        with open("./data/sensitive_words.txt") as f:
            sWords = [line.strip() for line in f.readlines()]
        sWords = sorted(sWords)

        word = self.word

        # Binary Search Algo
        target_ch = str(word[0]).lower()
        searchIndex = self.search(sWords, target_ch)
        endIndex = searchIndex + 1
        if searchIndex == -1:
            self.result = False
            return

        while sWords[searchIndex - 1][0] == target_ch:
            searchIndex -= 1

        while sWords[endIndex][0] == target_ch:
            endIndex += 1

        a = self.nlp(word)

        sensitive_words = [sWords[i] for i in range(searchIndex, endIndex)]

        for w in sensitive_words:
            if nltk.edit_distance(str(a), str(w)) > 5:
                continue
            w = self.nlp(w)
            if w.vector_norm:
                if a.similarity(w) > 0.8:
                    self.result = True
                    return

        self.result = False

    def isSensitiveWord(self):
        return self.result
