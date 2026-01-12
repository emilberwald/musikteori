import pathlib
from musikteori.midi_analyzer import MidiJinsAnalyzer


class TestMidiAnalyzer:
    def test_nahawand(self):
        analyzer = MidiJinsAnalyzer(pathlib.Path("G:/Musik/nihavend_longa.mid.mid"))
        similars = analyzer.get_top_similars()
        assert "nahawand" in {key.lower() for key in similars.keys()}
