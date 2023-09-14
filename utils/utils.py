import os
import ffmpeg

def get_audio_length(filename):
    try:
        probe = ffmpeg.probe(filename)
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        if audio_stream:
            return float(audio_stream['duration'])
        else:
            return 0.0
    except ffmpeg.Error as e:
        print(f"Error occurred while probing '{filename}': {e.stderr}")
        return 0.0

def count_wav_lengths(directory):
    total_length = 0.0
    for filename in os.listdir(directory):
        if filename.lower().endswith('.wav'):
            file_path = os.path.join(directory, filename)
            length = get_audio_length(file_path)
            total_length += length
            print(f"Length of '{filename}': {length} seconds")
    print(f"Total length of WAV files: {total_length} seconds")


# Usage example
# directory_path = './samples/meekv2'
# count_wav_lengths(directory_path)

import os
import wave

def get_sample_rate(filename):
    try:
        with wave.open(filename, 'rb') as wav_file:
            return wav_file.getframerate()
    except wave.Error as e:
        print(f"Error occurred while reading '{filename}': {str(e)}")
        return None

def get_wav_sample_rates(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.wav'):
            file_path = os.path.join(directory, filename)
            sample_rate = get_sample_rate(file_path)
            if sample_rate is not None:
                print(f"Sample rate of '{filename}': {sample_rate} Hz")


def get_average_decibels(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    try:
        # Read the audio file using soundfilecle
        data, sample_rate = sf.read(file_path)
        
        # Convert audio data to mono if it has multiple channels
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
        
        # Calculate the average decibels using RMS (Root Mean Square)
        rms = np.sqrt(np.mean(data ** 2))
        average_db = 20 * np.log10(rms)
        
        return average_db

    except Exception as e:
        print(f"Error while processing file: {e}")

# Usage example
directory_path = '../so-vits-svc-fork/recording-file.wav'
get_average_decibels(directory_path)
