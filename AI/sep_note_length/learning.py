import glob #複数のファイルを取り出す
import numpy as np
import os
from music21 import converter, instrument, note, chord
from keras.utils import np_utils
import model_conf
import pickle #パラメータをファイル保存
from tensorflow.keras.callbacks import ModelCheckpoint

sequence_length = 10 #一度に入力する長さ

network_input_notes = [] #学習データ
network_output_notes = [] #正解データ

#音価
network_input_length = []
network_output_length = []

#ピアノの音程
music_notes = ["rest","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5"]
#音の長さ 16分 8分 4分 2分 全音符
music_length = [0.25, 0.5, 1.0, 2.0, 4.0]

string_notes = [] #midiファイルの中で出現した音
note_length = [] #出現した音の長さ

#フォルダ内のすべてのmidiを使う
for midi in glob.glob("../midis/*.mid"):
    music = converter.parse(midi) #midiデータ
    parts = instrument.partitionByInstrument(music) #パート

    if parts:
        #ピアノパートを取り出す
        note_to_parse = parts.parts[0].recurse()
    else:
        #noteなし
        note_to_parse = music.flat.notes

    #音程を取り出す
    for element in note_to_parse:
        #単音
        if isinstance(element, note.Note):
            string_notes.append(str(element.pitch))
            music_notes.append(str(element.pitch))
            note_length.append(element.duration.quarterLength)
            music_length.append(element.duration.quarterLength)
        #和音            
        elif isinstance(element, chord.Chord):
            string_notes.append('.'.join(str(n.pitch) for n in element.notes))
            music_notes.append('.'.join(str(n.pitch) for n in element.notes))
            note_length.append(element.duration.quarterLength)
            music_length.append(element.duration.quarterLength)
        #休符
        elif isinstance(element, note.Rest):
            string_notes.append("rest")
            note_length.append(element.duration.quarterLength)
            music_length.append(element.duration.quarterLength)

#出てきた音程の種類
appeared_notes = sorted(set(music_notes))
n_len = len(appeared_notes) # 正規化用
#音価も同様
appeared_note_length = sorted(set(music_length))
duration_len = len(appeared_note_length)

#パラメータをファイル保存 (predition.pyで使う)
f = open('params/n_len.txt', 'wb')
pickle.dump(n_len, f)

#音程と数値の辞書型
note_int = dict((note, n) for n, note in enumerate(appeared_notes))
f = open('params/noteList.txt', 'wb')
pickle.dump(note_int, f)

f = open('params/duration_len.txt', 'wb')
pickle.dump(duration_len, f)

#音価
length_int = dict((length, n) for n, length in enumerate(appeared_note_length))
f = open('parmas/lengthList.txt', 'wb')
pickle.dump(length_int, f)

#数値のみのリスト
numerical_note = []
for note in string_notes:
    numerical_note.append(note_int[note])

#学習データの作成
for i in range(len(numerical_note) - sequence_length):
    network_input_notes.append(numerical_note[i:i+sequence_length])
    network_output_notes.append(numerical_note[i + sequence_length])

#10行1列にする
network_input_notes = np.reshape(network_input_notes, (-1, sequence_length, 1))
#正解データをone-hotエンコーディング
network_output_notes = np_utils.to_categorical(network_output_notes)

#音価
numerical_length = []
for length in note_length:
    numerical_length.append(length_int[length])

for i in range(len(numerical_length) - sequence_length):
    network_input_length.append(numerical_length[i:i+sequence_length])
    network_output_length.append(numerical_length[i + sequence_length])
network_input_length = np.reshape(network_input_length, (-1, sequence_length, 1))
network_output_length = np_utils.to_categorical(network_output_length)

#NNモデル構築のためshapeを保存
input_shape = [network_input_notes.shape[1], network_input_notes.shape[2]]
f = open('params/input_shape.txt', 'wb')
pickle.dump(input_shape, f)

#NNモデルの構築
model1 = model_conf.create_note_model(n_len, input_shape)
model2 = model_conf.create_length_model(duration_len, input_shape)

#重み保存
checkpoint_path = "checkpoint_note/cp.ckpt"
filepath = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path,
                            save_weights_only=True,
                            monitor="loss",
                            mode="min",
                            period=100,
                            verbose=1)
model1.summary()

# 重み読み込み
# model.load_weights(checkpoint_path)

#学習
model1.fit(network_input_notes, network_output_notes, epochs=1000, batch_size=64,
          callbacks=[cp_callback])

#音価
checkpoint_path = "checkpoint_length/cp.ckpt"
filepath = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path,
                            save_weights_only=True,
                            monitor="loss",
                            mode="min",
                            period=100,
                            verbose=1)

model2.fit(network_input_length, network_output_length, epochs=1000, batch_size=64,
           callbacks=[cp_callback])