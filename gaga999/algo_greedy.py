
# same fret with one finger (index or middle most) (*barre)

# arrange finger for a set of fingering
# hand distance and angle (mabey not)

# [0, 36.35, 34.31, 32.39, 30.57, 28.85, 27.23, 25.71, 24.26, 22.9, 21.62, 20.4, 19.26, 18.18, 17.16, 16.19, 15.28, 14.43, 13.62, 12.85, 12.13, 11.45, 10.81, 10.2, 9.63]
# [0, 36.35, 70.66, 103.05, 133.62, 162.47, 189.71, 215.41, 239.67, 262.58, 284.19, 304.59, 323.85, 342.03, 359.18, 375.38, 390.66, 405.09, 418.7, 431.56, 443.69, 455.14, 465.95, 476.15, 485.78]
# fret length
# thres or continuous function

FLENGTH=[0, 36.35, 70.66, 103.05, 133.62, 162.47, 189.71, 215.41, 239.67, 262.58, 284.19, 304.59, 323.85, 342.03, 359.18, 375.38, 390.66, 405.09, 418.7, 431.56, 443.69, 455.14, 465.95, 476.15, 485.78]
FWIDTH=7.4
BASENOTE=[64,59,55,50,45,40]
MAXLENTH=24
note2tab = dict()
occur=[]
statfing=dict()
trans=[]

def init():
    for note in range(BASENOTE[-1],BASENOTE[0]+MAXLENTH+1):
        l = []
        for i in range(0,6):
            if BASENOTE[i]<=note and note <= BASENOTE[i]+MAXLENTH:
                l.append((i,note-BASENOTE[i]))
        note2tab[note]=l
    with open(os.path.dirname(os.path.abspath(__file__))+"/stat.txt", "r") as f:
        n = int(f.readline())
        global occur
        occur = list(map(int, f.readline().split(' ')[0:n]))
        assert(len(occur)==n)
        f.readline()   # strings
        for i in range(0,n):
            statfing[tuple(map(int, f.readline().split(' ')[0:6]))]=i
        for i in range(0,n):
            tmp=f.readline().split(' ')
            tmp=list(map(int,tmp[0:int(tmp[0])+1]))
            trans.append(dict())
            for j in range(1,tmp[0]+1):
                if tmp[j] in trans[i]:
                    trans[i][tmp[j]]+=1
                else:
                    trans[i][tmp[j]]=1
    return

def outputtrack(tab_array):
    tab_char = ['E','B','G','D','A','E']
    lookup = [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1];
    length = len(tab_array[0])+len(tab_array[0])//16+2;
    if (length-2)%17!=0:
        for _ in range(0,17-(length-2)%17):
            for t in range(0,6):
                tab_array[t].append(-1);
        length+=17-(length-2)%17;
    numbering = [1 for s in range(0,length)];
    numbering[0]=2;
    cur = -1;
    for i in range(2,len(numbering)):
        if i%17==1:
            continue;
        cur+=1;
        for t in range(0,6):
            numbering[i] = max(lookup[tab_array[t][cur]],numbering[i]);
            #print(tab_array[t][cur],lookup[tab_array[t][cur]],'f');
    for t in range(0,6):
        cur = -1;
        for (i,n) in enumerate(numbering):
            if i==0:
                print(f"{tab_char[t]} ",end='');
                continue;
            if(i%17==1):
                print("|",end='');
            else:
                cur+=1;
                c = '-';
                if tab_array[t][cur]!=-1:
                    c = tab_array[t][cur];
                print(f"{c:-<{numbering[i]}}",end='');
        print('\n',end='');
    for n in numbering:
        print(f"{n: <{n}}",end='');
    print('\n',end='');

def note_std(note):
    while note > BASENOTE[0]+MAXLENTH:
        assert(0)
        note-=12;
    while note < BASENOTE[-1]:
        assert(0)
        note+=12
    return note;

def assfing(fing):      # -1:no sound / 0 no fing /  1 index ... finger / 5 thumb
    # thumb
    valid_fingers = [f for f in fing if f > 0]
    if not valid_fingers:
        return fing
    max_finger = max(valid_fingers)
    min_finger = min(valid_fingers)
    first_min_index = fing.index(min_finger)
    last_min_index = len(fing) - 1 - fing[::-1].index(min_finger)
    return (7,7,7,7,7,7)    #error return 7

def fingraw(fing):
    valid_fingers = [f for f in fing if f > 0]
    if not valid_fingers:
        return 1e7
    max_finger = max(valid_fingers)
    min_finger = min(valid_fingers)
    score=round(1000*valid_fingers.count(0) / len(valid_fingers)) #open
    if FLENGTH[max_finger]-FLENGTH[min_finger]>FLENGTH[7]-FLENGTH[2]:
        return -1e18
    elif FLENGTH[max_finger]-FLENGTH[min_finger]>=FLENGTH[6]-FLENGTH[2]:
        return score
    return 500+score

def fing2score(fing):
    score = fingraw(fing)
    if fing in statfing:  # past data
        return 1e9+fingraw(fing)+occur[statfing[fing]]
    return fingraw(fing)

def notse2fing(notes,fing):
    if len(notes)==0:
        assert(len(fing)==6)
        # if fingraw(fing)<-1e16:
        #     return []
        return [fing]
    res=[]
    for tr,pos in note2tab[notes[-1]]:
        if fing[tr]!=-1:
            continue;
        res.extend(notse2fing(notes[0:-1],fing[0:tr]+(pos,)+fing[tr+1:len(fing)]))
    return res

def solve(file):
    midi=mido.MidiFile(file)
    tpb = midi.ticks_per_beat
    time_sig = (4,4);
    tpbar = 0;
    tpt = 0;
    notes_seq = [];
    times = [];
    eot = 0;
    cur_time = 0;
    tpbar = tpb*time_sig[0];
    tpt=tpbar//16;
    for i, track in enumerate(midi.tracks):
        cur_time = 0
        for msg in track:
            if msg.type=='time_signature':
                time_sig = (msg.numerator,msg.denominator)
                tpbar = tpb*time_sig[0];
                tpt=tpbar//16;
            if msg.type == "end_of_track":
                eot = msg.time;
            if hasattr(msg,'time'):
                cur_time+=msg.time;
            if msg.type == 'note_on':
                # print(msg,file=sys.stderr)
                crt=round(cur_time / tpt)
                if len(times)!=0 and times[-1]==crt:
                    notes_seq[-1].append(note_std(msg.note))
                else :
                    notes_seq.append([note_std(msg.note)])
                    times.append(crt)
    fings=[notse2fing(notes,(-1,-1,-1,-1,-1,-1)) for notes in notes_seq]
    tab = [[-1 for col in range(0,round(cur_time / tpt)+1)] for row in range(0,6)];
    # for t in range(len(fings)):
    #     assert(len(fings[t])>0)
    dp=[[-1 for i in range(len(fings[t]))] for t in range(len(fings))] # max score sum or punishment 
    fr=[[-1 for i in range(len(fings[t]))] for t in range(len(fings))]
    for t in range(0,len(times)):
        mxsc=-2e18
        pos=-1
        for i in range(len(fings[t])):
            crsc=fing2score(fings[t][i])
            if crsc>mxsc:
                mxsc=crsc
                pos=i
        # if mxsc<1e9:
        #     for fi in fings[t]:
        #         print(fi,sys.stderr)
        #     assert(0)
        if pos!=-1:
            for i in range(0,6):
                tab[i][times[t]]=fings[t][pos][i]
    return tab

import sys
import os
import mido

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("usage:python algo.py [input file]")
        exit(1)
    init()
    outputtrack(solve(sys.argv[1]))
        


