from music21 import converter, instrument, note, chord, stream
import re

def str_to_Note(str_note):
    abc_note = str_note.split(" ")
    abc_note.pop(-1)
    
    new_spl_note = []
    for note in abc_note:
        
        newnote = ""
        
        if '^' in note:
            newnote += note[1] + '#'
        else:
            newnote += note[0]

        if ',,' in note:
            newnote += '2'
        elif ',' in note:
            newnote += '3'
        else:
            newnote += '4'
        
        new_spl_note.append(newnote)
    return new_spl_note
            
            
        
    
def parse_str_to_mid(str_note):

    new_spl_note = str_to_Note(str_note)
    NoteList = []
    offset = 0.5
    for i in new_spl_note:
        mid_note = note.Note(i,quarterLength = 1)
        mid_note.offset = offset
        mid_note.storedInstrument = instrument.Piano()
        NoteList.append(mid_note)
        offset += 0.5
    Strmidi = stream.Stream(NoteList)
    Strmidi.write('midi', fp=r'static\media\out.mid')
