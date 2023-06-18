## Notes

# Change the arguments and the input file here
input_dir = '/'  # Directory containing the input files
output_dir = '/'
min_silence_length = 0.1  # The minimum length of silence at which a split may occur [seconds]. Defaults to 3 seconds.
silence_threshold = 5e-3  # The energy level (between 0.0 and 1.0) below which the signal is regarded as silent.
step_duration = 0.01/10   # The amount of time to step forward in the input file after calculating energy. Smaller value = slower, but more accurate silence detection. Larger value = faster, but might miss some split opportunities. Defaults to (min-silence-length / 10.).
min_clip_length = 5.0  # The minimum length of the clip to be written [seconds].
seg_combine = 6 # number of segments to combine





# AudioSlicer

A simple Audio Slicer in Python which can split .wav audio files into multiple .wav samples, based on silence detection. Also, it dumps a .json that contains the periods of time in which the slice occours, in the following format: 

{sample nº : [cut start, cut end]}. Ex.:

{"0": ["0:0:0", "0:0:3"], "1": ["0:0:3", "0:0:10"], "2": ["0:10:0", "0:0:22"], "3": ["0:0:22", "0:0:32"]}

The code was taken from <b>/andrewphillipdoss.</b> Thanks!

The filename will also contains the parts when the video were sliced, ex.: sample01_0349_0401.wav


<h2> AI Adaptation </h2>
This project will turn into a neural network which can detect audio silence and split the files.
It will also needs to learn to detect 'breathing noises' from the dictator and remove from it.



<h2> Python 3.11.0 </h2>

numpy (1.24.1)

scypi (1.10.0)

tqdm (4.64.1)


<h2> Usage </h2>
To run this code, just change the path of the <b>input_file</b> and <b>output_dir</b> inside the code.
<br/><br/>
:exclamation:Ps: Please note that in order for your audio file to be cut into samples, it should contain periods of "silence". If you are trying to extract voice samples from a song, for example, it may not work as expected.
<br /><br />
Depending on the level of noise in your audio, the algorithm may skip the silence windows, resulting in missed cuts. Ensure that your audio is free from unwanted noise and that the silences are clearly defined. You can adjust the parameters of <b>min_silence_length</b>, <b>silence_threshold</b>, and <b>step_duration</b> to modify the length, amplitude, and duration of the silence window in order to better match your audio
