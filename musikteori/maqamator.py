from typing import List, Optional
import enum


class Jins:
    def __init__(
        self,
        *,
        pitches: List[float],
        extension_pitches: List[float] = [],
        modulation_pitches: Optional[List[float]] = None,
        tonics: List[float] = [0],
        wholestep: float = 2.0,
    ):
        """

        Args:
            pitches (List[float]):                      The pitches of the jins in [steps]. Usually the lowest pitch is the tonic and the highest pitch the ghammaz. Tonic should be 0.
            extension_pitches (List[float]):            Pitches for noodling around in that are not part of the usual pitches [steps]. Jins baggage. Default: [].
            modulation_pitches (Optional[List[float]]): Modulation points in terms of pitches [steps]. (unison, ghammaz, (octave), ...). Set to pitches if None.
            tonics (List[float]):                       The tonics, in order of decreasing rank
            wholestep (float):                          Value for [steps / wholestep] (where one whole step = P5 + P5 - P8).
        """
        self.pitches = pitches
        self.extension_pitches = extension_pitches
        self.modulation_pitches = pitches if modulation_pitches is None else modulation_pitches
        self.tonics = tonics
        self.wholestep = wholestep


class TurkishChord:
    def __init__(self, *, intervals: str, guclu: int | None = None):
        """Turkish Chord

        Args:
            intervals (str): The intervals in turkish notation (e.g. FBSKTA komas)
            guclu (int | None, optional): None if not applicable, 4 if the first part is a tetrachord, 5 if pentachord. Defaults to None.
        """
        self.intervals = intervals
        self.guclu = guclu


def turkish_jins_factory(*, turkish_chord: TurkishChord, common_turkish_chords: List[TurkishChord]):
    """Factory to help create Jins from turkish Makam
    NOTE: See Geçki

    Args:
        turkish_chord (TurkishChord): The chord to convert to a Jins
        common_turkish_turkish_chord (List[str]): Will be used to guess more modulation points by checking substrings against intervals

    Raises:
        ValueError: If something went wrong
    """

    class TurkishSemitones(enum.Enum):
        F = 1 * 12.0 / 53.0
        B = 4 * 12.0 / 53.0
        S = 5 * 12.0 / 53.0
        K = 8 * 12.0 / 53.0
        T = 9 * 12.0 / 53.0
        A = 12 * 12.0 / 53.0

    def get_pitches(intervals: str):
        pitches = [0]
        for interval in intervals:
            if interval == "F":
                pitches.append(pitches[-1] + TurkishSemitones.F)
            elif interval == "B":
                pitches.append(pitches[-1] + TurkishSemitones.B)
            elif interval == "S":
                pitches.append(pitches[-1] + TurkishSemitones.S)
            elif interval == "K":
                pitches.append(pitches[-1] + TurkishSemitones.K)
            elif interval == "T":
                pitches.append(pitches[-1] + TurkishSemitones.T)
            elif interval == "A":
                pitches.append(pitches[-1] + TurkishSemitones.A)
            else:
                raise ValueError(f"Unrecognized: {interval}")
        return pitches

    pitches = get_pitches(turkish_chord.intervals)
    modulation_pitches = []
    for pitch in {pitches[0], pitches[-1]}:
        modulation_pitches.append(pitch)
    if turkish_chord.guclu is not None:
        modulation_pitches.append(turkish_chord.guclu)
    for common_jins in common_turkish_chord:
        if common_jins.intervals in turkish_chord.intervals:
            modulation_pitches.append(turkish_chord.intervals.index(common_jins.intervals))
    return Jins(pitches=pitches, modulation_pitches=modulation_pitches)


common_turkish_chords = {
    "Kurdi4": TurkishChord(intervals="BTT"),
    "Kurdi5": TurkishChord(intervals="BTTT"),
    "Hicaz4Nihavend": TurkishChord(intervals="BAS"),
    "Huzzam5": TurkishChord(intervals="STSA"),
    "Segah5": TurkishChord(intervals="STKT"),
    "Ferahnak5": TurkishChord(intervals="STTK"),
    "Hicaz4": TurkishChord(intervals="SAS"),
    "Hicaz5": TurkishChord(intervals="SAST"),
    "Hicaz4Segah": TurkishChord(intervals="SAB"),
    "Kaba4": TurkishChord(intervals="KSS"),
    "Ussak4": TurkishChord(intervals="KST"),
    "Karcigar": TurkishChord(intervals="KSTSAST", guclu=4),
    "Huseyni5": TurkishChord(intervals="KSTT"),
    "Buselik4": TurkishChord(intervals="TBT"),
    "Buselik5": TurkishChord(intervals="TBTT"),
    "Nihavend": TurkishChord(intervals="TBTTBAS", guclu=5),
    "Mustear5": TurkishChord(intervals="TSKT"),
    "Nikriz5": TurkishChord(intervals="TSAS"),
    "Neveser": TurkishChord(intervals="TSASSAS", guclu=5),
    "Rast4": TurkishChord(intervals="TKS"),
    "Rast5": TurkishChord(intervals="TKST"),
    "Cargah4": TurkishChord(intervals="TTB"),
    "Cargah5": TurkishChord(intervals="TTBT"),
    "Pencgah5": TurkishChord(intervals="TTKS"),
}

turkish_ajnas = {
    name: turkish_jins_factory(turkish_chord=chord, common_turkish_chords=list(common_turkish_chords.values()))
    for name, chord in common_turkish_chords.items()
}


def letters(jins: Jins, zero_letter: str, zero_octave: int = 4, octave_letter: str = "C"):
    """Return an array of letters representing the scale.

    Args:
        zero (str): The 0 note.
        zero_octave (int): The octave-letter-based octave the letter belongs to.
        octave_letter (str): The octave root note.
    """
    result = []
    quartertone_symbols = [
        "A♮",
        "A𝄲",
        "B♭",
        "B𝄳",
        "B♮",
        "C𝄳",
        "C♮",
        "C𝄲",
        "D♭",
        "D𝄳",
        "D♮",
        "D𝄲",
        "E♭",
        "E𝄳",
        "E♮",
        "F𝄳",
        "F♮",
        "F𝄲",
        "G♭",
        "G𝄳",
        "G♮",
        "G𝄲",
        "A♭",
        "A𝄳",
    ]
    zero_index = quartertone_symbols.index(f"{zero_letter[0]}♮")
    octave_index = quartertone_symbols.index(f"{octave_letter[0]}♮")
    notes = sorted(set(jins.pitches + jins.extension_pitches + jins.modulation_pitches + jins.tonics))
    for note in notes:
        quartertone_number = (note / jins.wholestep) * 4.0 + zero_index
        decimalpart = quartertone_number - int(quartertone_number)
        if decimalpart <= -0.5:
            quartertone_number = quartertone_number - 1
            decimalpart += 1
        elif 0.5 <= decimalpart:
            quartertone_number = quartertone_number + 1
            decimalpart -= 1
        else:
            quartertone_number = quartertone_number
        symbol_octaveless = quartertone_symbols[int(quartertone_number) % len(quartertone_symbols)]
        octave = int((quartertone_number - octave_index) / len(quartertone_symbols)) + zero_octave
        complete_symbol = f"{symbol_octaveless[0]}{octave}{symbol_octaveless[1]}"
        if decimalpart > 0:
            complete_symbol += f"+{round(50.0 * decimalpart)}¢"
        elif decimalpart < 0:
            complete_symbol += f"{round(50.0 * decimalpart)}¢"
        result.append(complete_symbol)
    return result


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
        "ajam3": [0, 2, 4],  # wholetone trichord
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
        # wholetone span
        "indu4": [0, 1, 2, 5],
        "ADOian": [0, 1, 3, 4],
        "kurd4": [0, 1, 3, 5],  # netra chakra (subset)
        "hijaz4": [0, 1, 4, 5],  # agni chakra (subset)
        "nahawand4": [0, 2, 3, 5],  # veda chakra (subset)
        "ajam4": [0, 2, 4, 5],  # bana chakra (subset)
        "hijazkar4": [0, 3, 4, 5],  # rutu chakra (subset)
        "APHian": [0, 1, 2, 4],
        "rishi4": [0, 1, 2, 6],  # rishi chakra (subset)
        "vasu4": [0, 1, 3, 6],  # vasu chakra (subset)
        "brahma4": [0, 1, 4, 6],  # brahma chakra (subset)
        "IPRian": [0, 1, 5, 6],
        "ADUian": [0, 2, 3, 4],
        "disi4": [0, 2, 3, 6],  # disi chakra (subset)
        "rudra4": [0, 2, 4, 6],  # rudra chakra (subset)
        "APOian": [0, 2, 5, 6],
        "aditya4": [0, 3, 4, 6],  # aditya chakra (subset)
        "EDWian": [0, 3, 5, 6],
        "ARUian": [0, 4, 5, 6],
        "inuit": [0, 2, 4, 7],  # inuit tetratonic
        "primum": [0, 2, 5, 7],  # genus primum
        "BAJian": [0, 3, 4, 7],
        "vietnamese": [0, 3, 5, 7],  # vietnamese tetratonic
        "BABian": [0, 2, 3, 7],
        "AYOian": [0, 1, 3, 7],
        "BAPian": [0, 1, 5, 7],
        "BEMian": [0, 3, 6, 7],
        "BEXian": [0, 4, 5, 7],
        "inuit4": [0, 2, 4, 7],
        "mixolyric": [0, 2, 4, 8],
        "lanic": [0, 3, 4, 8],
        "haripriya4": [0, 3, 5, 8],
        "mynic": [0, 3, 5, 8],
        "BEKian": [0, 2, 6, 7],
        "lonic": [0, 3, 6, 8],
        "french 6": [0, 2, 6, 8],
        "gonic": [0, 4, 5, 8],
        "BIRian": [0, 4, 6, 7],
        # larger span
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
    "SabaDalanshin": Jins(
        pitches=[-3, -1.5, 0, 1, 4, 5], extension_pitches=[-4, -5], modulation_pitches=[-3, 0], tonics=[0, -3]
    ),
    "Bayati": Jins(pitches=[0, 1.5, 3, 5], extension_pitches=[-2, -3.5, 7, 8], modulation_pitches=[0, 5]),
    # https://maqamworld.com/en/jins/sikah.php [260.74, 293.33, 310, 320, 347.65, 391.11, 422]Hz ~ [-354, -151, -55, 0, 144, 347, 479]c
    "Sikah": Jins(pitches=[0, 1.5, 3.5], extension_pitches=[-0.5, -1.5, -3.5, 4.5], modulation_pitches=[0, 3.5]),
    "Husayni": Jins(pitches=[0, 2, 3, 3.5, 5, 7], modulation_pitches=[0]),
    "NahawandMurassa": Jins(pitches=[0, 2, 3, 5, 6], extension_pitches=[-1, 9], modulation_pitches=[0]),
    # Pretty sure 5 is a modulation pitch for Nahawand
    "Nahawand": Jins(pitches=[0, 2, 3, 5, 7], extension_pitches=[-1, -3, -4, 8], modulation_pitches=[0, 7]),
    "Nikriz": Jins(pitches=[0, 2, 3, 6, 7], extension_pitches=[-1, -4, 8, 9, 10], modulation_pitches=[0, 7]),
    # https://maqamworld.com/en/jins/rast.php [220, 241, 260.74, 293.33, 320, 347.65, 391.11, 422, 440]Hz ~ [-294, -136, 0, 204, 355, 498, 702, 834, 906]c
    "Rast": Jins(pitches=[0, 2, 3.5, 5, 7], extension_pitches=[-1.5, -3, 8, 9], modulation_pitches=[0, 7]),
    "UpperRast": Jins(pitches=[-5, -3, -1.5, 0], extension_pitches=[-7, 2], modulation_pitches=[-5, 0]),
    # https://tuning.ableton.com/arabic-maqam/jiharkah/ 0c 209c 378c 460c 702c 1061c
    # https://maqamworld.com/en/jins/jiharkah.php [293.33, 321.33, 347.65, 391.11, 433, 454, 521.48]Hz ~ [-294,  -136, 0, 204, 380, 462, 702]c
    "Jiharkah": Jins(pitches=[0, 2, 4 - 0.2, 5 - 0.4, 7], extension_pitches=[-1.5, -3], modulation_pitches=[0, 7]),
    "Ajam5": Jins(pitches=[0, 2, 4, 5, 7], extension_pitches=[-1, -3, 9], modulation_pitches=[0, 7]),
    "UpperAjam": Jins(pitches=[-5, -3, -1, 0], extension_pitches=[-7, 2], modulation_pitches=[-5, 0]),
    "Ajam3": Jins(pitches=[0, 2, 4], extension_pitches=[-1, -3, 5, 7], modulation_pitches=[0, 4]),
    "AjamMurassa": Jins(pitches=[0, 2, 4, 6, 7], extension_pitches=[-1, 9], modulation_pitches=[0, 7]),
    # https://maqamworld.com/en/jins/sikah_baladi.php [315, 364, 391.11, 425, 485, 515]Hz ~ [-375, -124, 0, 144, 372, 476]c
    # NOTE: Sikah ~ [0, 150, 350]c
    # NOTE: SikahBaladi ~ [0, 255, 377, 521, 747, 854]c from root (instead of from tonic)
    "SikahBaladi": Jins(pitches=[-3.77, -1.22, 0, 1.44, 3.7, 4.77], extension_pitches=[], modulation_pitches=[0]),
    "Mustaar": Jins(pitches=[0, 2.5, 3.5], extension_pitches=[-0.5, 4.5, 5.5], modulation_pitches=[0, 3.5]),
    # https://maqamworld.com/en/jins/sazkar.php [241, 260.74, 310, 320, 347.65, 391.11, 440]Hz ~ [-136, 0, 300, 355, 498, 702, 906]c
    "Sazkar": Jins(pitches=[0, 3, 3.5, 5, 7], extension_pitches=[-1.5, 9], modulation_pitches=[0, 7]),
    "Hijazkar": Jins(pitches=[-4, -1, 0, 1, 4, 5], extension_pitches=[], modulation_pitches=[0]),
}

# TODO: some kind of network traverser using networkx, for sayr and maqam
# TODO: Instead of floats, use accidentals, and inject "dialect"?
