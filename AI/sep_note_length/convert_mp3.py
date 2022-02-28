from midi2audio import FluidSynth

fs = FluidSynth(sound_font = 'default.sf2')
fs.midi_to_audio('output/test_output.mid', 'output/test_output.mp3')