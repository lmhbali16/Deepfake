import pathlib

import speech_recognition as sr
import os

transcript_file = open('transcript.csv', 'w')
# get number of samples
count = 0
for path in pathlib.Path("./samples").iterdir():
    if path.is_file():
        count += 1

# initialise the recognizer
recog = sr.Recognizer()
# loop through each sample and save text to transcript_post.csv
file_no = 51
filename = ""
text = ""
failed_count = 0
for path in pathlib.Path("./samples").iterdir():
    print(str(path))
    try:
        with sr.AudioFile("./" + str(path)) as source:
            audio_data = recog.record(source)
            try:
                text = recog.recognize_google(audio_data)
            except sr.UnknownValueError:
                print("Transcription failed - " + str(file_no))
                failed_count += 1
                continue
        transcript_file.write(str(path) + ',' + text + '\n')
    except FileNotFoundError:
        break
    except AssertionError:
        continue

print("failed: " + str(failed_count))

transcript_file.close()
