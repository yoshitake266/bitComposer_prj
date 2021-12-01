import pickle

f = open('noteList.txt', 'rb')
noteList = pickle.load(f)
print(len(noteList))

for note in noteList.keys():
	print(note)