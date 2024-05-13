from argparse import ArgumentParser
from pymongo import MongoClient
import os
import csv
import sys
import pandas as pd

# Argparse setup
parser = ArgumentParser(description='It does frame IO... stuff..')

parser.add_argument("--baselight", metavar='', help="Baselight stuff")
parser.add_argument("--xytech", metavar='', help="Xytech stuff")
parser.add_argument("--process", metavar='', help="Process stuff")
parser.add_argument("--output", metavar='', help="Output stuff")
# debug: argparse
parser.add_argument("--frame-timecode", metavar='', type=int, help="Frame to timecode; must follow by an integer to calcualte")
# debug baselight xytech from project 1
parser.add_argument("-bx", action='store_true', help="Project 1: output baselight+xytech w/ frame range")
args = parser.parse_args()

# File path
Xytech_file_path = "baselight_xytech/Sample_Xytech.txt"
Baselight_file_path = "baselight_xytech/Sample_Baselight_export.txt"

# DB setup
# Connect to MongoDB locally
client = MongoClient("mongodb://localhost:27017/")
# Get the crucicle database
db = client["crucible"]
final = db["Baselight_Xytech"]

# Modified project 1: written to csv file instead of console output
def baselight_xytech_csv():
    xytech_folders = []
    try:
        with open(Xytech_file_path, 'r') as read_xytech_file:
            for line in read_xytech_file:
                if "/" in line:
                    xytech_folders.append(line.strip())
    except FileNotFoundError:
        print("File not found.")
        return
    except PermissionError:
        print("Permission denied.")
        return

    try:
        with open(Baselight_file_path, 'r') as baselight_file, open("baselight_xytech.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['location', 'Frames to fix'])

            for line in baselight_file:
                line_split = line.split(" ")
                line_pop = line_split.pop(0)
                line_replace = line_pop.replace("/baselightfilesystem1","")
                new_file_path = ""
                for xytech_check in xytech_folders:
                    if line_replace in xytech_check:
                        new_file_path = xytech_check.strip()

                head = ""
                curr = ""
                last = ""
                for frame in line_split:
                    stripped_frame = frame.strip()
                    if not stripped_frame.isnumeric():
                        continue
                    if head == "":
                        head = int(stripped_frame)
                        curr = head
                        continue

                    if int(stripped_frame) == (curr+1):
                        curr = int(stripped_frame)
                        continue
                    else:
                        last = curr
                        if head == last:
                            writer.writerow([new_file_path, str(head)])
                        else:
                            writer.writerow([new_file_path, str(head) + '-' + str(last)])
                        head= int(stripped_frame)
                        curr=head
                        last="" 
                last = curr
                if head != "":
                    if head == last:
                        writer.writerow([new_file_path, str(head)])
                    else:
                        writer.writerow([new_file_path, str(head) + '-' + str(last)])
    except FileNotFoundError:
        print("Baselight_export.txt file not found.")
        return
    except PermissionError:
        print("Permission denied.")
        return

# convert frame to time code
def calculate_frame_to_timecode(frame, fps=24):
    hours = frame // (3600 * fps)
    frame %= 3600 * fps
    minutes = frame // (60 * fps)
    frame %= 60 * fps
    seconds = frame // fps
    frame %= fps
    return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frame)

def retrieve_frame_data():
    try:
        frame_data = []
        for x in final.find({}, {"Frames to fix": 1, "_id": 0}):  # Retrieve only 'frame' field, exclude '_id'
            frame_data.append(x["Frames to fix"])
        return frame_data
    except Exception as e:
        print("Error:", e)

def output_frame_to_timecode():
    frame_data = retrieve_frame_data()
    timecode_list = []
    for frame_range in frame_data:
        frames = str(frame_range).split('-')
        start_frame = int(frames[0])
        end_frame = int(frames[-1]) if len(frames) > 1 else start_frame
        start_timecode = calculate_frame_to_timecode(start_frame)
        end_timecode = calculate_frame_to_timecode(end_frame)
        if start_frame != end_frame:
            timecode_range = f"{start_timecode} - {end_timecode}"
        else:
            timecode_range = start_timecode
        timecode_list.append(timecode_range)
    
    # Read the existing CSV file
    df = pd.read_csv('baselight_xytech.csv')
    
    # Add the timecodes to the DataFrame
    df['Timecode'] = timecode_list
    
    # Write the updated DataFrame back to the CSV file
    df.to_csv('baselight_xytech.csv', index=False)
    
    print("Timecodes added to baselight_xytech.csv successfully!")

# output_frame_to_timecode()

if args.frame_timecode:
    print(f"Frame {args.frame_timecode} is {calculate_frame_to_timecode(args.frame_timecode)} at 24 fps")
if args.bx:
    baselight_xytech_csv()
