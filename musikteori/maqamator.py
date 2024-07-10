from typing import List


class Jins:
    def __init__(
        self,
        *,
        pitches: List[float],
        extension_pitches: List[float],
        modulation_pitches: List[float],
        wholestep: float = 2.0,
    ):
        """

        Args:
            pitches (List[float]):             The pitches of the jins in [steps]. Usually the lowest pitch is the tonic and the highest pitch the ghammaz.
            extension_pitches (List[float]):   Pitches for noodling around in that are not part of the usual pitches [steps]. Jins baggage.
            modulation_pitches (List[float]):  Modulation points in terms of pitches [steps]. (unison, ghammaz, (octave), ...)
            wholestep (float):                 Value for [steps / wholestep] (where one whole step = P5 + P5 - P8).
        """
        self.pitches = pitches
        self.extension_pitches = extension_pitches
        self.modulation_pitches = modulation_pitches
        self.wholestep = wholestep


arabic_ajnas = {
    "Ajam5": Jins(pitches=[0, 2, 4, 5, 7], extension_pitches=[-1, -3, 9], modulation_pitches=[0, 7]),
    "UpperAjam": Jins(pitches=[0, 2, 4, 5], extension_pitches=[-2, 7], modulation_pitches=[0, 5]),
    "Ajam3": Jins(pitches=[0, 2, 4], extension_pitches=[-1, -3, 5, 7], modulation_pitches=[0, 4]),
    "AjamMurassa": Jins(pitches=[0, 2, 4, 6, 7], extension_pitches=[-1, 9], modulation_pitches=[0, 7]),
    "AtharKurd": Jins(pitches=[0, 1, 3, 6, 7], extension_pitches=[-1, -4, 8], modulation_pitches=[0, 7]),
    "Bayati": Jins(pitches=[0, 1.5, 3, 5], extension_pitches=[-2, -3.5, 7, 8], modulation_pitches=[0, 5]),
    "Hijaz": Jins(pitches=[0, 1, 4, 5], extension_pitches=[-2, -3.5, 7, 8], modulation_pitches=[0, 5]),
    "HijazMurassa": Jins(pitches=[0, 1, 4, 5, 6], extension_pitches=[-2, -1], modulation_pitches=[0, 5]),
    "Hijazkar": Jins(pitches=[0, 3, 4, 5, 8, 9], extension_pitches=[], modulation_pitches=[4]),
    # https://tuning.ableton.com/arabic-maqam/jiharkah/ 378c 460c
    # https://maqamworld.com/en/jins/jiharkah.php [293.33, 321.33, 347.65, 391.11, 433, 454, 521.48]Hz ~ [-294,  -136, 0, 204, 380, 462, 702]c
    "Jiharkah": Jins(pitches=[0, 2, 4 - 0.2, 5 - 0.4, 7], extension_pitches=[-1.33, -3], modulation_pitches=[0, 7]),
    "Kurd": Jins(pitches=[0, 1, 3, 5], extension_pitches=[-2, 7, 8], modulation_pitches=[0, 5]),
    "Lami": Jins(pitches=[0, 1, 3, 5, 6], extension_pitches=[8], modulation_pitches=[0, 5]),
    "MukhalifSharqi": Jins(pitches=[0, 1.5, 2.5], extension_pitches=[], modulation_pitches=[0]),
    "Mustaar": Jins(pitches=[0, 2.5, 3.5], extension_pitches=[-0.5, 2, 1], modulation_pitches=[0]),
    "Nahawand": Jins(pitches=[0, 2, 3, 5, 7], extension_pitches=[-1, -3, -4, 8], modulation_pitches=[0, 7]),
    "NahawandMurassa": Jins(pitches=[0, 2, 3, 5, 6], extension_pitches=[-1, 9], modulation_pitches=[0]),
    "Nikriz": Jins(pitches=[0, 2, 3, 6, 7], extension_pitches=[-1, -4, 8, 9, 10], modulation_pitches=[0, 7]),
    "Rast": Jins(pitches=[0, 2, 3.5, 5, 7], extension_pitches=[-0.5, -3, 8, 9], modulation_pitches=[0, 7]),
    "Saba": Jins(pitches=[0, 1.5, 3, 4, 7, 8], extension_pitches=[-2, -3.5], modulation_pitches=[0, 3, 8]),
    "SabaDalanshin": Jins(pitches=[0, 1.5, 3, 4, 7, 8], extension_pitches=[-1, -2], modulation_pitches=[0, 3]),
    "SabaZamzam": Jins(pitches=[0, 1, 3, 4, 7, 8], extension_pitches=[-2], modulation_pitches=[0, 3, 8]),
    "Sazkar": Jins(pitches=[0, 3, 3.5, 5, 7], extension_pitches=[-0.5, 9], modulation_pitches=[0, 7]),
    "Sikah": Jins(pitches=[0, 1.5, 3.5], extension_pitches=[-0.5, -1.5, -3.5, 4.5], modulation_pitches=[0, 3.5]),
    # https://maqamworld.com/en/jins/sikah_baladi.php [315, 364, 391.11, 425, 485, 515]Hz ~ [-375, -124, 0, 144, 372, 476]c
    "SikahBaladi": Jins(pitches=[-3.77, -1.22, 0, 1.44, 3.7, 4.77], extension_pitches=[], modulation_pitches=[0]),
    "UpperRast": Jins(pitches=[0, 2, 3.5, 5], extension_pitches=[-2, 7], modulation_pitches=[0, 5]),
}

# TODO: some kind of network traverser using networkx, for sayr and maqam
# TODO: Instead of floats, use accidentals, and inject "dialect"?
