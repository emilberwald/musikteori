import argparse
import json
import pathlib
from typing import Dict, List

import numpy
import maqamator


class Printer:
    def __init__(self, ajnas: Dict[str, maqamator.Jins]):
        # Got a bit messy with ◯ as unused
        self.pitch_map = {
            "tonic": "✪",
            "modulation": "❂",
            "pitches": "⦿",
            "octave": "⛭",
            "extension": "⊛",
            "unused": "",
        }
        # Generate the fretboard grid
        steps = numpy.linspace(0, 10, 41).tolist()
        self._pitches_for_strings = [
            steps,
            [step - 5 for step in steps],
            [step - 10 for step in steps],
        ]
        self._atol = (
            float(min([min(numpy.diff(pitches_for_string)) for pitches_for_string in self._pitches_for_strings])) * 0.5
        )
        self._name_to_grid = self._generate_fretboard_grid(ajnas=ajnas)

    def _generate_fretboard_grid(self, *, ajnas: Dict[str, maqamator.Jins]):
        """Generate a fretboard-like grid with pitches represented by symbols."""
        name_to_grid = dict()
        for jins_name, jins in ajnas.items():
            name_to_grid[jins_name] = []
            for pitches_for_string in self._pitches_for_strings:
                row = []
                for pitch in pitches_for_string:
                    symbol = self._get_symbol(self.pitch_map, jins, pitch)
                    row.append(symbol)
                name_to_grid[jins_name].append(row)

        return name_to_grid

    def __str__(self):
        return "\n".join(
            [
                str(self.pitch_map),
                "\n".join(
                    [
                        "\n".join(
                            [
                                name,
                                self._name_to_grid_to_string(pitches_for_strings=self._pitches_for_strings, grid=grid),
                            ]
                        )
                        for name, grid in self._name_to_grid.items()
                    ]
                ),
            ]
        )

    def _approx_in(self, query: float, items: List[float]):
        return any(abs(query - reference) <= self._atol for reference in items)

    def _get_symbol(self, pitch_map, jins: maqamator.Jins, pitch):
        assert jins.wholestep == 2.0
        symbol = None
        if self._approx_in(pitch, jins.extension_pitches):
            symbol = pitch_map["extension"]
        if self._approx_in(pitch, jins.pitches):
            symbol = pitch_map["pitches"]
        if self._approx_in(pitch, jins.modulation_pitches):
            symbol = pitch_map["modulation"]
        if pitch == 0:
            symbol = pitch_map["tonic"]
        if symbol is None:
            shifted = pitch % 12
            if any([self._approx_in(pitch % 12, pitches) for pitches in [jins.pitches, jins.modulation_pitches]]):
                symbol = pitch_map["octave"]
            else:
                symbol = pitch_map["unused"]
        return symbol

    def _name_to_grid_to_string(self, *, pitches_for_strings, grid):
        text = ""
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                closest_pitch = pitches_for_strings[i][j]
                fractional_part = closest_pitch - int(closest_pitch)
                if fractional_part == 0:
                    if j > 0:
                        text += "\t"
                    if col == "":
                        text += "◯"
                    else:
                        text += str(col)
                else:
                    if col == "":
                        text += " "
                    else:
                        text += str(col)

            text += "\n"
        return text


if __name__ == "__main__":

    pathlib.Path("ajnas.txt").write_text(
        str(Printer(ajnas=maqamator.arabic_ajnas)),
        encoding="utf-8",
    )
