from music21 import converter, instrument, note, chord, stream

def parse_str_to_mid(str_note):
    NoteList = []
    offset = 0.5
    for i in str_note:
        mid_note = note.Note(i,quarterLength = 1)
        mid_note.offset = offset
        mid_note.storedInstrument = instrument.Piano()
        NoteList.append(mid_note)
        offset += 0.5
    return NoteList
