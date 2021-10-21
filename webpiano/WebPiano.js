// 変数宣言
const path = "audio/"             // オーディオファイルのパス
const keyMap = [
    { pcKey: "a", pianoKey: 0 },
    { pcKey: "q", pianoKey: 1 },
    { pcKey: "s", pianoKey: 2 },
    { pcKey: "d", pianoKey: 3 },
    { pcKey: "w", pianoKey: 4 },
    { pcKey: "f", pianoKey: 5 },
    { pcKey: "e", pianoKey: 6 },
    { pcKey: "g", pianoKey: 7 },
    { pcKey: "h", pianoKey: 8 },
    { pcKey: "r", pianoKey: 9 },
    { pcKey: "j", pianoKey: 10 },
    { pcKey: "t", pianoKey: 11 },
    { pcKey: "k", pianoKey: 12 },
    { pcKey: "y", pianoKey: 13 },
    { pcKey: "l", pianoKey: 14 },
    { pcKey: ";", pianoKey: 15 },
    { pcKey: "u", pianoKey: 16 },
    { pcKey: "z", pianoKey: 17 },
    { pcKey: "i", pianoKey: 18 },
    { pcKey: "x", pianoKey: 19 },
    { pcKey: "c", pianoKey: 20 },
    { pcKey: "o", pianoKey: 21 },
    { pcKey: "b", pianoKey: 22 },
    { pcKey: "p", pianoKey: 23 },
    { pcKey: "b", pianoKey: 24 },
    { pcKey: "@", pianoKey: 25 },
    { pcKey: "n", pianoKey: 26 },
    { pcKey: "m", pianoKey: 27 },
    { pcKey: "[", pianoKey: 28 },
    { pcKey: "/", pianoKey: 29 },
]                                   // PCキーとピアノ鍵盤番号の紐づけ
const pianoSounds = []              // Audioオブジェクト        
const touchkeyNumlish = []          // タッチ中の鍵盤番号リスト
let clickedKeyNum = null            // クリック中の鍵盤番号リスト
const isKeyPressing = new Array(30) // ピアノ鍵盤ごとの押下状態
isKeyPressing.fill(false)           // 初期値 = false            
const intervalIds = new Array(30)   // 各オーディオフェードアウトのインターバルID
intervalIds.fill(null)              // 初期値 = null           
const pianoWrap = document.getElementById("piano-wrap")     // 鍵盤全体
const whiteKeys = document.querySelectorAll(".white-key")   // 白鍵
const blackKeys = document.querySelectorAll(".black-key")   // 黒鍵

const note = [,,]
// 初期処理
// Audioオブジェクトを作成セット

for (var no of note){

}
for ( i = 0; i <= 29; i++ ){
    let sound = new Audio( path + i + ".wav" )

// const note = ["A2","A#2","B2","C3","C#3","D3","D#3","E3","F3","F#3","G3","G#3","A3","A#3","B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5"]

// // 初期処理
// // Audioオブジェクトを作成セット
// for ( var no of note ){
//     let sound = new Audio( path + no + ".wav" )

    sound.volume = 0
    pianoSounds.push(sound)
}
// タッチ対応判定
if (window.ontouchstart === null) {
    // タッチ対応：タッチイベントのリスナーをセット
    pianoWrap.addEventListener("touchstart", function(){ handleTouchEvents() })
    pianoWrap.addEventListener("touchmove", function(){ handleTouchEvents() })
    pianoWrap.addEventListener("touchend", function(){ handleTouchEvents() })
    pianoWrap.addEventListener("touchcancel", function(){ handleTouchEvents() }) 
} else {
    // タッチ非対応：マウスイベントのリスナーをセット
    pianoWrap.addEventListener("mousedown", function(){ handleMouseEvents() })
    pianoWrap.addEventListener("mouseup", function(){ handleMouseEvents() })
    window.addEventListener("mousemove", function(){ handleMouseEvents() })
} 

// 座標(x,y)に応じた鍵盤番号を取得
function getKeyNum(x, y){
    // 黒鍵とタッチ箇所が重なるかチェック
    for ( let j = 0; j < blackKeys.length; j++ ){
        const KeyRect = blackKeys[j].getBoundingClientRect()
        if ( x >= window.pageXOffset + KeyRect.left  &&
             x <= window.pageXOffset + KeyRect.right &&
             y >= window.pageYOffset + KeyRect.top   &&
             y <= window.pageYOffset + KeyRect.bottom ){
            // タッチした鍵盤番号をセット
            return Number( blackKeys[j].dataset.keyNum )
        }
    } 
    // 白鍵とタッチ箇所が重なるかチェック
    for ( let j = 0; j < whiteKeys.length; j++ ){
        const KeyRect = whiteKeys[j].getBoundingClientRect()
        if ( x >= window.pageXOffset + KeyRect.left  &&
             x <= window.pageXOffset + KeyRect.right &&
             y >= window.pageYOffset + KeyRect.top   &&
             y <= window.pageYOffset + KeyRect.bottom ){
            // タッチした鍵盤番号をセット
            return Number( whiteKeys[j].dataset.keyNum )
        }
    }
    // ピアノ外のタッチの場合
    return null
}

// タッチイベント発生時の処理
function handleTouchEvents(event){
    if (typeof event.cancelable !== 'boolean' || event.cancelable) {
        event.preventDefault();
    }
    const BeforeKeyNumllish = JSON.parse(JSON.stringify(touchkeyNumlish)) 
    console.log(BeforeKeyNumllish)
    touchKeyNullish.length = 0

    // 各接触ポイントから押下中の鍵盤番号リストを作成
    for ( let i = 0; i < event.touches.length; i++ ){
        const x = event.touches[i].pageX 
        const y = event.touches[i].pageY 
        let keyNum = getKeyNum(x, y)
        if ( keyNum !== null ){
            if ( !touchKeyNullish.includes(keyNum) ){
                // リストに存在しなければ鍵盤番号をセット
                touchkeyNumlish.push(keyNum)
            }
        }
    } 
    // 新リストのみに存在 => 鍵盤を押下した処理
    for ( let i = 0; i < touchKeyNullish.length; i++ ){
        if ( !BeforeKeyNumllish.includes(touchKeyNullish[i]) ){ 
            pressPianoKey(touchKeyNullish[i]) 
        }
    }
    // 旧リストのみに存在 => 鍵盤をはなした処理
    for ( let i = 0; i < BeforeKeyNullish.length; i++ ){
        if ( !touchKeyNumlish.includes(BeforeKeyNullish[i]) ){
            releasePianoKey(BeforeKeyNullish[i]) 
        }
    }
}

// マウスイベント発生時の処理
function handleMouseEvents(event){
    // 左クリック以外は対象外
    if ( event.which !== 1 ){ return }
    const x = event.pageX 
    const y = event.pageY 
    let keyNum
    switch ( event.type ){
        case "mousedown":
            keyNum = getKeyNum(x, y)
            if ( keyNum !== null ){ pressPianoKey(keyNum) }
            clickedKeyNum = keyNum
            break
        case "mouseup":
            if ( clickedKeyNum !== null ){
                keyNum = getKeyNum(x, y)
                if ( keyNum !== null ){ releasePianoKey(keyNum) }
                clickedKeyNum = null
            }
            break
        case "mousemove":
            keyNum = getKeyNum(x, y)
            if ( keyNum !== null ){
                // マウスポインタ位置が直前の鍵盤以外の鍵盤上の場合
                if ( keyNum !== clickedKeyNum ){ 
                    releasePianoKey(clickedKeyNum)
                    pressPianoKey(keyNum) 
                    clickedKeyNum = keyNum
                }
            } else {
                // マウスポインタ位置が鍵盤外の場合
                releasePianoKey(clickedKeyNum)
                clickedKeyNum = null
            }
            break
    }
}

// 時の処理
document.onkeydown = function(event) {
    // 鍵盤番号を取得
    const obj = keyMap.find( (item) => item.pcKey === event.key )
    if ( typeof obj !== "undefined" ){
        // keyMapに含まれるキーの場合は後続処理実行
        pressPianoKey(obj.pianoKey)
    } 
}

// PCke時の処理
document.onkeyup = function(event) {
    // 鍵盤番号を取得
    const obj = keyMap.find( (item) => item.pcKey === event.key )
    if ( typeof obj !== "undefined" ){
        // keyMapに含まれるキーの場合は後続処理実行
        releasePianoKey(obj.pianoKey)
    } 
}

// ピアノ鍵盤を押下した時の処理
function pressPianoKey(keyNum){
    if ( !isKeyPressing[keyNum] ){
        // 鍵盤を離している場合のみ続行(長押しによる連打防止)
        isKeyPressing[keyNum] = true
        document.querySelector(`[data-key-num="${keyNum}"]`).classList.add("pressing")
        soundPlay(keyNum)
    }
}

// ピアノ鍵盤をはなした時の処理
function releasePianoKey(keyNum){
    if ( isKeyPressing[keyNum] ){
        // 鍵盤を押している場合のみ続行
        isKeyPressing[keyNum] = false
        document.querySelector(`[data-key-num="${keyNum}"]`).classList.remove("pressing")
        soundStop(keyNum)
    }
}

// オーディオ再生
function soundPlay(soundNum){
    clearInterval( intervalIds[soundNum] )
    intervalIds[soundNum] = null
    pianoSounds[soundNum].volume = 1
    pianoSounds[soundNum].currentTime = 0
    pianoSounds[soundNum].play()
}

// オーディオ停止(フェードアウト)
function soundStop(soundNum){       
    // 20msごとに音量を下げる
    intervalIds[soundNum] = setInterval( function(){
        if ( pianoSounds[soundNum].volume <= 0.05 ){
            // 音量が0.05以下の場合、Interval停止・オーディオ停止
            clearInterval( intervalIds[soundNum] )
            intervalIds[soundNum] = null
            pianoSounds[soundNum].volume = 0
            pianoSounds[soundNum].pause()
            pianoSounds[soundNum].currentTime = 0
        } else {
            // 音量が0.05より大きい場合、音量を0.05下げる
            pianoSounds[soundNum].volume -= 0.05
        }
    }, 20 )
}