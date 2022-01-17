// 変数宣言
const path = "static/audio/"             // オーディオファイルのパス
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
    { pcKey: "v", pianoKey: 22 },
    { pcKey: "p", pianoKey: 23 },
    { pcKey: "b", pianoKey: 24 },
    { pcKey: "@", pianoKey: 25 },
    { pcKey: "n", pianoKey: 26 },
    { pcKey: "m", pianoKey: 27 },
    { pcKey: "[", pianoKey: 28 },
    { pcKey: ",", pianoKey: 29 },
]
//abc記法の配列
const abc_param = ["A,,", "^A,,", "B,,", "C,", "^C,", "D,", "^D,", "E,", "F,", "^F,", "G,", "^G,", "A,", "^A,", "B,", "C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B", "C'", "^C'", "D'"]
const abc_leng = ["8","4","2","","1/2"] //音符の宣言
const abc_rest = "z"                     //休符
const abc_id = ["zen","2","4","8","16"]  //音符と休符の配列
                                   
const pianoSounds = []              // Audioオブジェクト        
const touchkeyNumlish = []          // タッチ中の鍵盤番号リスト
let clickedKeyNum = null            // クリック中の鍵盤番号リスト
let abc_leng_arnum = 3              //
const isKeyPressing = new Array(30) // ピアノ鍵盤ごとの押下状態
isKeyPressing.fill(false)           // 初期値 = false            
const intervalIds = new Array(30)   // 各オーディオフェードアウトのインターバルID
intervalIds.fill(null)              // 初期値 = null           
const pianoWrap = document.getElementById("piano-wrap")     // 鍵盤全体
const whiteKeys = document.querySelectorAll(".white-key")   // 白鍵
const blackKeys = document.querySelectorAll(".black-key")   // 黒鍵
// 初期処理
const note = ["A2","Ahan2","B2","C3","Chan3","D3","Dhan3","E3","F3","Fhan3","G3","Ghan3","A3","Ahan3","B3","C4","Chan4","D4","Dhan4","E4","F4","Fhan4","G4","Ghan4","A4","Ahan4","B4","C5","Chan5","D5"]






// Audioオブジェクトを作成セット
for ( var no of note ){
    let sound = new Audio(path + no + ".wav" )
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

// 押した時の処理
document.onkeydown = function(event) {
    
    // 鍵盤番号を取得
    const obj = keyMap.find( (item) => item.pcKey === event.key )
    if ( typeof obj !== "undefined" ){
        // keyMapに含まれるキーの場合は後続処理実行
        
        pressPianoKey(obj.pianoKey)
    } 

}

// PCkey時の処理
document.onkeyup = function(event) {
    // 鍵盤番号を取得
    const obj = keyMap.find( (item) => item.pcKey === event.key )
    if ( typeof obj !== "undefined" ){
        // keyMapに含まれるキーの場合は後続処理実行
        releasePianoKey(obj.pianoKey)
        
    } 
}

function but_leng(ele){//全符　2分符　4分符　8分符 の処理
    if(ele.id == abc_id[0]){
        abc_leng_arnum = 0;
    }else if(ele.id == abc_id[1]){
        abc_leng_arnum = 1;
    }else if(ele.id == abc_id[2]){
        abc_leng_arnum = 2;
    }else if(ele.id == abc_id[3]){
        abc_leng_arnum = 3;
    }else if(ele.id == abc_id[4]){
        abc_leng_arnum = 4;
    }
}

function but_rest(){//休符の処理
    document.getElementById("input_notes").value += (abc_rest + abc_leng[abc_leng_arnum]) + ' ';
}

// ピアノ鍵盤を押下した時の処理
function pressPianoKey(keyNum){
    
    if ( !isKeyPressing[keyNum] ){
        // 鍵盤を離している場合のみ続行(長押しによる連打防止)
        isKeyPressing[keyNum] = true
        document.querySelector(`[data-key-num="${keyNum}"]`).classList.add("pressing")
        soundPlay(keyNum)
        document.getElementById("input_notes").focus()
        document.getElementById("input_notes").value += (abc_param[keyNum] + abc_leng[abc_leng_arnum]) + ' ';
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
