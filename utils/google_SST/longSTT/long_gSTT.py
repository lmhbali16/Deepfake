import os
# Imports the Google Cloud client library
from google.cloud import speech

GS_PATH = u'gs://sample_mf/mf_speech_clip.wav'
OUTPUTFILE = r'C:\Users\zhaoh\Desktop\COMP3888\transcriptmf.txt'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\zhaoh\Downloads\pj.json"


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        language_code="en-US",
        audio_channel_count=2,
        enable_automatic_punctuation=True,
        model='video',
        use_enhanced=True
    )

    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=9999999999)
    trans = ''
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        trans += result.alternatives[0].transcript

    return trans


trans = transcribe_gcs(GS_PATH)

with open(OUTPUTFILE, 'a') as out:
    out.write(trans + '\n')
