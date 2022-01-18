from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Activation, Lambda
from tensorflow.keras.optimizers import Adam

#音程AIモデルの作成
def create_note_model(length, network_shape):
    print(network_shape)
    model = Sequential()
    #入力データの正規化 データを音の種類の大きさで割る
    model.add(Lambda((lambda x: x/length), input_shape=(network_shape[0], network_shape[1])))
    #時系列ごとのデータを学習に含める
    model.add(LSTM(200, return_sequences=True))
    #ノードを減らす
    model.add(Dropout(0.3))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(0.3))
    #最後の時系列データを出力
    model.add(LSTM(200))
    model.add(Dropout(0.3))
    #全結合層
    model.add(Dense(length))
    #softmaxで確率を出力
    model.add(Activation('softmax'))

    #損失関数と最適化関数の設定
    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.0001))

    #作ったモデルをprint出力
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