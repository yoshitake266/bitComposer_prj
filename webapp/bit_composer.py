from music21 import converter, instrument, note, chord, stream
import glob
import numpy as np
from keras.utils import np_utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Lambda
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam

sequence_length = 100 #    1つの入力の長さ
string_flatten_network_input = []
string_network_output = []

for music in glob.glob("cavestory/*.mid"):
        string_notes = []
        print("parsing " + music)
        midi = converter.parse(music)
        
        note_to_parse = None
        parts = instrument.partitionByInstrument(midi)
        
        if parts:
                note_to_parse = parts.parts[0].recurse()
        else:
                note_to_parse = music.flat.notes
                
        for element in note_to_parse:
                if isinstance(element, note.Note):
                        string_notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                        string_notes.append('.'.join(str(n) for n in element.normalOrder))
                        
        for i in range(0, len(string_notes) - sequence_length, 1):
                for string_note in string_notes[i:i+sequence_length]:
                        string_flatten_network_input.append(string_note)
                        
                string_network_output.append(string_notes[i+sequence_length])

notenames = sorted(set(string_flatten_network_input + string_network_output))
note2int = dict((string_note, number) for number, string_note in enumerate(notenames))

network_input = []
for string_note in string_flatten_network_input:
        network_input.append(note2int[string_note])
        
network_input = np.reshape(network_input, (-1, sequence_length, 1))
#network_input = network_input / float(n_vocab)

network_output = []
for string_note in string_network_output:
        network_output.append(note2int[string_note])

network_output = np_utils.to_categorical(network_output)
n_vocab = len(notenames)


model = Sequential()
model.add(Lambda((lambda x: x/n_vocab), input_shape=(network_input.shape[1], network_input.shape[2])))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dropout(0.3))
model.add(Dense(n_vocab))
model.add(Activation('softmax'))

model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.0001))

dir = "model_checkpoint/"
filepath = "{loss:.4f}-weights-improvement-{epoch:02d}.hdf5"

checkpoint = ModelCheckpoint(
        filepath = dir + filepath, monitor="loss", verbose=0, save_best_only=True, mode='min', period=10
)


callbacks_list = [checkpoint]

model.fit(network_input, network_output, epochs=10, batch_size=64, callbacks=callbacks_list)

music_length = 250

start = np.random.randint(0, len(network_input)-1)
pattern = network_input[start]

int2note = dict((number, string_note) for number, string_note in enumerate(notenames))

numerical_prediction_output = []

for note_index in range(music_length):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))

        prediction = model.predict(prediction_input, verbose=0)
        
        numerical_note = np.argmax(prediction)
        numerical_prediction_output.append(numerical_note)

        #pattern = np.append(pattern, numerical_note/float(n_vocab))
        pattern = np.append(pattern, numerical_note)
        pattern = pattern[1:len(pattern)]

string_prediction_output = []

for i in range(music_length):
        string_prediction_output.append(int2note[numerical_prediction_output[i]])

offset = 0
prediction_output = []

for string_note in string_prediction_output:
    if ('.' in string_note) or string_note.isdigit():
        notes_in_chord = string_note.split('.')
        notes = []
        for current_note in notes_in_chord:
            new_note = note.Note(int(current_note))
            new_note.storedInstrument = instrument.Piano()
            notes.append(new_note)
        new_chord = chord.Chord(notes)
        new_chord.offset = offset
        prediction_output.append(new_chord)
    else:
        new_note = note.Note(string_note)
        new_note.offset = offset
        new_note.storedInstrument = instrument.Piano()
        prediction_output.append(new_note)
        
    offset += 0.5
midi_stream = stream.Stream(prediction_output)
midi_stream.write('midi', fp='test_output.mid')