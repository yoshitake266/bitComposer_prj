import pickle

# f = open('noteList.txt', 'rb')
# print(pickle.load(f))
f = open('n_len.txt', 'rb')
d = pickle.load(f)
print(d)