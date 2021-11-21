import glob # 複数のファイルを取り出す
import numpy as np
import pickle
from music21 import converter, instrument, note, chord
network_input = []
network_output = []

midi = converter.parse("midis/Jump_Up_Super_Star_-_Super_Mario_Odyssey_-_For_Piano_UPDATED.mid")
parts = instrument.partitionByInstrument(midi)
string_notes = []

print(parts.parts[0])

if parts:
    note_to_parse = parts.parts[0].recurse()
else:
    note_to_parse = midi.flat.notes

for element in note_to_parse:
    if isinstance(element, note.Note):
        string_notes.append(str(element.pitch))
    elif isinstance(element, chord.Chord):
        string_notes.append('.'.join(str(n.pitch) for n in element.notes))

# for i in range(0, len(string_notes) - )
print(len(string_notes))
# for music in glob.glob("midis/*.mid"):
#     midi = converter.parse(music)

#     parts = instrument.partitionByInstrument(midi)