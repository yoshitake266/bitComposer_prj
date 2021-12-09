from music21 import instrument, note, chord, stream
from tensorflow import keras
import numpy as np
import pickle
import AI.model_conf as model_conf
from fractions import Fraction
from random import randint
import os

def predict(user_inputs_notes):
																																																																f = open('AI/params/noteList.txt', 'rb')
																																																																note_int = pickle.load(f)

																																																																int2note = dict((val, key) for key,val in note_int.items())

																																																																f = open('AI/params/n_len.txt', 'rb')
																																																																n_len = pickle.load(f)

																																																																f = open('AI/params/lengthList.txt', 'rb')
																																																																length_int = pickle.load(f)
																																																																int2length = dict((val, key) for key,val in length_int.items())

																																																																f = open('AI/params/duration_len.txt', 'rb')
																																																																duration_len = pickle.load(f)

																																																																f = open('AI/params/input_shape.txt', 'rb')
																																																																shape = pickle.load(f)

																																																																model1 = model_conf.create_note_model(n_len, shape)

																																																																model1 = model_conf.model_load(model1, "AI/checkpoint_note/cp.ckpt")

																																																																model2 = model_conf.create_length_model(duration_len, shape)
																																																																model2 = model_conf.model_load(model2, "AI/checkpoint_length/cp.ckpt")

																																																																music_length = 240

																																																																#ユーザからの入力
																																																																input_notes = [note_int[st] for st in user_inputs_notes]
																																																																#生成した音程のリスト
																																																																numerical_prediction_output = input_notes
																																																																#生成した音の長さのリスト
																																																																numerical_prediction_output_length = [length_int[0.5] for i in input_notes ]
																																																																input_length = numerical_prediction_output_length

																																																																if len(input_notes) > 10:
																																																																																																																																input_notes = input_notes[-11:-1]
																																																																																																																																input_length = input_length[-11:-1]
																																																																elif len(input_notes) < 10:
																																																																																																																																for i in range(10 - len(input_notes)):
																																																																																																																																																																																																print(i)
																																																																																																																																																																																																r = randint(0, n_len)
																																																																																																																																																																																																input_notes.append(r)
																																																																																																																																																																																																#8分音符の長さ (今のところabc.jsで8分音符しか入力できない)
																																																																																																																																																																																																input_length.append(length_int[0.5])
																																																																

																																																																print(np.reshape(input_notes, (1, len(input_notes), 1)))
																																																																print(numerical_prediction_output)
																																																																print('----------------')
																																																																for note_index in range(music_length):

																																																																																																																																prediction_input_note = np.reshape(input_notes, (1, 10, 1))

																																																																																																																																prediction_input_length = np.reshape(input_length, (1, 10, 1))
																																																																																																																																print(prediction_input_note)
																																																																																																																																#予測
																																																																																																																																prediction1 = model1.predict(prediction_input_note, verbose=0)
																																																																																																																																prediction2 = model2.predict(prediction_input_length, verbose=0)
																																																																																																																																#softmaxの出力から確立が最大の音を生成
																																																																																																																																numerical_note = np.argmax(prediction1)
																																																																																																																																numerical_prediction_output.append(numerical_note)

																																																																																																																																numerical_length = np.argmax(prediction2)
																																																																																																																																numerical_prediction_output_length.append(numerical_length)

																																																																																																																																#次に入力する音
																																																																																																																																input_notes = np.append(input_notes, numerical_note)
																																																																																																																																#1音ずらして音の入力にする
																																																																																																																																input_notes = input_notes[1:11]

																																																																																																																																#音の長さ
																																																																																																																																input_length = np.append(input_length, numerical_length)
																																																																																																																																input_length = input_length[1:11]

																																																																string_prediction_output = []

																																																																for i in range(music_length):
																																																																																																																																#音程リストと長さのリストを格納
																																																																																																																																string_prediction_output.append([int2note[numerical_prediction_output[i]], int2length[numerical_prediction_output_length[i]]])

																																																																offset = 0.0 #音のタイミング
																																																																prediction_output = [] 

																																																																for string_note in string_prediction_output:
																																																																																																																																note_info = [d for d in string_note]
																																																																																																																																note_interval = note_info[0]

																																																																																																																																#音の長さが分数の場合
																																																																																																																																if isinstance(note_info[1], Fraction):
																																																																																																																																																																																																note_length = float(note_info[1])
																																																																																																																																else:
																																																																																																																																																																																																note_length = note_info[1]
																																																																																																																																#和音
																																																																																																																																if ('.' in note_interval):
																																																																																																																																																																																																notes_in_chord = note_interval.split('.')
																																																																																																																																																																																																notes = []

																																																																																																																																																																																																for current_note in notes_in_chord:
																																																																																																																																																																																																																																																																new_note = note.Note(current_note)
																																																																																																																																																																																																																																																																new_note.storedInstrument = instrument.Piano()
																																																																																																																																																																																																																																																																notes.append(new_note)
																																																																																																																																																																																																new_chord = chord.Chord(notes)
																																																																																																																																																																																																new_chord.duration.quarterLength = note_length
																																																																																																																																																																																																new_chord.offset = offset
																																																																																																																																																																																																prediction_output.append(new_chord)
																																																																																																																																																																																																offset += note_length
																																																																																																																																#休符
																																																																																																																																elif 'rest' in note_interval:
																																																																																																																																																																																																new_note = note.Rest()
																																																																																																																																																																																																new_note.duration.quarterLength = note_length
																																																																																																																																																																																																new_note.offset = offset
																																																																																																																																																																																																new_note.storedInstrument = instrument.Piano()
																																																																																																																																																																																																prediction_output.append(new_note)
																																																																																																																																																																																																offset += note_length
																																																																																																																																#メロディ
																																																																																																																																else:
																																																																																																																																																																																																new_note = note.Note(note_interval)
																																																																																																																																																																																																new_note.duration.quarterLength = note_length
																																																																																																																																																																																																new_note.offset = offset
																																																																																																																																																																																																new_note.storedInstrument = instrument.Piano()
																																																																																																																																																																																																prediction_output.append(new_note)
																																																																																																																																																																																																offset += note_length

																																																												
																																																																midi_stream = stream.Stream(prediction_output)
																																																																midi_stream.write('midi', fp='./static/media/out.mid')
