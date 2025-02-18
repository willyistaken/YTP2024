import mido
import copy

def gettabs():
    tabs=[[]]
    with open("out.txt","r",errors='ignore') as f:
        for line in f:
            if line.count("-")>20 or line.count("]")+line.count("|")>5:
                tabs[-1].append(line)
            elif sum(c.isdigit() for c in line)>20 and len(tabs[-1])>0:
                tabs[-1].append(line)
                tabs.append([])
    tabs.pop()
    return tabs

basetab=["E","B","G","D","A","E"]

def NStandard(qtab):
    for i in range(0,6):
        if len(qtab[i])<3 or qtab[i][0]!=basetab[i] or (qtab[i][1]!=" " and qtab[i][1]!="|"):
            return 1
    return 0

tabs=gettabs()
inmidi = mido.MidiFile("out.mid")

if len(tabs)!=len(inmidi.tracks)-1:
    with open(f'logs.txt','a') as f:
        f.write(f"track error occurs tabs: {len(tabs)} tracks: {len(inmidi.tracks)-1}\n")
    print(f"track error occurs tabs: {len(tabs)} tracks: {len(inmidi.tracks)-1}")
    exit(0)

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
        if NStandard(tabs[idx-1]):
            outmidi.save(f'track{idx}NS.mid')
            with open(f'track{idx}NS.txt','w') as f:
                f.writelines(tabs[idx-1])
            # with open(f'logs.txt','a') as f:
            #     f.write("NS occurs\n")
        else:
            outmidi.save(f'track{idx}.mid')
            with open(f'track{idx}.txt','w') as f:
                f.writelines(tabs[idx-1])
