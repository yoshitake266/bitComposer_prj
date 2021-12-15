from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Lambda
from tensorflow.keras.optimizers import Adam

#音程AIモデルの作成
def create_note_model(length, network_shape):
    print(network_shape)
    model = Sequential()
    model.add(Lambda((lambda x: x/length), input_shape=(network_shape[0], network_shape[1])))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(200))
    model.add(Dropout(0.3))
    model.add(Dense(length))
    model.add(Activation('softmax'))

    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.0001))

    model.summary()
    return model

#音価AIモデルの作成
def create_length_model(length, network_shape):
    model = Sequential()
    model.add(Lambda((lambda x: x/length), input_shape=(network_shape[0], network_shape[1])))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(200))
    model.add(Dropout(0.3))
    model.add(Dense(length))
    model.add(Activation('softmax'))

    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.0001))
    
    model.summary()
    return model

#重みを読み込む
def model_load(model, checkpoint_path):

    model.load_weights(checkpoint_path)
    return model