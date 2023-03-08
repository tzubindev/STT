import speech_recognition as sr
import requests

from pydub import AudioSegment
from os import path


class Transcribe:
    def __init__(self, url=None, audiofile=None) -> None:
        self.url = url
        self.audio_file = audiofile

    def getText(self):
        if self.url == None and self.audio_file == None:
            return "Syntax Error"

        req = None
        audio_file = None
        if self.audio_file is None:
            try:
                req = requests.get(self.url, allow_redirects=True)
                audio_file = req.content
            except:
                return "Audio File Error - Writing"
        else:
            audio_file = self.audio_file
        r = sr.Recognizer()
        aud = None
        audio_file = path.join(path.dirname(path.realpath(__file__)), audio_file)
        new_audio_file = "".join(audio_file.split(".")[:-1]) + ".wav"

        # # Write into a files
        # with open(audio_file, "wb+") as f:
        #     f.write(res.content)

        AudioSegment.from_mp3(audio_file).export(new_audio_file, format="wav")
        audio_file = new_audio_file
        try:
            with sr.AudioFile(new_audio_file) as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                aud = r.record(source)
        except:
            return "Audio File Error - Reading"

        response = None

        try:
            response = r.recognize_sphinx(aud)
        except sr.UnknownValueError:
            response = "Audio is not understandable."
            raise
        except sr.RequestError as e:
            response = e
            raise

        return response


print(Transcribe(audiofile="10sec.mp3").getText())
