
let spectrum = fft.analyze();// FFTの結果を取得
noStroke();

for (let i = 0; i< spectrum.length; i++){

 fill(255, 255*i/spectrum.length, 0); // 色を指定する

 let x = map(i, 0, spectrum.length, 0, width); // 周波数を計算する

 let h = -height + map(spectrum[i], 0, 255, height, 0); // 振幅を計算する

 rect(x+50, height, width / spectrum.length, h ) // 棒グラフ1つ分を作成する

} 

// Get the values of different frequency ranges
var bass = fft.getEnergy( "bass" );
var mid = fft.getEnergy( "mid" );
var treble = fft.getEnergy( "treble" );

// Map the range of each volume with your desired number
var mapBass = map( bass, 0, 255, -100, 100 );
var mapMid = map( mid, 0, 255, -150, 150 );
var treble = fft.getEnergy( treble, 0, 255, -200, 200 );

for( i = 0; i < pieces; i++ ) {

  rotate( TWP_PI / pieces );

  // Draw the bass lines
  line( mapBass, radius/2, 0, radius );

  // Draw the mid lines
  line( mapMid, radius/2, 0, radius );

  // Draw the treble lines
  line( mapTreble, radius/2, 0, radius );

}
function preload(){  //  音源を定義する

    sound = loadSound('13647.mp3'); // 音声データを読み込む
    //  予めOpen Processingにアップロードする
  }
  function play_stop() { // 音源を再生・停止する

    if (sound.isPlaying()) { // 音源が再生している時
      sound.pause(); //  音源を停止する
          playButton.html("Pause"); // ボタンを停止に変える
    } 
  
      else { // 音源が停止している時
      sound.loop(); // 音源を再生する
          playButton.html("Play"); //  ボタンを再生に変える
    }
  
  }   
  