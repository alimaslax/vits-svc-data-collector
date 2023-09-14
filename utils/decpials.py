import subprocess

command = ['ffmpeg', '-i', '../so-vits-svc-fork/recording-file.wav', '-af', 'astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=log.txt', '-f', 'null', '-']
output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)

# Extracting the desired values
values = {
    'DC offset': [],
    'Min level': [],
    'Max level': []
}

lines = output.split('\n')
for line in lines:
    line = line.strip()
    if line.startswith('[Parsed_astats_0 @'):
        parts = line.split(': ')
        if len(parts) == 2:
            key = parts[0].split('] ')[1]
            value = parts[1]
            if key in values:
                values[key].append(float(value))

# Calculate averages
averages = {}
for key, value_list in values.items():
    average = sum(value_list) / len(value_list)
    averages[key] = average

# Print the averages
for key, average in averages.items():
    print(f'{key}: {average}')
