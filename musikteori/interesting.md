```python
    # open string + required semitone span
    {
        0: {},
        1: {},
        # halftone fingers
        2: {"indu3": [0, 1, 2]},
        # halftone fingers
        3: {"kurd3": [0, 1, 3], "nahawand3": [0, 2, 3]},
        # halftone fingers
        4: {"hijaz3": [0, 1, 4], "ajam3": [0, 2, 4], "hijazkar3": [0, 3, 4]},
        # halftone fingers + 1 reaching
        5: {"sus b2 4": [0, 1, 5], "sus2 4": [0, 2, 5], "vietnamese": [0, 3, 5], "tense3": [0, 4, 5]},
        # half/wholetone fingers
        6: {"vienesse": [0, 1, 6], "sus2 b5": [0, 2, 6], "dim": [0, 3, 6], "b5": [0, 4, 6], "tense4": [0, 5, 6]},
        # half/wholetone fingers
        7: {
            "sus b2": [0, 1, 7],
            "sus2": [0, 2, 7],
            "min": [0, 3, 7],
            "maj": [0, 4, 7],
            "sus4": [0, 5, 7],
            "ongkari": [0, 6, 7],
        },
        # half/wholetone fingers
        8: {
            "aug": [0, 4, 8],
            "sarvasri aug5": [0, 5, 8],
            "CAHian": [0, 6, 8],
            "tense5": [0, 7, 8],
            "ute aug5": [0, 3, 8],
            "sus2 aug5": [0, 2, 8],
            "sus b2 aug5": [0, 1, 8],
            "sus2 aug5 ": [0, 2, 8],
        },
        # half/wholetone fingers + 1 reaching
        9: {
            "bugle": [0, 5, 9],
            "ILLian": [0, 6, 9],
            "maj6 no3": [0, 7, 9],
            "tenseb6": [0, 8, 9],
            "bilwadala": [0, 4, 9],
            "ute 6": [0, 3, 9],
            "sus2 6": [0, 2, 9],
            "sus b2 6": [0, 1, 9],
        },
        # half/wholetone/third fingers
        10: {
            "GOCian": [0, 6, 10],
            "dom7 no3": [0, 7, 10],
            "aug(5) (b)7 no3": [0, 8, 10],
            "tense 6": [0, 9, 10],
            "sansagari": [0, 5, 10],
            "italian aug6": [0, 4, 10],
            "ute (b)7": [0, 3, 10],
            "sus b2 (b)7": [0, 1, 10],
            "sus2 (b)7": [0, 2, 10],
        },
        # half/wholetone/third fingers
        11: {
            "[maj]7 no3": [0, 7, 11],
            "aug(5) [maj]7 no3": [0, 8, 11],
            "PODian": [0, 9, 11],
            "tense (b)7": [0, 10, 11],
            "enigma3": [0, 6, 11],
            "MODian": [0, 5, 11],
            "MOTian": [0, 4, 11],
            "sus b2 [maj]7": [0, 1, 11],
            "sus2 [maj]7": [0, 2, 11],
            "ute [maj]7": [0, 3, 11],
        },
    }

    {
        0: {},
        # shifted halftone fingers
        1: {
            "indu3": [0, 1, 2],
            "nahawand3": [0, 2, 3],
            "hijazkar3": [0, 3, 4],
            "tense3": [0, 4, 5],
            "tense4": [0, 5, 6],
            "ongkari": [0, 6, 7],
            "tense5": [0, 7, 8],
            "tenseb6": [0, 8, 9],
            "tense 6": [0, 9, 10],
            "tense (b)7": [0, 10, 11],
        },
        # shifted halftone fingers
        2: {
            "kurd3": [0, 1, 3],
            "ajam3": [0, 2, 4],
            "vietnamese": [0, 3, 5],
            "b5": [0, 4, 6],
            "sus4": [0, 5, 7],
            "CAHian": [0, 6, 8],
            "maj6 no3": [0, 7, 9],
            "aug(5) (b)7 no3": [0, 8, 10],
            "PODian": [0, 9, 11],
        },
        # shifted halftone fingers
        3: {
            "hijaz3": [0, 1, 4],
            "sus2 4": [0, 2, 5],
            "dim": [0, 3, 6],
            "maj": [0, 4, 7],
            "sarvasri aug5": [0, 5, 8],
            "ILLian": [0, 6, 9],
            "dom7 no3": [0, 7, 10],
            "aug(5) [maj]7 no3": [0, 8, 11],
        },
        # shifted halftone fingers
        4: {
            "sus b2 4": [0, 1, 5],
            "sus2 b5": [0, 2, 6],
            "min": [0, 3, 7],
            "aug": [0, 4, 8],
            "bugle": [0, 5, 9],
            "GOCian": [0, 6, 10],
            "[maj]7 no3": [0, 7, 11],
        },
        # shifted half/wholetone fingers
        5: {
            "vienesse": [0, 1, 6],
            "sus2": [0, 2, 7],
            "ute aug5": [0, 3, 8],
            "bilwadala": [0, 4, 9],
            "sansagari": [0, 5, 10],
            "enigma3": [0, 6, 11],
        },
        # shifted half/wholetone fingers
        6: {
            "sus b2": [0, 1, 7],
            "sus2 aug5": [0, 2, 8],
            "ute 6": [0, 3, 9],
            "italian aug6": [0, 4, 10],
            "MODian": [0, 5, 11],
            "sus2 aug5 ": [0, 2, 8],
        },
        # shifted half/wholetone fingers
        7: {"sus b2 aug5": [0, 1, 8], "sus2 6": [0, 2, 9], "ute (b)7": [0, 3, 10], "MOTian": [0, 4, 11]},
        # shifted half/wholetone fingers
        8: {"sus b2 6": [0, 1, 9], "sus2 (b)7": [0, 2, 10], "ute [maj]7": [0, 3, 11]},
        # shifted half/wholetone/third fingers
        9: {"sus b2 (b)7": [0, 1, 10], "sus2 [maj]7": [0, 2, 11]},
        # shifted half/wholetone/third fingers
        10: {"sus b2 [maj]7": [0, 1, 11]},
        11: {},
    }

    {
        0: {},
        1: {},
        2: {},
        # shifted halftone fingers
        3: {"BIRian": [0, 4, 6, 7]},
        # shifted halftone fingers
        4: {"koptic": [0, 4, 6, 8], "epogic": [0, 4, 7, 8], "dim add5": [0, 3, 6, 7]},
        # shifted half/wholetone fingers
        5: {
            "mynic": [0, 3, 6, 8],
            "saric": [0, 4, 6, 9],
            "lothic": [0, 3, 7, 8],
            "maj6": [0, 4, 7, 9],
            "aeoloric": [0, 4, 8, 9],
        },
        # shifted half/wholetone fingers
        6: {
            "dim7": [0, 3, 6, 9],
            "dom7b5": [0, 4, 6, 10],
            "min 6": [0, 3, 7, 9],
            "dom7": [0, 4, 7, 10],
            "aug(5) (b)7": [0, 4, 8, 10],
        },
        # shifted half/wholetone fingers + reaching
        7: {
            "half dim7": [0, 3, 6, 10],
            "min (b)7": [0, 3, 7, 10],
            "(maj) [maj]7": [0, 4, 7, 11],
            "aug(5) [maj]7": [0, 4, 8, 11],
        },
        # shifted half/wholetone/third fingers
        8: {"dim [maj]7": [0, 3, 6, 11], "min [maj]7": [0, 3, 7, 11]},
    }
```
