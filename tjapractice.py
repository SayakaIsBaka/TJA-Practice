#! /usr/bin/env python3

import sys
import os

from pydub import AudioSegment
from pydub.playback import play

def read_header(lines):
    bpm = None
    offset = None
    audio_name = None
    i = None
    header = []
    for i in range(len(lines)):
        if lines[i][:4] == "BPM:":
            bpm = float(lines[i][4:])
        elif lines[i][:7] == "OFFSET:":
            offset = float(lines[i][7:])
        elif lines[i][:5] == "WAVE:":
            audio_name = lines[i][5:].strip()
        elif lines[i][:6] == "TITLE:":
            header.append(lines[i][:6] + "practice_" + lines[i][6:].strip() + "\n")
        elif lines[i].strip() == "#START":
            break
        elif lines[i][:10] == "DEMOSTART:":
            continue
        else:
            header.append(lines[i])
    return (i, bpm, offset, header, audio_name)

def get_delimited_lines(lines, pos, offset, bpm, start, end):
    delimited_lines = []
    cur_time = offset * -1 * 1000
    measure = 4
    start_audio = None
    start_bpm = None
    start_measure = None
    while lines[pos].strip() != "#END" and cur_time < end:
        if cur_time > start:
            if start_audio == None:
                start_audio = cur_time
                start_bpm = bpm
                start_measure = measure
            delimited_lines.append(lines[pos])

        if lines[pos][:9] == "#MEASURE ":
            timing_sig = lines[pos][9:].strip().split('/')
            measure = float(timing_sig[0]) / (float(timing_sig[1]) / 4)
        elif lines[pos][:11] == "#BPMCHANGE ":
            bpm = float(lines[pos][11:])
        elif lines[pos][:7] == "#DELAY ":
            cur_time = cur_time + float(lines[pos][7:]) * 1000
        elif lines[pos].strip() != "" and lines[pos].strip()[-1] == ',':
            cur_time = cur_time + (60 / bpm) * measure * 1000
        pos += 1
    return (delimited_lines, start_audio, cur_time, start_bpm, start_measure)

def export_audio(start, end, audio, filename, fadeout = 0):
    cut_audio = audio[start:][:(end - start + fadeout)]
    if fadeout > 0:
        cut_audio = cut_audio.fade_out(fadeout)
    cut_audio.export(filename, format="ogg")

def write_tja(header, bpm, audio_name, filename, lines, measure):
    out_file = open(filename, "w")
    out_file.writelines(header)
    out_file.write("WAVE:" + audio_name + "\n")
    out_file.write("BPM:" + str(bpm) + "\n")
    out_file.write("OFFSET:0\n\n")

    if lines[0].strip() != "#START":
        out_file.write("#START\n")
    out_file.write("#MEASURE " + str(measure) + "/4\n")
    out_file.writelines(lines)
    out_file.write("#END\n")


def main(filename):
    file = open(filename, "r")
    lines = file.readlines()

    (pos, bpm, offset, header, audio_name) = read_header(lines)
    if (bpm == None or offset == None or audio_name == None):
        print("Error: BPM, offset or audio file not found", file=sys.stderr)
        exit(1)

    (delimited_lines, start, end, start_bpm, start_measure) = get_delimited_lines(lines, pos, offset, bpm, float(sys.argv[2]), float(sys.argv[3]))

    tja_dir = os.path.dirname(os.path.realpath(file.name))
    
    audio = AudioSegment.from_file(os.path.join(tja_dir, audio_name))
    cut_audio_name = "practice_" + os.path.splitext(audio_name)[0] + ".ogg"
    if len(sys.argv) > 4:
        export_audio(start, end, audio, os.path.join(tja_dir, cut_audio_name), int(sys.argv[4]))
    else:
        export_audio(start, end, audio, os.path.join(tja_dir, cut_audio_name))
    
    write_tja(header, start_bpm, cut_audio_name, os.path.join(tja_dir, "practice_" + os.path.basename(file.name)), delimited_lines, start_measure)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: tjapractice.py [tja file] [start time] [end time] [fade-out (optional)] (in ms)", file=sys.stderr)
    else:
        main(sys.argv[1])