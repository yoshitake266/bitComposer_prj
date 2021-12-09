import glob # 複数のファイルを取り出す
import numpy as np
import os
from music21 import converter, instrument, note, chord
from keras.utils import np_utils
import model_conf
import pickle
from tensorflow.keras.callbacks import ModelCheckpoint

sequence_length = 10

network_input_notes = []
network_output_notes = []

network_input_length = []
network_output_length = []

music_notes = ["rest","A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5"]
music_length = [0.25, 0.5, 1.0, 2.0, 4.0]

string_notes = []
note_length = []
for midi in glob.glob("music/*.mid"):
    music = converter.parse(midi)
    parts = instrument.partitionByInstrument(music)

    if parts:
        note_to_parse = parts.parts[0].recurse()
    else:
        note_to_parse = music.flat.notes

    for element in note_to_parse:
        if isinstance(element, note.Note):
            string_notes.append(str(element.pitch))
            music_notes.append(str(element.pitch))
            note_length.append(element.duration.quarterLength)
            music_length.append(element.duration.quarterLength)            
        elif isinstance(element, chord.Chord):
            string_notes.append('.'.join(str(n.pitch) for n in element.notes))
            music_notes.append('.'.join(str(n.pitch) for n in element.notes))
            note_length.append(element.duration.quarterLength)
            music_length.append(element.duration.quarterLength)
        elif isinstance(element, note.Rest):
            string_notes.append("rest")
            note_length.append(element.duration.quarterLength)
            music_length.append(element.duration.quarterLength)

appeared_notes = sorted(set(music_notes))
n_len = len(appeared_notes) # 正規化用
appeared_note_length = sorted(set(music_length))
duration_len = len(appeared_note_length)

f = open('n_len.txt', 'wb')
pickle.dump(n_len, f)

note_int = dict((note, n) for n, note in enumerate(appeared_notes))
f = open('noteList.txt', 'wb')
pickle.dump(note_int, f)

f = open('duration_len.txt', 'wb')
pickle.dump(duration_len, f)

length_int = dict((length, n) for n, length in enumerate(appeared_note_length))
f = open('lengthList.txt', 'wb')
pickle.dump(length_int, f)

numerical_note = []
for note in string_notes:
    numerical_note.append(note_int[note])

for i in range(len(numerical_note) - sequence_length):
    network_input_notes.append(numerical_note[i:i+sequence_length])
    network_output_notes.append(numerical_note[i + sequence_length])

network_input_notes = np.reshape(network_input_notes, (-1, sequence_length, 1))
network_output_notes = np_utils.to_categorical(network_output_notes)

numerical_length = []
for length in note_length:
    numerical_length.append(length_int[length])

for i in range(len(numerical_length) - sequence_length):
    network_input_length.append(numerical_length[i:i+sequence_length])
    network_output_length.append(numerical_length[i + sequence_length])
network_input_length = np.reshape(network_input_length, (-1, sequence_length, 1))
network_output_length = np_utils.to_categorical(network_output_length)

print(network_input_notes)
print(network_input_notes.shape)
print('--------------')
print(network_output_notes)
print(network_output_notes.shape)
print('--------------')
print(network_input_length)
print(network_input_length.shape)
print('--------------')
print(network_output_length)
print(network_output_length.shape)

#モデル構築のためshapeを保存
input_shape = [network_input_notes.shape[1], network_input_notes.shape[2]]
f = open('input_shape.txt', 'wb')
pickle.dump(input_shape, f)

model1 = model_conf.create_note_model(n_len, input_shape)
model2 = model_conf.create_length_model(duration_len, input_shape)

checkpoint_path = "checkpoint_note/cp.ckpt"
filepath = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path,
                            save_weights_only=True,
                            monitor="loss",
                            mode="min",
                            period=100,
                            verbose=1)
model1.summary()

# model.load_weights(checkpoint_path)

model1.fit(network_input_notes, network_output_notes, epochs=500, batch_size=64,
          callbacks=[cp_callback])

checkpoint_path = "checkpoint_length/cp.ckpt"
filepath = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path,
                            save_weights_only=True,
                            monitor="loss",
                            mode="min",
                            period=100,
                            verbose=1)

model2.fit(network_input_length, network_output_length, epochs=500, batch_size=64,
           callbacks=[cp_callback])