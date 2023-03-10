import subprocess
import whisper
import requests
import os


class Transcribe:
    def __init__(self, url, isAudioFile=False) -> None:
        self.url = url
        self.isAudioFile = isAudioFile

    def getText(self):
        root_file_name = "audio_0"
        audio_file = None

        try:
            if not self.isAudioFile:
                while os.path.exists(root_file_name + ".mp3"):
                    names = root_file_name.split("_")
                    names[1] = int(names[1]) + 1
                    root_file_name = "_".join(names)

                audio_file = root_file_name + ".mp3"
                # audio_file = "/tmp/" + root_file_name + ".mp3"

                # subprocess.Popen(["./create-file.sh %s" % audio_file], shell=True)

                res = requests.get(self.url, allow_redirects=True)
                # Write into a files
                with open(audio_file, "wb+") as f:
                    f.write(res.content)
            else:
                audio_file = self.url
        except:
            return "Audio File Error - Writing"

        # model = whisper.load_model("tiny")
        model = whisper.load_model("small")
        result = model.transcribe(audio_file, fp16=False)
        if os.path.exists(audio_file):
            os.remove(audio_file)

        return result["text"]
