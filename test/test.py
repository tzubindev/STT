from sensitive_words_marking import SensitiveWordsMarking
from text_processing import TextProcessing

import webbrowser
import os

# most frequent words
# sentiment
if __name__ == "__main__":
    while True:
        result = SensitiveWordsMarking(
            TextProcessing(input("Enter your sentence here: ")).getProcessedSentence()
        ).getMarkedObj()

        sentence = " ".join(result.keys()).strip()

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
                    <div class="w-3/4 m-auto h-auto grid grid-cols-8 p-4 text-center gap-8">"""

        content = ""
        for key, value in result.items():
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

        with open("./output/test.html", "w") as f:
            f.write(head + content + tail)

        # to get the current working directory
        directory = os.getcwd()
        webbrowser.open(directory + "/output/test.html")
