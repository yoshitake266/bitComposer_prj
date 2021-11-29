from midi2audio import FluidSynth

fs = FluidSynth(sound_font = 'default.sf2')
fs.midi_to_audio('ayatitle.mid', 'ayatitle.mp3')