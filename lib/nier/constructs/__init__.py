"""
Structs that represent parts of NieR Replicant ver.1.22474487139... save files.

Credit for decoding most of the struct fields goes to https://github.com/Acurisu
Most constants and original structs were translated to Python from
https://github.com/Acurisu/NieR-Replicant-ver.1.22474487139/blob/main/Editor/src/Nier.ts

Newly decoded fields in this package include time (for a given save + for each garden plot) and garden plots,
equipped words, fishing records, item new/viewed states, and more.

:author: Doug Skrypa
"""

from .game_data import Savefile, Gamedata, Plot, Header
