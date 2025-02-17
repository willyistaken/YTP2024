import mido
from mido import MidiFile

note2tab = { 64: [(1, 0), (2, 5), (3, 9), (4, 14), (5, 19)], 
            65: [(1, 1), (2, 6), (3, 10), (4, 15), (5, 20)], 
            66: [(1, 2), (2, 7), (3, 11), (4, 16), (5, 21)], 
            67: [(1, 3), (2, 8), (3, 12), (4, 17), (5, 22)], 
            68: [(1, 4), ( 2, 9), (3, 13), (4, 18), (5, 23)], 
            69: [(1, 5), (2, 10), (3, 14), (4, 19)], 
            70: [(1, 6), (2, 11), (3, 15), (4, 20)], 
            71: [(1, 7), (2, 12), ( 3, 16), (4, 21)], 
            72: [(1, 8), (2, 13), (3, 17), (4, 22)], 
            73: [(1, 9) , (2, 14), (3, 18), (4, 23)], 
            74: [(1, 10), (2, 15), (3, 19)], 
            75: [(1 , 11), (2, 16), (3, 20)], 
            76: [(1, 12), (2, 17), (3, 21)], 
            77: [(1, 13), (2, 18), (3, 22)], 
            78: [(1, 14), (2, 19), (3, 23)], 
            79: [(1, 15), ( 2, 20)], 
            80: [(1, 16), (2, 21)], 
            81: [(1, 17), (2, 22)], 
            82: [(1, 18), (2, 23)], 
            83: [(1, 19)], 
            84: [(1, 20)], 
            85: [(1, 21)], 
            86: [(1, 22)], 
            87: [(1, 23)], 
            59: [(2, 0), (3, 4), (4, 9), (5, 14), (6, 19)], 
            60: [( 2, 1), (3, 5), (4, 10), (5, 15), (6, 20)], 
            61: [(2, 2), (3, 6), (4, 11), (5, 16), (6, 21)], 
            62: [(2, 3), (3, 7), (4, 12), (5, 17), (6, 22)], 
            63: [(2, 4), (3, 8), (4, 13), (5, 18), (6, 23)], 
            55: [(3, 0), (4, 5), (5, 10), (6, 15)], 
            56: [(3, 1), (4, 6), (5, 11), (6, 16)], 
            57: [(3, 2), (4, 7), (5, 12), (6, 17)], 
            58: [(3, 3), (4, 8), (5, 13), (6, 18)], 
            50: [(4, 0), (5, 5), (6, 10)], 
            51: [(4, 1), (5, 6), (6, 11)], 
            52: [(4, 2), (5, 7), (6, 12)], 
            53: [(4, 3), (5, 8), (6, 13)], 
            54: [(4, 4), (5, 9), (6, 14)], 
            45: [(5, 0), (6, 5)], 
            46: [(5, 1), (6, 6)], 
            47: [(5, 2) , (6, 7)], 
            48: [(5, 3), (6, 8)], 
            49: [(5, 4), (6, 9)], 
            40: [(6, 0)], 
            41: [(6, 1)], 
            42: [(6, 2)], 
            43: [(6, 3)], 
            44: [(6, 4)] 
};

tab_char = ['E','B','G','D','A','E']

def note_std(note):
    while note > 87 or note < 40:
        if note > 87:
            note-=12;
        if note < 40:
            note+=12;
    return note;

def list_note_on_events(midi_file):
    midi = MidiFile(midi_file)
    ppq = midi.ticks_per_beat
    time_sig = (4,4);
    bpb = 0;
    tpb = 0;
    tptt = 0;
    notes = [];
    eot = 0;
    cur_time = 0;
    for i, track in enumerate(midi.tracks):
    #    print(f"Track {i}: {track.name}")
        cur_time = 0
    #    print(track);
        for msg in track:
            if msg.type=='time_signature':
                time_sig = (msg.numerator,msg.denominator)
                bpb=time_sig[0];
                tpb = ppq*bpb;
                tptt=tpb/16;
            if msg.type == "end_of_track":
                eot = msg.time;
            if hasattr(msg,'time'):
                cur_time+=msg.time;
            if msg.type == 'note_on':
                notes.append((note_std(msg.note),int(cur_time // tptt)));
    tab = [[-1 for col in range(0,int(cur_time // tptt))] for row in range(0,6)];
    for note in notes:
        f = 0;
        for (track,fret) in note2tab[note[0]]:
            track-=1;
            if tab[track][note[1]]==-1:
                tab[track][note[1]]=fret;
                f=1;
                break;
    return tab;

def outputtrack(tab_array):
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
    
import sys
if __name__ == "__main__":
    midi_filename = sys.argv[1]  # Change this to your MIDI file path
    outputtrack(list_note_on_events(midi_filename));

    '''
    note2tab={};
    s = [64,59,55,50,45,40];
    for j in range(0,6):
        for i in range(0,24):
            if s[j]+i not in note2tab:
                note2tab[s[j]+i] = [];
            note2tab[s[j]+i].append((j+1,i));
    '''

    #print(note2tab)
