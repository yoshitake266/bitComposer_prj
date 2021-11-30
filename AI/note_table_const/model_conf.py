from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Lambda
from tensorflow.keras.optimizers import Adam
import pickle
import os

#モデルの作成
def create_model(n_len, network_input):
    model = Sequential()
    model.add(Lambda((lambda x: x/n_len), input_shape=(network_input.shape[1], network_input.shape[2])))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(200))
    model.add(Dropout(0.3))
    model.add(Dense(n_len))
    model.add(Activation('softmax'))

    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.0001))

    return model
#重みを読み込む
def model_load(model):
    checkpoint_path = "checkpoint/cp.ckpt"

    model.load_weights(checkpoint_path)
    return model