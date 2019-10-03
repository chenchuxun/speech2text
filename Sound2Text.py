from logmmse import logmmse_from_file
import io
import os
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

"""
This application demonstrates a voice file 
can be transformed to text in a better result after applying a noise reduction. 
example:
 
:param 1. inputFilePath: your own file path
       2. languageCode: refer to https://cloud.google.com/speech-to-text/docs/languages
       
       
# Please set up  your own GOOGLE_APPLICATION_CREDENTIALS json file, example ./my_google_credentials.json
gaCredentials = r"*********.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= gaCredentials
s2t = Speech2Text()
s2t.languageCode='yue-Hant-HK'
s2t.inputFilePath = "your own file path" such as:  "./wzw.wav" (we provide two example files within the same directory)
s2t.speech2Text(s2t.inputFilePath)
s2t.noiseReduce() #the processed file will be saved in the currenty directory
s2t.speech2Text(s2t.outputFilePath)
 
 
 console1:
 
Processing speech to Text, file name is :  wzw.wav
Transcript: 一套成功嘅電影對一個社會嘅經濟同文化推動力係好大㗎所以我哋2003年嘅香港電影全力回歸社會反映社會影響社會大家要警惕禽流感我哋就拍咗金雞我哋拍賣香港係男女平等我嚟拍咗大隻佬唔係淨係女人除衫先有人睇㗎人除衫都好好睇㗎就喺上個禮拜警方喺旺角帶舉掃黃點解呀係邊個通風報信呀我哋部電影豪情
Processing speech to Text, file name is :  ./wzw_reduceNoise.wav
Transcript: 一套成功嘅電影對一個社會嘅經濟同文化推動力係好大㗎所以我哋2003年嘅香港電影全力回歸社會反映社會影響社會立提醒大家要警惕禽流感我哋就拍咗金雞我哋拍賣飛鷹提醒大家香港係男女平等嘅我哋拍咗大隻佬唔係淨係女人除衫先有人睇㗎除衫都好好睇㗎就喺上個禮拜警方喺旺角帶舉掃黃點解呀係邊個通風報信呀我哋部電影豪情

console2:
Processing speech to Text, file name is :  ./zjc.wav
Transcript: 我想知我咁快返嚟咁樣嘅一方吹唔係第一時間返屋企嗰條女囉點會上到樓你喺個門口等緊紅油呀我不及妻兒唔搞啲輕擎嘅開心返嚟囉佢飯都五十幾條啦喺呢度住宿嘅免費一個月就慳返成皮㗎喇有咩頭暈身㷫又唔使急症排隊排到仆街將我成日同人講假期買樓輪公屋冇㗎啦坐監係香港年輕人嘅出路
Processing speech to Text, file name is :  ./zjc_reduceNoise.wav
Transcript: 我想知我咁快返嚟咁樣嘅一方吹我唔係第一時間返屋企嗰條女囉點會上到樓你喺個門口等緊紅油呀我不及妻兒唔搞啲輕擎嘅開心返嚟囉做嚇就好咩條數咁計嘅喺出面做緊劏房租衫差一個月啦你繼水電煤喎所以餐廳腿飯都五十幾條啦喺呢度住宿嘅免費一個月即刻返上嚟㗎啦有咩頭暈身㷫又唔使急症排隊排到仆街我成日同人講假期買樓輪公屋冇㗎啦坐監係香港年輕人嘅出路 
"""


class Speech2Text():

    inputFilePath = ""
    outputFilePath = ""
    languageCode = ""

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
            language_code=self.languageCode) #language_code='yue-Hant-HK'

        # Detects speech in the audio file
        response = client.recognize(config, audio)
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))


    def noiseReduce(self):
        fileName = os.path.basename(self.inputFilePath)
        self.outputFilePath = "./" + fileName[:fileName.index(".")] + "_reduceNoise" + fileName[fileName.index("."):]
        if os.path.exists(self.outputFilePath) == False:
            logmmse_from_file(self.inputFilePath,self.outputFilePath)




