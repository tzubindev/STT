from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import random
import math
from text_processing import TextProcessing
import time

# start_time = time.time()
# Additional Data => 2000 more data (1000->pos, 1000->neg)
# lines = []
# cnt = 0

# training_rate = 0.95

# train_data = data[: math.ceil(len(data) * training_rate)]
# test_data = data[math.ceil(len(data) * training_rate) :]

# print(f"Data Size: {len(data)}")
# print(f"Train Data Size: {len(train_data)}")
# print(f"Test Data Size: {len(test_data)}")
# print(f"Test/Train Ratio: {len(test_data)/len(train_data)}")


class NaiveBayes:
    def __init__(self) -> None:
        data_files = [
            "./data/amazon_cells_labelled.txt",
            "./data/imdb_labelled.txt",
            "./data/yelp_labelled.txt",
            "./data/self-defined.txt",
        ]
        processed_data = dict()
        lines = []

        for file in data_files:
            with open(file, "r", encoding="utf-8") as f:
                readlines = f.readlines()
                for line in readlines:
                    lines.append(line)

        for line in lines:
            label = line.rstrip()[:-1].rstrip()
            feature = line.rstrip()[-1]

            # print(TextProcessing(label).getProcessedSentence())
            processed_data[TextProcessing(label).getProcessedSentence()] = int(feature)

        data = [(sentence, processed_data[sentence]) for sentence in processed_data]
        random.shuffle(data)
        training_data = data[:1]
        # training_data = data

        self.cl = NaiveBayesClassifier(training_data)

    def getClassifier(self):
        return self.cl

    def classifySentences(self, sentences):
        sentiments = []

        blob= TextBlob(sentences)

        for s in blob.sentences:

            sentiments.append(
                self.cl.classify(TextProcessing(str(s)).getProcessedSentence())
            )
        positiveCounter = 0
        negativeCounter = 0
        counter = 0
        for n in sentiments:
            counter +=1


        for n in sentiments:
            if n == 1:
                positiveCounter += 1
            else:
                negativeCounter += 1

        positivePercent = positiveCounter / counter
        negativePercent = negativeCounter / counter

        return {"Negative": negativePercent, "Positive": positivePercent}


# Analysis Purpose

# # # for (sentence, label) in test_data:
# # #     prob_dist = cl.prob_classify(sentence)
# # #     print(f"{sentence}: {prob_dist.max()}")

# print(f"Accuracy: {cl.accuracy(test_data)}")

# accuracy_arr = []
# NUM_OF_TEST = 20

# if __name__ == "__main__":
#     while True:
#         ans = input("Please Enter Your Sentence: ")
#         blob = TextBlob(ans, classifier=cl)
#         print(f"Your Sentence's sentiment: {blob.classify()}")

# title = "|Accuracy Testing|"

# print()
# print("=" * len(title))
# print(title)
# print("=" * len(title))
# print()

# while cnt != NUM_OF_TEST:
#     random.shuffle(data)
#     train_data = data[: math.ceil(len(data) * training_rate)]
#     test_data = data[math.ceil(len(data) * training_rate) :]
#     cl = NaiveBayesClassifier(train_data)
#     accuracy = cl.accuracy(test_data)
#     print(f"Case {cnt+1} Accuracy: {accuracy}")
#     cnt += 1
#     accuracy_arr.append(accuracy)

# title = "|Summary Info|"

# print()
# print("=" * len(title))
# print(title)
# print("=" * len(title))
# print()

# accuracy_arr = sorted(accuracy_arr)

# N = len(accuracy_arr)
# U = sum(accuracy_arr) / N

# # [1] Calculating Standard Deviation
# SD = math.sqrt(sum([(i - U) ** 2 for i in accuracy_arr]) / N)

# # [2] Calculating Average Absolute Deviation
# AAD = sum([abs(i - U) for i in accuracy_arr]) / N

# MAX_VALUE = max(accuracy_arr)
# MIN_VALUE = min(accuracy_arr)
# MAX_DIFFERENCE = MAX_VALUE - MIN_VALUE
# LESSER_THAN_80 = []
# GREATER_THAN_AVR = []

# for i in accuracy_arr:
#     if i < 0.8:
#         LESSER_THAN_80.append(i)
#     if i > U:
#         GREATER_THAN_AVR.append(i)


# # Print Valued Info
# print(f"Average Value \t\t\t: {round(U,4)}")
# print(f"Standard Deviation \t\t: {round(SD,4)}")
# print(f"Average Absolute Deviation \t: {round(AAD,4)}")
# print(f"Max Value \t\t\t: {round(MAX_VALUE,4)}")
# print(f"Min Value \t\t\t: {round(MIN_VALUE,4)}")
# print(f"Max Difference \t\t\t: {round(MAX_DIFFERENCE,4)}")
# print(f"< 80 \t\t\t\t: LENGTH [{len(LESSER_THAN_80)}] => {LESSER_THAN_80}")
# print(f"> Avr \t\t\t\t: LENGTH [{len(GREATER_THAN_AVR)}] => {GREATER_THAN_AVR}")
# end_time = time.time() - start_time
# print(f"Total Execution Time \t\t: {end_time} seconds")
# print(f"Average Execution Time \t\t: {end_time / NUM_OF_TEST } seconds")
# print()
