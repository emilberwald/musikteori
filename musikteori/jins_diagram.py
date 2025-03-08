import argparse
import json
import pathlib
from typing import Dict, List
import maqamator


def generate_fretboard_grid(*, ajnas: Dict[str, maqamator.Jins], pitches_for_strings: List[List[float]]):
    """Generate a fretboard-like grid with pitches represented by symbols."""
    # Got a bit messy with ◯ as unused
    pitch_map = {"tonic": "✪", "modulation": "❂", "pitches": "⦿", "octave": "⛭", "extension": "⊛", "unused": ""}

    grid = []
    grid.append([str(pitch_map)])
    for jins_name, jins in ajnas.items():
        grid.append([jins_name])
        for pitches_for_string in pitches_for_strings:
            row = []
            for pitch in pitches_for_string:
                symbol = get_symbol(pitch_map, jins, pitch)
                row.append(symbol)
            grid.append(row)

    return grid


def get_symbol(pitch_map, jins: maqamator.Jins, pitch):
    assert jins.wholestep == 2.0
    symbol = None
    if pitch in jins.extension_pitches:
        symbol = pitch_map["extension"]
    if pitch in jins.pitches:
        symbol = pitch_map["pitches"]
    if pitch in jins.modulation_pitches:
        symbol = pitch_map["modulation"]
    if pitch == 0:
        symbol = pitch_map["tonic"]
    if symbol is None:
        shifted = pitch % 12
        if any([(pitch % 12) in pitches for pitches in [jins.pitches, jins.modulation_pitches]]):
            symbol = pitch_map["octave"]
        else:
            symbol = pitch_map["unused"]
    return symbol


if __name__ == "__main__":
    pitches_for_strings = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5],
        [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0],
    ]

    # Generate the fretboard grid
    grid = generate_fretboard_grid(ajnas=maqamator.arabic_ajnas, pitches_for_strings=pitches_for_strings)
    pathlib.Path("ajnas.txt").write_text("\n".join(["\t".join(row) for row in grid]), encoding="utf-8")
