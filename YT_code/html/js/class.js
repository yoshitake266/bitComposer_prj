class Note{
    constructor(note, duration, s_pos, e_pos){
        this.note = note;
        this.duration = duration;
        this.s_pos = s_pos; //カーソル範囲(はじめ)
        this.e_pos = e_pos; //カーソル範囲(終わり)
    }
    
    get_note(){
        return this.note;
    }
    get_duration(){
        return this.duration;
    }
    get_s_pos(){
        return this.s_pos;
    }
    get_e_pos(){
        return this.e_pos;
    }
    
    set_s_pos(value){
        this.s_pos = value;
    }
    set_e_pos(value){
        this.e_pos = value;
    }
}

class Test{
    constructor(value){
        this.value = value
    }
    show(){
        console.log(this.value)
    }
}