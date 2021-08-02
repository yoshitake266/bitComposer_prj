from music21 import converter, instrument, note, chord, stream
import glob
import numpy as np
from keras.utils import np_utils
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Lambda
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam

sequence_length = 100
string_flatten_network_input = []
