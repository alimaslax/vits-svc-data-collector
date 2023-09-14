from scipy.io import wavfile
import os
import numpy as np
import argparse
from tqdm import tqdm
import json
import os

from datetime import datetime, timedelta

# Utility functions

def GetTime(video_seconds):

    if (video_seconds < 0) :
        return 00

    else:
        sec = timedelta(seconds=float(video_seconds))
        d = datetime(1,1,1) + sec

        instant = str(d.hour).zfill(2) + ':' + str(d.minute).zfill(2) + ':' + str(d.second).zfill(2) + str('.001')
    
        return instant

def GetTotalTime(video_seconds):

    sec = timedelta(seconds=float(video_seconds))
    d = datetime(1,1,1) + sec
    delta = str(d.hour) + ':' + str(d.minute) + ":" + str(d.second)
    
    return delta

def windows(signal, window_size, step_size):
    if type(window_size) is not int:
        raise AttributeError("Window size must be an integer.")
    if type(step_size) is not int:
        raise AttributeError("Step size must be an integer.")
    for i_start in range(0, len(signal), step_size):
        i_end = i_start + window_size
        if i_end >= len(signal):
            break
        yield signal[i_start:i_end]

def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))

def rising_edges(binary_signal):
    previous_value = 0
    index = 0
    for x in binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1

'''
Last Acceptable Values

min_silence_length = 0.3
silence_threshold = 1e-3
step_duration = 0.03/10

'''

# Change the arguments and the input file here
input_dir = '/Users/maslaxali/Music/meekv2/vocals/dreamsandnightmare/'  # Directory containing the input files
output_dir = '/Users/maslaxali/Music/meekv2/samples/'
min_silence_length = 0.1  # The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.
silence_threshold = 5e-3  # The energy level (between 0.0 and 1.0) below which the signal is regarded as silent.
step_duration = 0.01/10   # The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).
min_clip_length = 5.0  # The minimum length of the clip to be written [seconds].
seg_combine = 6 # number of segments to combine

# List all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file has a .wav extension
    if filename.endswith('.wav'):
        # Construct the full file path
        input_file = os.path.join(input_dir, filename)

    input_filename = input_file
    window_duration = min_silence_length
    if step_duration is None:
        step_duration = window_duration / 10.
    else:
        step_duration = step_duration

    output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
    dry_run = False

    print("Splitting {} where energy is below {}% for longer than {}s.".format(
        input_filename,
        silence_threshold * 100.,
        window_duration
        )
    )

    # Read and split the file

    sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)

    max_amplitude = np.iinfo(samples.dtype).max
    print(max_amplitude)

    max_energy = energy([max_amplitude])
    print(max_energy)

    window_size = int(window_duration * sample_rate)
    step_size = int(step_duration * sample_rate)

    signal_windows = windows(
        signal=samples,
        window_size=window_size,
        step_size=step_size
    )

    window_energy = (energy(w) / max_energy for w in tqdm(
        signal_windows,
        total=int(len(samples) / float(step_size))
    ))

    window_silence = (e > silence_threshold for e in window_energy)

    cut_times = (r * step_duration for r in rising_edges(window_silence))

    # This is the step that takes long, since we force the generators to run.
    print("Finding silences...")
    cut_samples = [int(t * sample_rate) for t in cut_times]
    cut_samples.append(-1)

    cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in range(len(cut_samples) - 1)]

    new_ranges = []

    i = 0
    count = 0
    while i < len(cut_ranges):
        start = cut_ranges[i][1]
        stop = cut_ranges[i][2]

        if i == 0:
            new_ranges.append((count, cut_samples[i], cut_samples[i+1]))

        if i + seg_combine < len(cut_ranges):
            new_ranges.append((count, new_ranges[-1][2], cut_ranges[i+seg_combine][2]))
            i += seg_combine
        else:
            break
        count = count + 1

    print(new_ranges)


    video_sub = {str(i) : [str(GetTime(((cut_samples[i])/sample_rate))), 
                        str(GetTime(((cut_samples[i+1])/sample_rate)))] 
                for i in range(len(cut_samples) - 1)}

    for i, start, stop in tqdm(new_ranges):
        # Remember to change the output file path as well
        output_file_path = os.path.join(output_dir, "{}_{:03d}.wav".format(
            os.path.splitext(os.path.basename(input_filename))[0],
            i
        ))
        clip_length = (stop - start) / sample_rate  # Length of the clip in seconds
        if clip_length >= min_clip_length:  # Check if the clip is long enough
            if not dry_run:
                print("Writing file {}".format(output_file_path))
                wavfile.write(
                    filename=output_file_path,
                    rate=sample_rate,
                    data=samples[start:stop]
                )
            else:
                print("Not writing file {}".format(output_file_path))
        else:
            print("Skipping file {} due to insufficient length".format(output_file_path))
            
    with open (output_dir+'\\'+output_filename_prefix+'.json', 'w') as output:
        json.dump(video_sub, output)
