import pickle

f = open('noteList.txt', 'rb')
print(pickle.load(f))