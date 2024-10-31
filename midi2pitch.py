import mido

# Mapping of MIDI note numbers to note names
note_names = [
    "C-1", "C#-1", "D-1", "D#-1", "E-1", "F-1", "F#-1", "G-1", "G#-1", "A-1", "A#-1", "B-1",
    "C0", "C#0", "D0", "D#0", "E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0",
    "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
    "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
    "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
    "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
    "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
    "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6",
    "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7",
    "C8"
]

def midi_to_pitches(midi_file_path):
    mid = mido.MidiFile(midi_file_path)
    pitches = []
    
    # Dictionary to track active notes
    active_notes = {}
    
    for track in mid.tracks:
        track_pitches = []
        time = 0
        
        for msg in track:
            time += msg.time  # Update the time with delta time
            
            if msg.type == 'note_on' and msg.velocity > 0:
                # Start a note
                active_notes[msg.note] = time
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # End a note
                if msg.note in active_notes:
                    # Collect the note name at the end of its duration
                    note_name = note_names[msg.note]
                    if time == active_notes[msg.note]:  # Ensure timing matches
                        track_pitches.append(note_name)
                    del active_notes[msg.note]  # Remove it from active notes

            # If we reach a point in time with active notes, collect them
            if active_notes:
                simultaneous_notes = [note_names[note] for note in active_notes.keys()]
                track_pitches.append("".join(simultaneous_notes))

        if track_pitches:
            # Remove duplicates while keeping the order
            seen = set()
            unique_pitches = []
            for note in track_pitches:
                if note not in seen:
                    seen.add(note)
                    unique_pitches.append(note)
            pitches.append(unique_pitches)

    return pitches

def format_pitches(pitches):
    output = ""
    for track in pitches:
        output += "\n".join(track) + "\n---\n"
    return output.strip()

# Usage
midi_file_path = "basic_pitch_transcription.mid"
pitches = midi_to_pitches(midi_file_path)
formatted_output = format_pitches(pitches)
print(formatted_output)

