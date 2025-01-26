import mido
import copy

def gettabs():
    tabs=[[]]
    with open("out.txt","r") as f:
        for line in f:
            if line.count("-")>20:
                tabs[-1].append(line)
            elif line.count("1")>20:
                tabs[-1].append(line)
                tabs.append([])
    tabs.pop()
    return tabs

tabs=gettabs()
inmidi = mido.MidiFile("out.mid")

for idx, track in enumerate(inmidi.tracks):
    if idx==0:
        continue
    # print(idx)
    # print(len(inmidi.tracks))
    # for msg in track:
    #     print(msg)
    inst=set()
    for msg in track:
        if msg.type=="program_change":
            inst.add(msg.program)
    if len(inst)==0:
        # print("No instrument")
        continue
    if 24<=min(inst) and max(inst)<=31 and len(tabs[idx-1])==7:
        outmidi = copy.deepcopy(inmidi)
        outmidi.tracks=[outmidi.tracks[0],outmidi.tracks[idx]]
        if tabs[idx-1][0][0]!='E' or tabs[idx-1][1][0]!='B' or tabs[idx-1][2][0]!='G' or tabs[idx-1][3][0]!='D' or tabs[idx-1][4][0]!='A' or tabs[idx-1][0][0]!='E':
            outmidi.save(f'track{idx}NS.mid')
            with open(f'track{idx}NS.txt','w') as f:
                f.writelines(tabs[idx-1])
            with open(f'logs.txt','w') as f:
                f.write("NS occurs\n")
        else:
            outmidi.save(f'track{idx}.mid')
            with open(f'track{idx}.txt','w') as f:
                f.writelines(tabs[idx-1])
