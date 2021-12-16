from midi2audio import FluidSynth
import os


def output():
	fs = FluidSynth(sound_font= './static/media/default.sf2')
	fs.midi_to_audio('./static/media/out.mid', './static/media/out.mp3')
