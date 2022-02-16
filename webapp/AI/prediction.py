from music21 import instrument, note, chord, stream,tempo
from tensorflow import keras
import numpy as np
import pickle
import AI.model_conf as model_conf
from fractions import Fraction
from random import randint
import os

def predict(user_inputs_notes, user_inputs_note_length,bpm):
	print(user_inputs_notes)
	print('--------------------')
	print(user_inputs_note_length)
	print('--------------------')
	path = os.path.dirname(__file__) + '/'
	#音と数のリスト、ラベルの数、モデル作成のための行列の形を読み込む
	f = open(path + 'params/noteList.txt', 'rb')
	note_int = pickle.load(f)
	print(note_int)
	print('--------------')
	int2note = dict((val, key) for key,val in note_int.items())
	f = open(path + 'params/n_len.txt', 'rb')
	
	n_len = pickle.load(f)
	print(n_len)
	print('----------------')
	f = open(path + 'params/lengthList.txt', 'rb')
	length_int = pickle.load(f)
	print(length_int)
	print('---------------')
	int2length = dict((val, key) for key,val in length_int.items())
	f = open(path + 'params/duration_len.txt', 'rb')
	
	duration_len = pickle.load(f)
	print(duration_len)
	print('-------------------')
	f = open(path + 'params/input_shape.txt', 'rb')
	shape = pickle.load(f)
	print(shape)
	print('---------------')
	#モデル作成
	model1 = model_conf.create_note_model(n_len, shape)
	model1 = model_conf.model_load(model1, path + "checkpoint_note/cp.ckpt")
	model2 = model_conf.create_length_model(duration_len, shape)
	model2 = model_conf.model_load(model2, path + "checkpoint_length/cp.ckpt")
	
	#ユーザからの入力
	input_notes = [note_int[st] for st in user_inputs_notes]
	#生成した音程のリスト
	numerical_prediction_output = input_notes
	#生成した音の長さのリスト
	numerical_prediction_output_length = [length_int[nl] for nl in user_inputs_note_length]
	input_length = numerical_prediction_output_length

	length_sum = sum(user_inputs_note_length)
	music_length = length_sum + bpm #生成する音の数

	#入力がshape[0]より少ないならshape[0]音分の入力に補填
	if len(input_notes) > shape[0]:
		input_notes = input_notes[-1*(1+shape[0]):-1]
		input_length = input_length[-1*(1+shape[0]):-1]
	elif len(input_notes) < shape[0]:
		for i in range(shape[0] - len(input_notes)):
			r = randint(0, n_len-1)
			input_notes.append(note_int[int2note[r]])
			r = randint(0, duration_len-1)
			input_length.append(length_int[int2length[r]])
	print(input_notes)
	print('-----------')
	print(input_length)

	music_length_now = length_sum

	while music_length_now < music_length:

		prediction_input_note = np.reshape(input_notes, (1, shape[0], 1))
		prediction_input_length = np.reshape(input_length, (1, shape[0], 1))

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

		#1音ずらしてshape[0]音にする
		input_notes = input_notes[1:shape[0]+1]
		#音の長さ
		input_length = np.append(input_length, numerical_length)
		input_length = input_length[1:shape[0]+1]

		music_length_now += int2length[numerical_length]

	string_prediction_output = []
	for i in range(len(numerical_prediction_output)):
		#音程リストと長さのリストを格納
		string_prediction_output.append([int2note[numerical_prediction_output[i]], int2length[numerical_prediction_output_length[i]]])

	offset = 0.0 #音のタイミング
	prediction_output = [] #midi note
	mm = tempo.MetronomeMark(number=bpm)
	prediction_output.append(mm)

	#midi生成
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

	#midiの作成
	midi_stream = stream.Stream(prediction_output)
	midi_stream.write('midi', fp=path + '../static/media/out.mid')