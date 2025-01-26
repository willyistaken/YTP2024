import mido
import copy

# 讀取多軌 MIDI 檔案
multi_track_midi = mido.MidiFile("out.mid")
print(multi_track_midi.type)

cnt=0
for track in multi_track_midi.tracks:
    print(f'track{cnt}:-------------------')
    cnt+=1
    if cnt==1:
        continue
    for msg in track:
        print(msg)
