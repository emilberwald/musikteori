import pathlib
from musikteori.maqamator import arabic_ajnas

import pretty_midi


class MidiJinsAnalyzer:
    def __init__(self, path: pathlib.Path):
        self.midi_data = pretty_midi.PrettyMIDI(str(path))
        total_velocity = sum(sum(self.midi_data.get_chroma()))
        self.relative_chroma = [sum(semitone) / total_velocity for semitone in self.midi_data.get_chroma()]

    def get_top_similars(self):
        similars = dict()
        for shift in range(12):
            for key, value in self._get_shifted_similars(shift).items():
                if similars.get(key, (shift, 0))[-1] < value:
                    similars[key] = (shift, value)
        max_value = max([value for _, value in similars.values()])
        return {name: (pretty_midi.utilities.note_number_to_name(shift)[0], value) for name, (shift, value) in similars.items() if value == max_value}

    def _get_shifted_similars(self, shift=0):
        similarities = dict()
        for name, jins in arabic_ajnas.items():
            pitches = [(pitch + shift) % 12 for pitch in jins.pitches]
            weight = 0
            for pitch in pitches:
                # TODO: can this be done for quarter tones etc if it is computed using pitch bends etc ?
                if pitch == int(pitch):
                    weight += self.relative_chroma[pitch]
            similarities[name] = float(weight)

        max_value = max(similarities.values())
        return {name: value for name, value in similarities.items() if value == max_value}
