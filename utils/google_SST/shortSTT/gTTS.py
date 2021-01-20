import io
import os
import csv
# Imports the Google Cloud client library
from google.cloud import speech


# Before you run this code, please set up the environment referring to
# https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries, don't forget to replace the sample folder
# path and the transcript csv file path below, those are the only things you need to modify before running
DIRNAME = r'C:\Users\zhaoh\Desktop\COMP3888\samples'
OUTPUTFILE = r'C:\Users\zhaoh\Desktop\COMP3888\transcript.csv'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\zhaoh\Downloads\pj.json"
# Instantiates a client
client = speech.SpeechClient()

def get_file_paths(dirname):
    file_paths = []
    for root, directories, files in os.walk(dirname):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def process_file(file):
    trans = ''
    # Loads the audio into memory
    with io.open(file, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        language_code="en-US",
        audio_channel_count=2,
        enable_automatic_punctuation = True,
        use_enhanced  = True
    )

    # Detects speech in the audio file
    transcript_arr = client.recognize(config=config, audio=audio)
    for result in transcript_arr.results:
        trans += result.alternatives[0].transcript
    return trans

files = get_file_paths(DIRNAME)                 # get all file-paths of all files in dirname and subdirectories
for file in files:                              # execute for each file
    (filepath, ext) = os.path.splitext(file)    # get the file extension
    file_name = os.path.basename(file)          # get the basename for writing to output file
    if ext == '.wav':                           # only interested if extension is '.wav'
        transcript = process_file(file)                  # result is returned to a
        with open(OUTPUTFILE, 'a') as f:        # write results to file
            writer = csv.writer(f)
            writer.writerow([file_name, transcript])