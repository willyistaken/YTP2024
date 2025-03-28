# Topic:
(mp3)->(midi)->(sheet music)+(finger style sheet)->(video)

## mp3 to midi

https://github.com/LIMUNIMI/MMSP2021-Audio2ScoreAlignment
https://github.com/DamRsn/NeuralNote
https://colab.research.google.com/github/magenta/mt3/blob/main/mt3/colab/music_transcription_with_transformers.ipynb
https://basicpitch.spotify.com/

## midi to sheet
https://github.com/BYVoid/MidiToSheetMusic

## midi to finger style
https://github.com/noahbaculi/guitar-tab-generator/?tab=readme-ov-file
https://noahbaculi.com/guitartab
https://github.com/natecdr/tuttut/


## video(highly optional) 
no current tool

## playback tab:
http://www.tofret.com/tablature-player.php

## Training Resource (Easy)
- Dataset: [Github](https://github.com/marl/GuitarSet/tree/master?tab=readme-ov-file)
- current: [tbt-it](https://tabs.tabit.net/)

## Related work
- Paper: [GTT](https://arxiv.org/pdf/2309.09085)
- CNN: [Not sure what's its aims](https://github.com/andywiggins/tab-cnn/tree/master)

## current use

- [data](https://tabs.tabit.net/list.php?f=3671&p=2)
- [tab parser](https://github.com/bostick/tbt-parser)

## Knowledge

- [midi instruments](https://fmslogo.sourceforge.io/manual/midi-instrument.html)
- [guitar note](https://metacpan.org/pod/MIDI::Chord::Guitar)
- normal guitar at most 24 fret (40 ~ 88)
- [mido message](https://mido.readthedocs.io/en/stable/messages/index.html)
- fret length
- [0, 36.35, 70.66, 103.05, 133.62, 162.47, 189.71, 215.41, 239.67, 262.58, 284.19, 304.59, 323.85, 342.03, 359.18, 375.38, 390.66, 405.09, 418.7, 431.56, 443.69, 455.14, 465.95, 476.15, 485.78]

## problem
- tempo incorrect
- wrong starting point

## Next to do
- find tools auto gen info from midi, like start point, time signature

