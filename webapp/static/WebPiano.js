class Note{
    constructor(note, duration, s_pos){
        this.note = note; // 音程
        this.duration = duration; // 音価
        this.s_pos = s_pos; //カーソル範囲(はじめ)
        this.e_pos = s_pos + note.length; //カーソル範囲(終わり)
    }
    
    //getter
    get get_note(){
        return this.note;
    }
    get get_duration(){
        return this.duration;
    }
    get get_s_pos(){
        return this.s_pos;
    }
    get get_e_pos(){
        return this.e_pos;
    }
    
    //setter
    set set_note(value){
        this.note = value;
    }
    set set_s_pos(value){
        this.s_pos = value;
    }
    set set_e_pos(value){
        this.e_pos = value;
    }
}

//bpmを変更した時
function bpm_change(event){
    var val = event.currentTarget.value;

    // abc記法のテキストボックスのヘッダを更新
    if (val > 99)
        var context = 'Q:' + val.toString(10) + '\n';
    else
        var context = 'Q:' + val.toString(10) + ' \n';
    
    note_list[0].set_note = context;
    innerText ="";
    note_list.forEach(element => {
        innerText += element.get_note;
    });
    input.value = innerText;
    input.focus()
}

// POST送信の際のデータの変換
function arrange_note(){
    var innerText ="";
    for(i = 1; i < note_list.length; i++){
        innerText += note_list[i].get_note
    }
    input.value = innerText;
}
// 変数宣言
const path = "static/audio/"             // オーディオファイルのパス
const keyMap = [
                { pcKey: "a", pianoKey: 0 , abcKey: "A,,"},
                { pcKey: "q", pianoKey: 1 , abcKey: "^A,,"},
                { pcKey: "s", pianoKey: 2 , abcKey: "B,,"},
                { pcKey: "d", pianoKey: 3 , abcKey: "C,"},
                { pcKey: "w", pianoKey: 4 , abcKey: "^C,"},
                { pcKey: "f", pianoKey: 5 , abcKey: "D,"},
                { pcKey: "e", pianoKey: 6 , abcKey: "^D,"},
                { pcKey: "g", pianoKey: 7 , abcKey: "E,"},
                { pcKey: "h", pianoKey: 8 , abcKey: "F,"},
                { pcKey: "r", pianoKey: 9 , abcKey: "^F,"},
                { pcKey: "j", pianoKey: 10 , abcKey: "G,"},
                { pcKey: "t", pianoKey: 11 , abcKey: "^G,"},
                { pcKey: "k", pianoKey: 12 , abcKey: "A,"},
                { pcKey: "y", pianoKey: 13 , abcKey: "^A,"},
                { pcKey: "l", pianoKey: 14 , abcKey: "B,"},
                { pcKey: "z", pianoKey: 15 , abcKey: "C"},
                { pcKey: "u", pianoKey: 16 , abcKey: "^C"},
                { pcKey: "x", pianoKey: 17 , abcKey: "D"},
                { pcKey: "i", pianoKey: 18 , abcKey: "^D"},
                { pcKey: "c", pianoKey: 19 , abcKey: "E"},
                { pcKey: "v", pianoKey: 20 , abcKey: "F"},
                { pcKey: "o", pianoKey: 21 , abcKey: "^F"},
                { pcKey: "b", pianoKey: 22 , abcKey: "G"},
                { pcKey: "p", pianoKey: 23 , abcKey: "^G"},
                { pcKey: "n", pianoKey: 24 , abcKey: "A"},
                { pcKey: "@", pianoKey: 25 , abcKey: "^A"},
                { pcKey: "m", pianoKey: 26 , abcKey: "B"},
                { pcKey: ",", pianoKey: 27 , abcKey: "C'"},
                { pcKey: "[", pianoKey: 28 , abcKey: "^C'"},
                { pcKey: ".", pianoKey: 29 , abcKey: "D'"},
            ] //入力ページのピアノと対応したJsonオブジェクト

var interval_start = 0 //カーソル範囲のはじめ
var interval_end = 6  //カーソル範囲の終わり
var context = "" // noteの文字列
var index = 0 //note_list参照用
var input = document.getElementById("input_notes") //テキストボックス
var note_list = new Array() // 入力メロディの情報
note_list.push(new Note("Q:100\n", 0, interval_start)); //abc記法のヘッダ
var mouse_flag = false;

//abc記法の配列
const abc_param = ["A,,", "^A,,", "B,,", "C,", "^C,", "D,", "^D,", "E,", "F,", "^F,", "G,", "^G,", "A,", "^A,", "B,", "C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B", "C'", "^C'", "D'"]
const abc_leng = ["8","4","2","","1/2"] //音符の宣言
const abc_leng_param = [4, 2, 1, 0.5, 0.25]
const abc_rest = "z"                     //休符
const abc_id = [
                {id:"zen", pcKey:"1", arnum:0},
                {id: "2", pcKey:"2", arnum:1},
                {id: "4", pcKey:"3", arnum:2},
                {id: "8", pcKey:"4", arnum:3},
                {id: "16", pcKey:"5", arnum: 4},
            ]  //音符と休符の配列
var param = document.getElementById('param')
const pianoSounds = []              // Audioオブジェクト
const touchkeyNumlish = []          // タッチ中の鍵盤番号リスト
let clickedKeyNum = null            // クリック中の鍵盤番号リスト
let abc_leng_arnum = 3              // 音価配列のindex(初期値)
const isKeyPressing = new Array(30) // ピアノ鍵盤ごとの押下状態
isKeyPressing.fill(false)           // 初期値 = false
const intervalIds = new Array(30)   // 各オーディオフェードアウトのインターバルID
intervalIds.fill(null)              // 初期値 = null
const pianoWrap = document.getElementById("piano-wrap")     // 鍵盤全体
const whiteKeys = document.querySelectorAll(".white-key")   // 白鍵
const blackKeys = document.querySelectorAll(".black-key")   // 黒鍵
// 初期処理
const note = ["A2","Ahan2","B2","C3","Chan3","D3","Dhan3","E3","F3","Fhan3","G3","Ghan3","A3","Ahan3","B3","C4","Chan4","D4","Dhan4","E4","F4","Fhan4","G4","Ghan4","A4","Ahan4","B4","C5","Chan5","D5"]
//音価button
var button = document.getElementById("8")
button.classList.add('b-pressing')

//bpmを変更したときの処理
var bpm = document.getElementById('bpm')
bpm.addEventListener('change', bpm_change)

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
    pianoWrap.addEventListener("mousedown", function(){ handleMouseEvents(event) })
    pianoWrap.addEventListener("mouseup", function(){ handleMouseEvents(event) })
    window.addEventListener("mousemove", function(){ handleMouseEvents(event) })
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
    // console.log(BeforeKeyNumllish)
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
    mouse_flag = true
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
    mouse_flag = false;
}

//音符クリック時
document.onclick = function(event){
    if(document.activeElement.id === "input_notes"){
        input.setSelectionRange //テキストボックスのカーソル位置を取得
        
        for(i = 0; i < note_list.length; i++){
            if(note_list[i].get_s_pos === input.selectionStart
            && note_list[i].get_e_pos >= input.selectionEnd){
                index = i;
                break;
            }
        }
        interval_start = note_list[index].get_s_pos;
        interval_end = note_list[index].get_e_pos;
        
    }
}

//音符挿入時の並べ替え
function sort_insert(index, list, li_len, text_length){
    for(i = li_len-1; i > index; i--){
        obj = list[i-1];
        list[i-1] = list[i];
        list[i] = obj;
        list[i].set_s_pos = list[i].get_s_pos + text_length;
        list[i].set_e_pos = list[i].get_e_pos + text_length;
    }               
}

//音符delete時の並べ替え
function sort_delete(index, list, text_length){
    for(i = index; i < list.length; i++){
        list[i].set_s_pos = list[i].get_s_pos - text_length;
        list[i].set_e_pos = list[i].get_e_pos - text_length;
    }
    note_list.splice(index, 1)
}

//テキストボックスの編集
function edit_note(abcKey){
                
    if(abcKey === "Delete"){
        if(index > 0){
            sort_delete(index, note_list, note_list[index].get_note.length)
            index--; //範囲を左に
        }
    }
    else{
        //オブジェクトに入れる音価
        abc_length = abc_leng_param[abc_leng_arnum]

        if(note_list.length % 16 === 0){
            context = abcKey + abc_leng[abc_leng_arnum] + '\n' + ' ';
        }
        else{
            context = abcKey + abc_leng[abc_leng_arnum] + ' '
        }
    
        note_list.push(new Note(context, abc_length, note_list[index].get_e_pos))
        index++; // 範囲を右に
        sort_insert(index, note_list, note_list.length, context.length)
    }
    interval_start = note_list[index].get_s_pos
    interval_end = note_list[index].get_e_pos

    innerText ="";
    note_list.forEach(element => {
        innerText += element.get_note;
    });
    input.value = innerText;
    input.setSelectionRange(interval_start, interval_end)
    input.focus();
}
// 押した時の処理
document.onkeydown = function(event) {
    
    // 鍵盤番号を取得
    const obj = keyMap.find( (item) => item.pcKey === event.key )
    
    if ( typeof obj !== "undefined" ){
        // keyMapに含まれるキーの場合は後続処理実行 
        pressPianoKey(obj.pianoKey)
    }
    else if(event.key === "Delete" || event.key === "Backspace"){
        edit_note("Delete")
    }
    else if(event.code === "Space"){
        edit_note(abc_rest);//休符の処理
    }
    else{
        // キーボード入力で音符の長さの指定
        const obj2 = abc_id.find((item) => item.pcKey === event.key)
        
        if(typeof obj2 !== "undefined"){
            button.classList.remove('b-pressing')
            button = document.getElementById(obj2.id)
            button.classList.add('b-pressing')
            abc_leng_arnum = obj2.arnum
        }
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
    const obj = abc_id.find((item) => item.id === ele.id)
    abc_leng_arnum = obj.arnum
    //押下状態のスタイルの保持
    button.classList.remove('b-pressing')
    button = document.getElementById(obj.id)
    button.classList.add('b-pressing')
}

// ピアノ鍵盤を押下した時の処理
function pressPianoKey(keyNum){
    
    if ( !isKeyPressing[keyNum] ){
        // 鍵盤を離している場合のみ続行(長押しによる連打防止)
        
        isKeyPressing[keyNum] = true
        document.querySelector(`[data-key-num="${keyNum}"]`).classList.add("pressing")
        soundPlay(keyNum)
        
        if(!mouse_flag){
            edit_note(keyMap[keyNum].abcKey);
        }    
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
