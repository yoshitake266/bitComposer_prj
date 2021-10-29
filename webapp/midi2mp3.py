from midi2audio import FluidSynth



def output():
	fs = FluidSynth(sound_font='default.sf2')
	fs.midi_to_audio(r'static\media\out.mid', r'static\media\out.mp3')