let playButton;
let volumeSlider;
let speedSlider;

function setup(){
	
  createCanvas(windowWidth,windowHeight);
	
	playButton = createButton("Play");
	playButton.size(100, 50);
	playButton.position(100, 20);
	playButton.style('background-color', color(30));
	playButton.style('color', color(200));
	playButton.mousePressed(play_stop);
	
	volumeSlider = createSlider(0, width, width/2);
	volumeSlider.position(250, 50);
	
	speedSlider = createSlider(0, width, width/2);
	speedSlider.position(400, 50);
	
  fft = new p5.FFT();
	
}

function draw(){
	
  background(50);
	
  let spectrum = fft.analyze();
  noStroke();
	
  for (let i = 0; i< spectrum.length; i++){
		fill(255, 255*i/spectrum.length, 0);
    let x = map(i, 0, spectrum.length, 0, width);
    let h = -height + map(spectrum[i], 0, 255, height, 0);
    rect(x+50, height, width / spectrum.length, h )
  }
	
	let volume = map(volumeSlider.value(), 0, width, 0, 0.5);
	volume = constrain(volume, 0.001, 0.1);
  sound.amp(volume);

	let speed = map(speedSlider.value(), 0.1, width, 0, 2);
	speed = constrain(speed, 0.5, 2);
	sound.rate(speed);
	
}

function preload(){
  sound = loadSound('13647.mp3');
}

function play_stop() {
	
  if (sound.isPlaying()) {
    sound.pause();
		playButton.html("Pause");
  } 
	
	else {
    sound.loop();
		playButton.html("Play");
  }
	
}	
