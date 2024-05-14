import pandas as pd
import subprocess

def extract_timecode(file_path):
    try:
        command = [
            'ffmpeg',
            '-i', file_path,
            '-vf', 'showinfo',
            '-f', 'null', 
            '-'
        ]

        result = subprocess.run(command, stderr=subprocess.PIPE, text=True, check=True)
        
        timecodes = []
        for line in result.stderr.split('\n'):
            if 'showinfo' in line and 'pts_time:' in line:
                parts = line.split('pts_time:')
                if len(parts) > 1:
                    timecode = float(parts[1].split(' ')[0])
                    timecodes.append(timecode)
        
        return timecodes

    except subprocess.CalledProcessError as e:
        print(f"ffmpeg command failed with error: {e.stderr}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def convert_seconds_to_timecode(seconds, fps=24):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    frames = int((seconds - int(seconds)) * fps)
    
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, secs, frames)

def timecode_to_seconds(timecode, fps=24):
    parts = timecode.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    frames = int(parts[3])
    
    total_seconds = hours * 3600 + minutes * 60 + seconds + frames / fps
    return total_seconds

# Example usage
file_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Reference/twitch_nft_demo.mp4'
timecodes = extract_timecode(file_path)

# Convert timecodes to HH:MM:SS:FF format
formatted_timecodes = [convert_seconds_to_timecode(tc) for tc in timecodes]

# Read the CSV file
csv_file_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/baselight_xytech.csv'
df = pd.read_csv(csv_file_path)

# Filter rows where the Timecode column matches the extracted timecodes
matching_rows = []
for index, row in df.iterrows():
    timecode_range = row.iloc[2]
    if ' - ' in timecode_range:
        start_timecode, end_timecode = timecode_range.split(' - ')
        start_seconds = timecode_to_seconds(start_timecode)
        end_seconds = timecode_to_seconds(end_timecode)
    
        for tc in timecodes:
            if start_seconds <= tc <= end_seconds:
                matching_rows.append(row)
                break

filtered_df = pd.DataFrame(matching_rows)

# Write the filtered rows to an Excel file
output_file_path = '/Users/amatamuadthong/Desktop/467_multi_media/Project/The-Crucible/Test_thumbnail.xlsx'
filtered_df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f"Filtered data has been written to {output_file_path}")
