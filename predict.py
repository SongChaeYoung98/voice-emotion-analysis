# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 10:46
# @Author  : MengnanChen
# @FileName: predict.py
# @Software: PyCharm Community Edition
# 원본 : https://github.com/cnlinxi/speech_emotion/blob/master/predict.py

#도움 될만한 거, 개발 과정
# https://stackoverrun.com/ko/q/4141310
# https://www.python2.net/questions-175104.htm
# https://stackoverflow.com/questions/60350519/how-to-accept-filename-from-user-and-save-the-sound-file-in-python
# https://kongnamool.tistory.com/25 pyaudio 라이브러리 설치 오류
# port audio error : https://stackoverflow.com/questions/50243645/i-cant-import-pyaudio
# https://stackoverflow.com/questions/36681836/pyaudio-could-not-import-portaudio <-conda install -c anaconda portaudio 덕분에 성공
# 파이썬 백분율 표기 : https://codetorial.net/python/string_format.html
# https://banana-media-lab.tistory.com/entry/Librosa-python-library로-음성파일-분석하기
# 마이크 장치에 따라 pyaudio에서 인식이 될 때도 있고 안 될 때도 있다.
# 제조사에서 제공하는 usb 마이크 전용 드라이버가 없으면 realtek audio에서 인식이 안 되는 거 그대로 python에 적용되는 모양
# 아날로그 음성 입력을 통해 마이크 작동 가능 또는 장치 드라이버가 제공되는 usb 마이크 사용 시 정상 작동 가능


import sys
import os
sys.path.append(os.path.join(os.getcwd(),'utility'))

from tkinter import *
from keras.models import load_model
from utility import functions, globalvars
import librosa
import numpy as np
import threading

#추가
import tkinter as tk
import threading
import pyaudio
import wave
from tkinter import *
import tkinter.font as font
from tkinter.filedialog import asksaveasfilename
#추가완료

#plot
import librosa
import librosa.display
import IPython.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
#




# 분류할 일곱가지 감정 정의
emotion_classes=['anger','boredom','disgust','anxiety/fear','happiness','sadness','neutral'] 


# 음성 분석을 위한 wav 파일 불러오는 데 사용되는 path와 모양, 기본 파일 지정 코드
def predict(data_path:str,model_path:str):
    y,sr=librosa.load(data_path,sr=16000) # librosa:load wav
    f=functions.feature_extract_test(data=(y,sr)) # feature extraction
    u=np.full((f.shape[0],globalvars.nb_attention_param),globalvars.attention_init_value,dtype=np.float64)
    model=load_model(model_path)

    result=model.predict([u,f])
    return result[0]


# 오디오 녹음 버튼 이벤트 / Record & Stop
class App():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100

    frames = []

    # 버튼색상, 텍스트 구성, 크기 지정
    def __init__(self, master):
        self.isrecording = False
        myFont = font.Font(weight="bold")
        self.button1 = tk.Button(main, text='Record', command=self.startrecording,
                                 height=2, width=20, bg='#0052cc', fg='#ffffff')
        self.button2 = tk.Button(main, text='stop', command=self.stoprecording,
                                 height=2, width=20, bg='#0052cc', fg='#ffffff')
        self.button1['font'] = myFont
        self.button2['font'] = myFont
        self.button1.place(x=30, y=30)
        self.button2.place(x=280, y=30)

    def startrecording(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format, channels=self.channels,
            rate=self.fs, frames_per_buffer=self.chunk, input=True)
        self.isrecording = True

        print('Recording')
        t = threading.Thread(target=self.record)
        t.start()

    def stoprecording(self):
        self.isrecording = False
        print('recording complete')

        self.filename = ('./data/test/record.wav') #파일은 프로젝트 파일 내 data\test\record.wav로 저장


        # 'wb'= wave파일쓰기 전용모드로 반환, 녹음 후 파일 형태와 샘플링 지정
        # 녹음을 마치면 버튼 이벤트 창 종료
        wf = wave.open(self.filename, 'wb') 
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        main.destroy()

    # 녹음 중이면 콘솔 창에 Recording 을 주기적으로 출력
    def record(self):
        while self.isrecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            print("Recording")

# 버튼 이벤트 윈도우 창의 제목은 recorder로 하고 크기는 520*120 으로 한다.
main = tk.Tk()
main.title('recorder')
main.geometry('520x120')
app = App(main)
main.mainloop()

# 오디오 녹음 버튼 이벤트 / Record & Stop 완료



# 감정 분석 코드 오픈
if __name__ == '__main__':
    model_path='weights_blstm_hyperas_1.h5' # 녹음된 파일 불러오기
    data_path='data/test/record.wav' # 녹음된 파일을 불러오는 경로
    result=predict(data_path,model_path)
    assert len(result)==globalvars.nb_classes
    index_top_n=np.argsort(result)[-globalvars.top_n:]
    human_result=[emotion_classes[i] for i in index_top_n] #가장 높은 값 첫 번째
    probability_result=[result[i] for i in index_top_n] #가장 높은 값 두 번째

    #음성 파일 load, plot
    #x 축은 시간(ms)이고, y축은 db 단위 이다.
    #db는 max 값을 기준으로 상대적인 값의 변화로 표현된다.
    audio_path='data/test/record.wav'
    y, sr = librosa.load(audio_path)
    D = librosa.amplitude_to_db(librosa.stft(y[:1024]), ref=np.max)
    plt.plot(D.flatten())
    plt.show()


    # 음성 데이터를 더 잘 분석하기 위해, MFCC를 수행한 후, amplitude를 log scale로 변환하도록 함

    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)

    log_S = librosa.power_to_db(S, ref=np.max)
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
    plt.title('mel power spectrogram')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    plt.show()

    # Normalization 시켜 그래프의 중앙에 정렬되어 보기 좋게 만듦
    min_level_db = -100


    def _normalize(S):
        return np.clip((S - min_level_db) / -min_level_db, 0, 1)


    norm_S = _normalize(log_S)

    plt.figure(figsize=(12, 4))
    librosa.display.specshow(norm_S, sr=sr, x_axis='time', y_axis='mel')
    plt.title('norm mel power spectrogram')
    plt.colorbar(format='%+0.1f dB')
    plt.tight_layout()
    plt.show()





# 최종 분석 결과 윈도우 창
    
    window2 = Tk()  # 윈도우 생성

    # 제목
    re1 = Label(window2, text='\n\n[음성을 통한 {}개의 감정 분석 결과]\n '.format(globalvars.top_n), font='bold')

    # 제일 높은 수치를 가진 감정을 적색
    re2 = Label(window2, text='{} : {:.3%} '.format(human_result[6], probability_result[6]), fg="red")

    # 두 번째로 높은 수치를 가진 감정은 청색으로 출력
    re3 = Label(window2, text='{} : {:.3%} '.format(human_result[5], probability_result[5]), fg="blue")

    re4 = Label(window2, text='{} : {:.3%} '.format(human_result[4], probability_result[4]))
    re5 = Label(window2, text='{} : {:.3%} '.format(human_result[3], probability_result[3]))
    re6 = Label(window2, text='{} : {:.3%} '.format(human_result[2], probability_result[2]))
    re7 = Label(window2, text='{} : {:.3%} '.format(human_result[1], probability_result[1]))
    re8 = Label(window2, text='{} : {:.3%} '.format(human_result[0], probability_result[0]))



# 각 감정 텍스트를 윈도우 창에 배치
    re1.pack()
    re2.pack()
    re3.pack()
    re4.pack()
    re5.pack()
    re6.pack()
    re7.pack()
    re8.pack()



    # 최종 분석 결과의 새 창 이름은 '음성 분석 결과'라 한다.
    #크기는 320*280으로 한다.
    window2.title('음성 분석 결과')
    window2.geometry('320x280')

    print('emotion is:  {} = {}'.format(human_result[6],probability_result[6]))
    print('emotion is:  {} = {}'.format(human_result[5],probability_result[5]))
    print('emotion is:  {} = {}'.format(human_result[4],probability_result[4]))
    print('emotion is:  {} = {}'.format(human_result[3],probability_result[3]))
    print('emotion is:  {} = {}'.format(human_result[2],probability_result[2]))
    print('emotion is:  {} = {}'.format(human_result[1],probability_result[1]))
    print('emotion is:  {} = {}'.format(human_result[0],probability_result[0]))






    window2.mainloop()

    #분석이 최종적으로 완료되면 해당 폴더 내에 녹음했던 파일을 지워, 다음 다음에 대비한다.
    os.remove('./data/test/record.wav')