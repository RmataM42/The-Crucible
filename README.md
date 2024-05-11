Reuse Proj 1​
Add argparse to input baselight file (--baselight),  xytech (--xytech) from proj 1​
Populate new database with 2 collections: One for Baselight (Folder/Frames) and Xytech (Workorder/Location)​
Download my amazing VP video, https://mycsun.box.com/s/v55rwqlu5ufuc8l510r8nni0dzq5qki7Links to an external site.​
Run script with new argparse command --process <video file>  ​
From (5) Call the populated database from (3), find all ranges only that fall in the length of video from (4)
Using ffmpeg or 3rd party tool of your choice, to extract timecode from video and write your own timecode method to convert marks to timecode​
New argparse--output parameter for XLS with flag from (5) should export same CSV export as proj 1 (matching xytech/baselight locations), but in XLS with new column from files found from (6) and export their timecode ranges as well​
Create Thumbnail (96x74) from each entry in (6), but middle most frame or closest to. Add to XLS file to it's corresponding range in new column ​
Render out each shot from (6) using (7) and upload them using API to frame.io (https://developer.frame.io/api/reference/)
---------------------------------------------------------------------------------

Deliverables​

Copy/Paste code​
Excel file with new columns noted on Solve (8) and (9)​
Screenshot of Frame.io account (10)
----------------------------------------------------------------------------------

Grading​

​10 argparse and all new commands​
5 Read DB from proj1

5 Reuse proj1​
20 Timecode work from video and marks​
30 XLS output / Correct XLS info location/frame ranges/TC ranges/thumbnail​
30 Frame.io Upload
