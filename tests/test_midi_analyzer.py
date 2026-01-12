import pathlib
from musikteori.midi_analyzer import MidiJinsAnalyzer


class TestMidiAnalyzer:
    def test_nahawand(self):
        analyzer = MidiJinsAnalyzer(pathlib.Path("G:/Musik/nihavend_longa.mid.mid"))
        similars = analyzer.get_top_similars()
        assert "Nahawand" in similars.keys()

    def test_g_minor(self):
        analyzer = MidiJinsAnalyzer(pathlib.Path("G:/Musik/Passacaglia.mid"))
        similars = analyzer.get_top_similars()
        assert similars["Nahawand"][0] == "G"
