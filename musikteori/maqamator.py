from typing import List, Optional


class Jins:
    def __init__(
        self,
        *,
        pitches: List[float],
        extension_pitches: List[float] = [],
        modulation_pitches: Optional[List[float]] = None,
        wholestep: float = 2.0,
    ):
        """

        Args:
            pitches (List[float]):                      The pitches of the jins in [steps]. Usually the lowest pitch is the tonic and the highest pitch the ghammaz.
            extension_pitches (List[float]):            Pitches for noodling around in that are not part of the usual pitches [steps]. Jins baggage. Default: [].
            modulation_pitches (Optional[List[float]]): Modulation points in terms of pitches [steps]. (unison, ghammaz, (octave), ...). Set to pitches if None.
            wholestep (float):                          Value for [steps / wholestep] (where one whole step = P5 + P5 - P8).
        """
        self.pitches = pitches
        self.extension_pitches = extension_pitches
        self.modulation_pitches = pitches if modulation_pitches is None else modulation_pitches
        self.wholestep = wholestep


def nonstandard_ajnas():
    # https://ianring.com/musictheory/scales/finder/
    # https://www.flutopedia.com/scale_catalog.htm
    # https://www.daqarta.com/dw_ss0a.htm
    # and others just made up...

    triads = {
        "indu3": [0, 1, 2],
        "kurd3": [0, 1, 3],
        "hijaz3": [0, 1, 4],
        "sus b2 4": [0, 1, 5],
        "vienesse": [0, 1, 6],
        "sus b2": [0, 1, 7],
        "sus b2 aug5": [0, 1, 8],
        "sus b2 6": [0, 1, 9],
        "sus b2 (b)7": [0, 1, 10],
        "sus b2 [maj]7": [0, 1, 11],
        "nahawand3": [0, 2, 3],
        "ajam3": [0, 2, 4],
        "sus2 4": [0, 2, 5],
        "sus2 b5": [0, 2, 6],
        "sus2": [0, 2, 7],
        "sus2 aug5": [0, 2, 8],
        "sus2 aug5 ": [0, 2, 8],
        "sus2 6": [0, 2, 9],
        "sus2 (b)7": [0, 2, 10],
        "sus2 [maj]7": [0, 2, 11],
        "hijazkar3": [0, 3, 4],
        "vietnamese": [0, 3, 5],
        "dim": [0, 3, 6],
        "min": [0, 3, 7],
        "ute aug5": [0, 3, 8],
        "ute 6": [0, 3, 9],
        "ute (b)7": [0, 3, 10],
        "ute [maj]7": [0, 3, 11],
        "tense3": [0, 4, 5],
        "b5": [0, 4, 6],
        "maj": [0, 4, 7],
        "aug": [0, 4, 8],
        "bilwadala": [0, 4, 9],
        "italian aug6": [0, 4, 10],
        "MOTian": [0, 4, 11],
        "tense4": [0, 5, 6],
        "sus4": [0, 5, 7],
        "sarvasri aug5": [0, 5, 8],
        "bugle": [0, 5, 9],
        "sansagari": [0, 5, 10],
        "MODian": [0, 5, 11],
        "ongkari": [0, 6, 7],
        "CAHian": [0, 6, 8],
        "ILLian": [0, 6, 9],
        "GOCian": [0, 6, 10],
        "enigma3": [0, 6, 11],
        "tense5": [0, 7, 8],
        "maj6 no3": [0, 7, 9],
        "dom7 no3": [0, 7, 10],
        "[maj]7 no3": [0, 7, 11],
        "tenseb6": [0, 8, 9],
        "aug(5) (b)7 no3": [0, 8, 10],
        "aug(5) [maj]7 no3": [0, 8, 11],
        "tense 6": [0, 9, 10],
        "PODian": [0, 9, 11],
        "tense (b)7": [0, 10, 11],
    }

    tetrads = {
        "dim add5": [0, 3, 6, 7],
        "mynic": [0, 3, 6, 8],
        "dim7": [0, 3, 6, 9],
        "half dim7": [0, 3, 6, 10],
        "dim [maj]7": [0, 3, 6, 11],
        "lothic": [0, 3, 7, 8],
        "min 6": [0, 3, 7, 9],
        "min (b)7": [0, 3, 7, 10],
        "min [maj]7": [0, 3, 7, 11],
        "BIRian": [0, 4, 6, 7],
        "koptic": [0, 4, 6, 8],
        "saric": [0, 4, 6, 9],
        "dom7b5": [0, 4, 6, 10],
        "epogic": [0, 4, 7, 8],
        "maj6": [0, 4, 7, 9],
        "dom7": [0, 4, 7, 10],
        "(maj) [maj]7": [0, 4, 7, 11],
        "aeoloric": [0, 4, 8, 9],
        "aug(5) (b)7": [0, 4, 8, 10],
        "aug(5) [maj]7": [0, 4, 8, 11],
    }

    # TODO: add more
    # TODO: group by commonality?
    ajnas = dict()
    for name, pitches in triads.items():
        ajnas[name] = Jins(pitches=pitches)
    for name, pitches in tetrads.items():
        ajnas[name] = Jins(pitches=pitches)
    return ajnas


arabic_ajnas = {
    "SabaZamzam": Jins(pitches=[0, 1, 3, 4, 7, 8], extension_pitches=[-2], modulation_pitches=[0, 3, 8]),
    "Kurd": Jins(pitches=[0, 1, 3, 5], extension_pitches=[-2, 7, 8], modulation_pitches=[0, 5]),
    "Lami": Jins(pitches=[0, 1, 3, 5, 6], extension_pitches=[8], modulation_pitches=[0, 5]),
    "AtharKurd": Jins(pitches=[0, 1, 3, 6, 7], extension_pitches=[-1, -4, 8], modulation_pitches=[0, 7]),
    "Hijaz": Jins(pitches=[0, 1, 4, 5], extension_pitches=[-2, -3.5, 7, 8], modulation_pitches=[0, 5]),
    "HijazMurassa": Jins(pitches=[0, 1, 4, 5, 6], extension_pitches=[-2, -1], modulation_pitches=[0, 5]),
    "MukhalifSharqi": Jins(pitches=[0, 1.5, 2.5], extension_pitches=[], modulation_pitches=[0]),
    "Saba": Jins(pitches=[0, 1.5, 3, 4, 7, 8], extension_pitches=[-2, -3.5], modulation_pitches=[0, 3, 8]),
    "SabaDalanshin": Jins(pitches=[0, 1.5, 3, 4, 7, 8], extension_pitches=[-1, -2], modulation_pitches=[0, 3]),
    "Bayati": Jins(pitches=[0, 1.5, 3, 5], extension_pitches=[-2, -3.5, 7, 8], modulation_pitches=[0, 5]),
    # https://maqamworld.com/en/jins/sikah.php [260.74, 293.33, 310, 320, 347.65, 391.11, 422]Hz ~ [-354, -151, -55, 0, 144, 347, 479]c
    "Sikah": Jins(pitches=[0, 1.5, 3.5], extension_pitches=[-0.5, -1.5, -3.5, 4.5], modulation_pitches=[0, 3.5]),
    "NahawandMurassa": Jins(pitches=[0, 2, 3, 5, 6], extension_pitches=[-1, 9], modulation_pitches=[0]),
    "Nahawand": Jins(pitches=[0, 2, 3, 5, 7], extension_pitches=[-1, -3, -4, 8], modulation_pitches=[0, 7]),
    "Nikriz": Jins(pitches=[0, 2, 3, 6, 7], extension_pitches=[-1, -4, 8, 9, 10], modulation_pitches=[0, 7]),
    # https://maqamworld.com/en/jins/rast.php [220, 241, 260.74, 293.33, 320, 347.65, 391.11, 422, 440]Hz ~ [-294, -136, 0, 204, 355, 498, 702, 834, 906]c
    "Rast": Jins(pitches=[0, 2, 3.5, 5, 7], extension_pitches=[-1.5, -3, 8, 9], modulation_pitches=[0, 7]),
    "UpperRast": Jins(pitches=[0, 2, 3.5, 5], extension_pitches=[-2, 7], modulation_pitches=[0, 5]),
    # https://tuning.ableton.com/arabic-maqam/jiharkah/ 378c 460c
    # https://maqamworld.com/en/jins/jiharkah.php [293.33, 321.33, 347.65, 391.11, 433, 454, 521.48]Hz ~ [-294,  -136, 0, 204, 380, 462, 702]c
    "Jiharkah": Jins(pitches=[0, 2, 4 - 0.2, 5 - 0.4, 7], extension_pitches=[-1.33, -3], modulation_pitches=[0, 7]),
    "Ajam5": Jins(pitches=[0, 2, 4, 5, 7], extension_pitches=[-1, -3, 9], modulation_pitches=[0, 7]),
    "UpperAjam": Jins(pitches=[0, 2, 4, 5], extension_pitches=[-2, 7], modulation_pitches=[0, 5]),
    "Ajam3": Jins(pitches=[0, 2, 4], extension_pitches=[-1, -3, 5, 7], modulation_pitches=[0, 4]),
    "AjamMurassa": Jins(pitches=[0, 2, 4, 6, 7], extension_pitches=[-1, 9], modulation_pitches=[0, 7]),
    # https://maqamworld.com/en/jins/sikah_baladi.php [315, 364, 391.11, 425, 485, 515]Hz ~ [-375, -124, 0, 144, 372, 476]c
    # NOTE: Sikah ~ [0, 150, 350]c
    # NOTE: SikahBaladi ~ [0, 255, 377, 521, 747, 854]c from root (instead of from tonic)
    "SikahBaladi": Jins(pitches=[-3.77, -1.22, 0, 1.44, 3.7, 4.77], extension_pitches=[], modulation_pitches=[0]),
    "Mustaar": Jins(pitches=[0, 2.5, 3.5], extension_pitches=[-0.5, 2, 1], modulation_pitches=[0]),
    # https://maqamworld.com/en/jins/sazkar.php [241, 260.74, 310, 320, 347.65, 391.11, 440]Hz ~ [-136, 0, 300, 355, 498, 702, 906]c
    "Sazkar": Jins(pitches=[0, 3, 3.5, 5, 7], extension_pitches=[-1.5, 9], modulation_pitches=[0, 7]),
    "Hijazkar": Jins(pitches=[0, 3, 4, 5, 8, 9], extension_pitches=[], modulation_pitches=[4]),
}

# TODO: some kind of network traverser using networkx, for sayr and maqam
# TODO: Instead of floats, use accidentals, and inject "dialect"?


