from logmmse import logmmse_from_file
import io
import os
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types



class Speech2Text():

    inputFilePath = ""
    outputFilePath = ""

    def speech2Text(self,audioFile):
        print("Processing speech to Text, file name is : ",audioFile)
        # Instantiates a client
        client = speech.SpeechClient()
        # The name of the audio file to transcribe
        file_name = os.path.join(
            os.path.dirname(__file__),
            'resources',
            'audio.raw')


        # Loads the audio into memory
        with io.open(audioFile, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)


        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            audio_channel_count=2,
            language_code='yue-Hant-HK')#language_code='yue-Hant-HK'

        # Detects speech in the audio file
        response = client.recognize(config, audio)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))


    def noiseReduce(self):
        fileName = os.path.basename(self.inputFilePath)
        self.outputFilePath = "./" + fileName[:fileName.index(".")] + "_reduceNoise" + fileName[fileName.index("."):]
        if os.path.exists(self.outputFilePath) == False:
            logmmse_from_file(self.inputFilePath,self.outputFilePath)

gaCredentials = r"[GOOGLE_APPLICATION_CREDENTIALS]"  # Please set up  your own GOOGLE_APPLICATION_CREDENTIALS json file here
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= gaCredentials


s2t = Speech2Text()
s2t.inputFilePath = "./wzw.wav"
s2t.speech2Text(s2t.inputFilePath)
s2t.noiseReduce()
s2t.speech2Text(s2t.outputFilePath)
