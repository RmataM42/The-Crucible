import csv

#import Xytech.txt
Xytech_file_path = "Project_1/Sample_Xytech.txt"
xytech_folders = []

try:
    with open(Xytech_file_path, 'r') as read_xytech_file:
        # Filter out only line that contains "/" append in xytech_folders list
        for line in read_xytech_file:
            if "/" in line:
                # If "/" is found, append the line to xytech_folders list
                xytech_folders.append(line)
except FileNotFoundError:
    print("File not found.")
except PermissionError:
    print("Permission denied.")


# Debug: See if xytech_folders[] comes out correctly
# print("\nDebug test:  xytech_folders[]\n")
# for x, folder in enumerate(xytech_folders, start=1):
#     print(x, folder.strip())

# print(xytech_folders)
#import Baselight_export.txt
Baselight_file_path = "Project_1/Sample_Baselight_export.txt"
try:
    with open(Baselight_file_path, 'r') as baselight_file: 
        n = 1 
        for line in baselight_file:
            # Split baselight txt into list w/ whitespace as delimeter
            # Able to: seperate file path and frame 
            line_split = line.split(" ")
                # debug line_split
            # print (n, line_split)
            # n+=1

            # Pop 1st element in list which is always file path
            # After line_pop: line_split will only contains frame number
            line_pop = line_split.pop(0)
                # debug line_pop
            # print(n, line_pop)
            # n+=1

            # Replace "/baselightfilesystem1" w/ "" in 1st element of line_pop
            line_replace = line_pop.replace("/baselightfilesystem1","")
                # debug line_replace
            # print(n, line_replace)
            # n+=1

            # Compare Baselight.txt to Xytech.txt to find matching txt
            # !STILL don't know how new_path comes out to match 15 of baselight
            new_file_path = ""
            for xytech_check in xytech_folders:
                if line_replace in xytech_check:
                        # debug test: line_replace
                    # print(n, line_replace)
                    # n+=1 
                        # debug test: xytech_check 
                    # print(n, xytech_check.strip())
                    # n+=1
                    new_file_path = xytech_check.strip()
                        # debug test: new_file_path 
                    # print(n, new_file_path)
                    # n+=1

            #Frame Computation
            head = ""
            curr = ""
            last = ""
            for frame in line_split:
                # eliminate whitespace in frame list in case of error in script
                # stripped_frame will contonuosly looping (incremeting) throughtout the list
                stripped_frame = frame.strip()
                    # debug test: stripped_frame
                # print(n, stripped_frame)
                # n+=1

                # Check if frame contains <err> and <null> 
                if not stripped_frame.isnumeric():
                    continue
                # Assign pointer head and curr to 1st frame of every line in list
                if head == "":
                    head = int(stripped_frame)
                    curr = head
                        # Debug test: head and curr pointer
                    # print(f"1st if, head: {head}, curr: {curr}, last: {last}")
                    # print(f"stripped_frame: {stripped_frame} ")
                    continue
                    # Debug end of line, test head pointer position base on line 1
                # if stripped_frame ==  1251:
                #     print ((f"End of line 1, head: {head}, curr: {curr}, last: {last}"))

                if int(stripped_frame) == (curr+1):
                    curr = int(stripped_frame)
                        # Debug test: head and curr pointer
                    # print(f"2nd if, head: {head}, curr: {curr}, last: {last}")
                    # print(f"stripped_frame: {stripped_frame} ")
                    continue
                else:
                    # if next frame "skips", ex: 4 -> 31
                    last = curr
                    # if it is an alone frame
                    if head == last:
                        print ("%s %s" % (new_file_path, head))
                    else:
                        print ("%s %s-%s" % (new_file_path, head, last))
                    # proceed to next frame iteration
                    # head points @ next frame after last succesful frame conputation, hence reset
                    head= int(stripped_frame)
                    curr=head
                    last=""
            #End of the line     
            last = curr
            if head != "":
                if head == last:
                    print ("%s %s" % (new_file_path, head))
                        # Debug test: End of line alone frame
                    # print(f"\nLine {n} Alone last, head: {head}, curr: {curr}, last: {last}\n")
                    # n+=1
                else:
                    print ("%s %s-%s" % (new_file_path, head, last))
                        # Debug test: End of line group frame
                    # print(f"\nLine {n} Group last, head: {head}, curr: {curr}, last: {last}\n")
                    # n+=1
except FileNotFoundError:
    print("Baselight_export.txt file not found.")
except PermissionError:
    print("Permission denied.")