import glob # 複数のファイルを取り出す
import numpy as np
import os
from music21 import converter, instrument, note, chord
from keras.utils import np_utils
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Lambda
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
import pickle

network_input = []
network_output = []

midi = converter.parse("midis/Jump_Up_Super_Star_-_Super_Mario_Odyssey_-_For_Piano_UPDATED.mid")
parts = instrument.partitionByInstrument(midi)
string_notes = []

sequence_length = 100

if parts:
    note_to_parse = parts.parts[0].recurse()
else:
    note_to_parse = midi.flat.notes

for element in note_to_parse:
    
    if isinstance(element, note.Note):
        string_notes.append(f"{str(element.pitch)} {element.duration.quarterLength}")
    elif isinstance(element, chord.Chord):
        string_notes.append(f"{'.'.join(str(n.pitch) for n in element.notes)} {element.duration.quarterLength}")
    elif isinstance(element, note.Rest):
        string_notes.append(f"rest {element.duration.quarterLength}")

appeared_notes = sorted(set(string_notes))
n_len = len(appeared_notes) # 正規化用
f = open('n_len.txt', 'wb')
pickle.dump(n_len, f)

note_int = dict((note, n) for n, note in enumerate(appeared_notes))
f = open('noteList.txt', 'wb')
pickle.dump(note_int, f)

numerical_note = []
for note in string_notes:
    numerical_note.append(note_int[note])

for i in range(len(numerical_note) - sequence_length):
    network_input.append(numerical_note[i:i+sequence_length])
    network_output.append(numerical_note[i + sequence_length])

network_input = np.reshape(network_input, (-1, sequence_length, 1))
network_output = np_utils.to_categorical(network_output)

print(network_input)
print(network_input.shape)
print('--------------')
print(network_output)
print(network_output.shape)

f = open('input_notes.txt', 'wb')
pickle.dump(network_input, f)
model = Sequential()
model.add(Lambda((lambda x: x/n_len), input_shape=(network_input.shape[1], network_input.shape[2])))
model.add(LSTM(150, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(150, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(150))
model.add(Dropout(0.3))
model.add(Dense(n_len))
model.add(Activation('softmax'))

model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.0001))

model.summary()

checkpoint_path = "checkpoint/cp.ckpt"
filepath = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path,
                              save_weights_only=True,
                              monitor="loss",
                              mode="min",
                              period=50,
                              verbose=1)

model.load_weights(checkpoint_path)

model.save('saved_model/my_model')
# model.fit(network_input, network_output, epochs=500, batch_size=64,
#           callbacks=[cp_callback])