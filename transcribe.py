import subprocess
import whisper
import requests
import os

from textblob import TextBlob


class Transcribe:
    def __init__(self, url, isAudioFile=False, firstSpeakerIsAgent=True) -> None:
        self.url = url
        self.isAudioFile = isAudioFile
        self.audio_file = None
        self.firstSpeakerIsAgent = firstSpeakerIsAgent

        try:
            if not self.isAudioFile:
                root_file_name = "audio_0"
                while os.path.exists(root_file_name + ".mp3"):
                    names = root_file_name.split("_")
                    names[1] = int(names[1]) + 1
                    root_file_name = "_".join(names)

                self.audio_file = root_file_name + ".mp3"
                # audio_file = "/tmp/" + root_file_name + ".mp3"

                # subprocess.Popen(["./create-file.sh %s" % audio_file], shell=True)

                res = requests.get(self.url, allow_redirects=True)
                # Write into a files
                with open(self.audio_file, "wb+") as f:
                    f.write(res.content)
            else:
                self.audio_file = self.url
        except:
            return "Audio File Error - Writing"

        self.result = []
        self.audios = []
        self.getSegments()

        if os.path.exists(self.audio_file) and not self.isAudioFile:
            os.remove(self.audio_file)

    def getSegments(self):

        # model = whisper.load_model("tiny")
        model = whisper.load_model("small")

        speaker = "Agent" if self.firstSpeakerIsAgent else "Client"
        self.result = model.transcribe(
            self.audio_file,
            fp16=False,
        )

    def speakerDiarization(self):
        import sys
        import os

        sys.path.insert(
            0,
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "./pyAudioAnalysis/pyAudioAnalysis/",
            ),
        )
        import audioSegmentation as aS

        (
            speaker_marking,
            duration_arr,
            purity_cluster_m,
            purity_speaker_m,
        ) = aS.speaker_diarization(self.audio_file, 2)

        list_of_timestamps = []
        curNum = -1
        lastDuration = 0.0

        for i in range(len(speaker_marking)):
            if curNum == -1:
                curNum = speaker_marking[i]

            if curNum != speaker_marking[i] or i == len(speaker_marking) - 1:
                curNum = speaker_marking[i]
                list_of_timestamps.append(round(lastDuration))

            lastDuration = duration_arr[i]
        return list_of_timestamps

    def getResult(self):
        obj = self.result
        r = obj["segments"]

        def getEnd(obj):
            return obj["end"]

        ls = list(map(getEnd, r))
        ts = self.speakerDiarization()
        new_ts = []
        speakers = []
        result = []

        lastNum = 0
        speaker = "agent" if self.firstSpeakerIsAgent else "client"
        for i in ls:
            nw = [t for t in ts if (t <= i and t > lastNum)]
            lastNum = nw[len(nw) - 1]
            new_ts.append(nw)
            speakers.append(speaker)
            if len(nw) % 2 == 1:
                speaker = "agent" if speaker == "client" else "client"

        for i in range(len(r)):
            for s in TextBlob(r[i]["text"]).sentences:
                result.append([speakers[i], str(s)])

        return result
