import glob # 複数のファイルを取り出す
import numpy as np
import os
from music21 import converter, instrument, note, chord
from keras.utils import np_utils
import model_conf
import pickle
from tensorflow.keras.callbacks import ModelCheckpoint

network_input = []
network_output = []
sequence_length = 1
string_notes = []

for midi in glob.glob("../midis/*.mid"):
    music = converter.parse(midi)
    parts = instrument.partitionByInstrument(music)
    music_notes = []

    if parts:
        note_to_parse = parts.parts[0].recurse()
    else:
        note_to_parse = music.flat.notes

    for element in note_to_parse:
        if isinstance(element, note.Note):
            music_notes.append(f"{str(element.pitch)} {element.duration.quarterLength}")
        elif isinstance(element, chord.Chord):
            music_notes.append(f"{'.'.join(str(n.pitch) for n in element.notes)} {element.duration.quarterLength}")
        elif isinstance(element, note.Rest):
            music_notes.append(f"rest {element.duration.quarterLength}")
    string_notes.append(music_notes)
    
appeared_notes = sorted(set(string_notes[:][:]))
n_len = len(appeared_notes) # 正規化用
f = open('n_len.txt', 'wb')
pickle.dump(n_len, f)

note_int = dict((note, n) for n, note in enumerate(appeared_notes))
f = open('noteList.txt', 'wb')
pickle.dump(note_int, f)

numerical_note = []
for i in range(len(string_notes)):
    note_list = []
    for note in string_notes[i]
        note_list.append(note_int[note])
    numerical_note.append(note_list)

for i in range(len(numerical_note)):
    for j in range(len(numerical_note[i] - sequence_length))
    network_input.append(numerical_note[j:j+sequence_length])
    network_output.append(numerical_note[j + sequence_length])

network_input = np.reshape(network_input, (-1, sequence_length, 1))
network_output = np_utils.to_categorical(network_output)

print(network_input)
print(network_input.shape)
print('--------------')
print(network_output)
print(network_output.shape)

f = open('input_notes.txt', 'wb')
pickle.dump(network_input, f)

model = model_conf.create_model(n_len, network_input)

checkpoint_path = "checkpoint/cp.ckpt"
filepath = os.path.dirname(checkpoint_path)
cp_callback = ModelCheckpoint(checkpoint_path,
                            save_weights_only=True,
                            monitor="loss",
                            mode="min",
                            period=50,
                            verbose=1)

model.summary()

model.load_weights(checkpoint_path)

model.fit(network_input, network_output, epochs=2400, batch_size=64,
          callbacks=[cp_callback])