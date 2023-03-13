from text_processing import TextProcessing
from textblob import TextBlob
import spacy
import re
import nltk


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

    def getMarkedObj(self):
        sWords = None
        with open("./data/sensitive_words.txt") as f:
            sWords = [line.strip() for line in f.readlines()]
        sWords = sorted(sWords)

        for word in self.processed_sentence:

            # Binary Search Algo
            target_ch = str(word[0]).lower()
            searchIndex = self.search(sWords, target_ch)
            if searchIndex == -1:
                self.result[word] = []
                continue

            while sWords[searchIndex - 1][0] == target_ch:
                searchIndex -= 1

            endIndex = searchIndex
            while sWords[endIndex][0] == target_ch:
                endIndex += 1

            a = self.nlp(word)

            sensitive_words = [sWords[i] for i in range(searchIndex, endIndex)]
            result_words = []

            for w in sensitive_words:
                if nltk.edit_distance(str(a), str(w)) > 5:
                    continue
                w = self.nlp(w)
                if w.vector_norm:
                    if a.similarity(w) > 0.8:
                        result_words.append(str(w))

            self.result[word] = result_words

        self.checkMatchedWords()
        self.mark()
        return self.result

    def getMarkedHTML(self):
        head = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Text Analysis</title>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="w-screen h-screen overflow-x-hidden flex flex-col p-8">
                <h1 class="w-full h-auto block text-center text-2xl font-bold">Senstive Words Marking</h1>
                <div class="grow flex items-center">
                    <div class="w-3/4 m-auto h-auto grid grid-cols-8 p-4 text-center gap-4">"""

        content = ""
        for key, value in self.result.items():
            content += "<div "
            if value:
                content += "class='border-t-4 border-red-500'"
            else:
                content += "class='border-t-4 border-green-500'"
            content += ">" + key + "</div>"

        tail = """
                    </div>
                </div>
            </body>
        </html>
                """

        return head + content + tail

    def hasSensitiveWord(self):
        for key, value in self.result.items():
            if value:
                return True

        return False
