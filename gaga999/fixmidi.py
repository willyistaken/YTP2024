import mido
import copy


# shortest to sixteenth note

# midpath="basic_bluebird.mid"
midpath="basic_haruhikage.mid"
outpath="out.mid"
# midpath="HeyJudetrack6.mid"
# midpath="basic_Onthefrontline.mid"

LNOTE=40
HNOTE=79

inmidi = mido.MidiFile(midpath)

# log=open("log.txt","a")
# if not any(msg.type=="time_signature" for msg in inmidi.tracks[0]):
#     inmidi.tracks[0].append(mido.MetaMessage('time_signature', numerator=4, denominator=4, notated_32nd_notes_per_beat=8, time=0))

# if any(msg.type=="note_on" and msg.note<35 for msg in inmidi.tracks[1]):
#     log.write(f"{midpath}: error: note below B(35)\n")

# if any(msg.type=="note_on" and msg.note<40 for msg in inmidi.tracks[1]):
#     log.write(f"{midpath}: warning: note below E(40)\n")

# if any(msg.type=="note_on" and msg.note>88 for msg in inmidi.tracks[1]):
#     log.write(f"{midpath}: error: note above E(88)\n")

# if any(msg.type=="note_on" and msg.note>79 for msg in inmidi.tracks[1]):
#     log.write(f"{midpath}: warning: note above G(79)\n")

print(len(inmidi.tracks))
print(inmidi.ticks_per_beat)

def delmsg(i):
    if i<len(inmidi.tracks[1])-1:
        inmidi.tracks[1][i+1].time+=inmidi.tracks[1][i].time
    del inmidi.tracks[1][i]

for i in reversed(range(len(inmidi.tracks[1]))):
    msg = inmidi.tracks[1][i]
    if (msg.type=="note_on" or msg.type=="note_off") and (msg.note<LNOTE or msg.note>HNOTE):
        delmsg(i)

for i in reversed(range(len(inmidi.tracks[1]))):
    msg = inmidi.tracks[1][i]
    if msg.type=="note_on" and msg.velocity<45:
        for j in range(i,len(inmidi.tracks[1])):
            ms2=inmidi.tracks[1][j]
            if ms2.type!="note_off" or ms2.note!=msg.note:
                continue
            delmsg(j)
            break
        delmsg(i)

# check msg other than note_on/off 
# move start without relatively, move end according to note length, with absolute time
# base tick check remainder by %BT</2

print("-------------------")

cnt=0
for msg in inmidi.tracks[1]:
    if (msg.type=="note_on" or msg.type=="note_off") and msg.velocity<50 and msg.velocity!=0:
        cnt+=1

inmidi.save(outpath)
print(cnt)
# log.close()

    
