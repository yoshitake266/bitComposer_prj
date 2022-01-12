from music21 import converter, instrument, note, chord, stream
import re

def abc_to_note(str_note):
    abc_note = str_note.split(" ")
    abc_note.pop(-1)
    
    new_note_length = []
    new_spl_note = []
    for note in abc_note:
        
        newnote = ""
        #休符
        if 'z' in note:
            newnote += "rest"
            #["8","4","2"," ","1/2"]
        else:
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

        #長さを格納
        if re.search('[0-9]', note):

            if note in '8': #全音符
                new_note_length.append(4.0)
            elif note in '4': #2分
                new_note_length.append(2.0)
            elif note in '2': #4分
                new_note_length.append(1.0)
            elif note in '1/2': #16分
                new_note_length.append(0.25)
        else:
            #8分
            new_note_length.append(0.5)

    return new_spl_note, new_note_length
def parse_str_to_mid(str_note):

    new_spl_note = abc_to_note(str_note)
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
