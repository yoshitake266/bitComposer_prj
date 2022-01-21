$(function(){
  //幅指定
  var h = $(window).height();
  //Wrapをゼロにする
  $('wrap').css('display','none');
  //縦に並べる
  $('loader-bg','#loader').height(h).css('display','block');
})//全ての読み込みが完了したら実行
$(window).load(function () { 
  // delayはキューを遅延
  //fadeOutはアニメーション効果は指定したスピードで実行されます。
  //
  $('#loader-bg').delay(10000).fadeOut(800);
  $('#loader').delay(600).fadeOut(300);
  $('#wrap').css('display', 'block').show();
});