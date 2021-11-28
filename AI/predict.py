from music21 import instrument, note, chord, stream
from tensorflow import keras
import numpy as np
import pickle
from fractions import Fraction

f = open('noteList.txt', "rb")
note_int = pickle.load(f)

f = open('n_len.txt', "rb")
n_len = pickle.load(f)

f = open('input_notes.txt', "rb")
network_input = pickle.load(f)
int2note = dict((val, key) for key,val in note_int.items())

model = keras.models.load_model('saved_model/my_model')

music_length = 300

input_notes = np.array(['A4 1/3'])

numerical_rediction_output = []

print('----------------')
for note_index in range(music_length):
	prediction_input = input_notes.reshape((1, len(input_notes), 1))

	prediction = model.predict(prediction_input, verbose=0)

	numerical_note = np.argmax(prediction)
	numerical_prediction_output.append(numerical_note)

	input_notes.append(numerical_note)
	input_notes = input_notes[1:len(input_notes)]

string_prediction_output = []

for i in range(music_length):
	string_prediction_output.append(int2note[numerical_prediction_output[i]])

print(string_prediction_output)

offset = 0
prediction_output = []

for string_note in string_prediction_output:
	note_info = string_note.split(" ")
	note = note_info[0]

	if '\/' in note_info[1]:
		note_length = duration.Duration(note_info[1]).quarterLengthNoTuplets
	else:
		note_length = note_info[1]

	if ('.' in string_note) or string_note.isdigit():
		notes_in_chord = string_note.split('.')
		notes = []

		for current_note in notes_in_chord:
			new_note = note.Note(int(current_note))
			new_note.storedInstrument = insturment.Piano()
			notes.append(new_note)
		new_chord = chord.Chord(notes)
		new_chord.duration.quarterLength = float(note_length)
		new_chord.offset = offset
		prediction_output.append(new_chord)
		offset += note_length
	elif 'rest' in note:
		new_note = note.Rest()
		new_note.duration.quarterLength = float(note_length)
		new_note.offset = offset
		new_note.storedInstrument = instrument.Piano()
		prediction_output.append(new_chord)
		offset += note_length
	else:
		new_note = note.Note(string_note)
		new_note.duration.quarterLength = float(note_length)
		new_note.offset = offset
		new_note.storedInstrument = instrument.Piano()
		prediction_output.append(new_chord)
		offset += note_length

print(prediction_output)

midi_stream = stream.Stream(prediction_output)
midi_stream.write('midi', fp='./test_output.mid')