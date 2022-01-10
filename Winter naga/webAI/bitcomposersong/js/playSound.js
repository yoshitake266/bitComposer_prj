var soundID = "Thunder";

function loadSound () {
    createjs.Sound.registerSound("assets/AnyConv.com__test_output.wav", soundID);
  }
  function playSound () {
    createjs.Sound.play(soundID);
  }