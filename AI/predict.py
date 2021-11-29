from music21 import instrument, note, chord, stream
from tensorflow import keras
import numpy as np
import pickle
import model_conf

f = open('noteList.txt', 'rb')
note_int = pickle.load(f)

int2note = dict((val, key) for key,val in note_int.items())

model = model_conf.create_model()

model = model_conf.model_load(model)
music_length = 300

str_note_list = ['A3 0.5', 'A3 1.0', 'A3 4/3', 'A3.C#4.A4 0.5','A3.C#4.E4 2.0',
'A3.C4 0.5', 'A3.C4 1.0', 'A3.D4 0.5', 'A4 0.5', 'A4 1.0'] 
input_notes = [note_int[n] for n in str_note_list]
numerical_prediction_output = input_notes

print('----------------')
for note_index in range(music_length):
	prediction_input = np.reshape(input_notes, (1, len(input_notes), 1))

	prediction = model.predict(prediction_input, verbose=0)

	numerical_note = np.argmax(prediction)
	numerical_prediction_output.append(numerical_note)

	input_notes.append(numerical_note)
	input_notes = input_notes[1:len(input_notes)]

string_prediction_output = []

for i in range(music_length):
	string_prediction_output.append(int2note[numerical_prediction_output[i]])

print(string_prediction_output)

offset = 0.0
prediction_output = []

for string_note in string_prediction_output:
	note_info = string_note.split(" ")
	note_interval = note_info[0]

	if '/' in note_info[1]:
		floats = [float(fl) for fl in note_info[1].split('/')]
		note_length = floats[0] / floats[1]
	else:
		note_length = float(note_info[1])

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
		# elif 'rest' in note_interval:
		# 	new_note = note.Rest()
		# 	new_note.duration.quarterLength = note_length
		# 	new_note.offset = offset
		# 	new_note.storedInstrument = instrument.Piano()
		# 	prediction_output.append(new_chord)
		# 	offset += note_length
		#メロディ
	else:
		new_note = note.Note(note_interval)
		new_note.duration.quarterLength = note_length
		new_note.offset = offset
		new_note.storedInstrument = instrument.Piano()
		prediction_output.append(new_chord)
		offset += note_length

print(prediction_output)

midi_stream = stream.Stream(prediction_output)
midi_stream.write('midi', fp='./test_output.mid')