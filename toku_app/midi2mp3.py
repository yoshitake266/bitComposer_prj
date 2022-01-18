from midi2audio import FluidSynth
import os


def output():
	path = os.path.dirname(__file__) + '/'
	fs = FluidSynth(sound_font= path + 'static/media/default.sf2')
	fs.midi_to_audio(path + 'static/media/out.mid', path + 'static/media/out.mp3')
	fs.midi_to_audio(path + 'static/media/out.mid', path + 'static/media/out.wav')
