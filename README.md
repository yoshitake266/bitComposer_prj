# bit composer
 自動作曲Webアプリケーション

# アプリの機能・特徴
ユーザが作った短いメロディからゲーム音楽風の曲を作曲してくれる

# 使い方
1. Webページ上に表示されるピアノからメロディを入力していく
2. メロディをサーバに送信してAIが作曲
3. 曲のmp3を再生

# Webシステムについて
サーバプログラムはPythonのライブラリのFlaskを使っています。
 
 ![image](https://user-images.githubusercontent.com/43458963/143021077-12c72daf-c194-4914-8e4b-0b77dd9f3822.png)

# AIについて
自動作曲はRNN(Recurrent Neural Network)を使っています。
![キャプチャ](https://user-images.githubusercontent.com/43458963/143048883-7ccfc8c7-33bf-4be4-9133-b6e54f8e240f.PNG)

# 環境構築 (Ubuntu)

## Pythonのインストール
- Python ver3.9.6

## Pythonライブラリのインストール(pip)
- flask
- music21
- midi2audio
- tensorflow
- pickle

### Windowsの場合はFluidSynthとLilyPondをダウンロードして環境Pathを通す
- [Wiki: Pythonでmp3と楽譜の生成](https://github.com/yoshitake266/bitComposer_prj/wiki/Python%E3%81%A7mp3%E3%81%A8%E6%A5%BD%E8%AD%9C%E3%81%AE%E7%94%9F%E6%88%90)

## ApacheのインストールからFlask実行まで
- [Wiki: Ubuntu環境のApacheサーバでFlaskを実行](https://github.com/yoshitake266/bitComposer_prj/wiki/Ubuntu%E7%92%B0%E5%A2%83%E3%81%AEApache%E3%82%B5%E3%83%BC%E3%83%90%E3%81%A7Flask%E3%82%92%E5%AE%9F%E8%A1%8C)

### 上記の作業が面倒という人はrun.pyをpythonで実行
