var deme;
(function(deme){
  var SoundVisualizer = (function (){
    function SoundVisualizer(){
        var _this = this;
       /** サウンドID*/ 
       this.SOUND_ID = "sound";
       /**boxの間隔 */
       this.BOX_INTERVAL = 100;
       /**color */
       this.START_COLOR = 0x2DADAC;
       this.END_COLOR = 0xFF337A;
        /** フーリエ変換を行う分割数。2の乗数でなくてはならない */
        this.FFTSIZE =64;
        /** Boxを描画するカウント */
        this.drawCount = -1;



    }

  }

})