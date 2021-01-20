import os
import string
import scipy
import sys
import glob
from pydub import AudioSegment, effects
from pydub.playback import play
from synthesize import *
from hyperparams import Hyperparams as hp

# CP25E: Additional env vars
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
os.environ["LD_LIBRARY_PATH"] = ":/usr/local/cuda-10.0/lib64:/usr/local/cuda-10.0/extras/CUPTI/lib64:"

MIN_WORD_NUM = 1
MAX_WORD_NUM = 50

#Silence between sentences and commas
COMMA_PAUSE = AudioSegment.silent(duration = 300)
END_PAUSE = AudioSegment.silent(duration = 600)

TARGET_AMP = -10 #amplitude in dBFS


#Check if string format and length is correct
def check_string(text):

	if text is None:
		return False

	text = text.lower()

	if len(text.split(" ")) < MIN_WORD_NUM or len(text.split(" ")) > MAX_WORD_NUM:
		return False

	if not all(i in hp.vocab or i == "," for i in text):
		return False

	return True

#Request text input in terminal
# def request_input(min_word_num = 5, max_word_num = 50):

# 	text_input = None

# 	while True:

# 		if text_input is not None:

# 			text_input = str(input("Add motivational text, please! Please note:\nMinimum word number is "
# 				+ str(min_word_num) + "\nMaximum word number is " 
# 				+ str(max_word_num) + "Numbers need to be written in text\n"
# 				+ "Characters accepted: [a-z, A-Z, ., ', ?]\nHave fun!\n"))

# 		else:
# 			check_text = check_string(text_input, min_word_num, max_word_num)

# 			if check_text:
# 				print("Text is good to go. Move on with processing ")
# 				return text_input

# 			else:
# 				print("Incorrect text! You did not follow the instruction. Try it again!\n\n")
# 				text_input = None



#Return list of sentences
def process_text(text):

	#Split text by dots and remove the last one as it is empty
	if text.count(".") == 0:
		split_lines = [text]
	elif text.endswith("."):
		split_lines = text.split(".")[:-1]
	else:
		split_lines = text.split(".")

	result_text = []

	if len(text) == 0:
		print("Sentence did not end with dot")
		text = text + "."
		split_lines = text.split(".")

	#Add back the dots and remove the white space at the beginning
	for i in range(len(split_lines)):
		
		line = split_lines[i]
		#If text is comma separated
		if "," in line:

			line = line.split(",")
			#remove whitespace
			for j in line[:-1]:
				if j.startswith(" "):
					result_text.append(j[1:])
				else:
					result_text.append(j)
			#remove write space from last section of the sentence and add dot
			if line[-1].startswith(" "):
				result_text.append(line[-1][1:] + ".")

			else:
				result_text.append(line[-1] + ".")
		
		#If no comma in sentence
		else:
			if line.startswith(" "):
				result_text.append(line[1:] + ".")

			else:
				result_text.append(line + ".")
		

	return result_text


#Write into the file
def write_text(text_list):
	print("Start putting text into txt file")

	if len(text_list) > 1:

		with open(hp.test_data, "w") as f:

			for i in range(len(text_list) - 1):
				f.write(text_list[i]+"\n")

			f.write(text_list[-1])

	else:
		with open(hp.test_data, "w") as f:
			f.write(text_list[0])

#Merge all the wav files
def merge_wav(outpath):

	
	file = open(hp.test_data, "r").read().split("\n")

	#get the wav file names that are not the end of a sentence (comma separate)
	idx_comma = [i for i in range(len(file)) if not file[i].endswith(".")]

	wave_files = glob.glob("./" + hp.sampledir + "/*.wav")
	wave_files.sort()

	final_wav = None

	for i in range(len(wave_files)):

		if i == 0:
			final_wav = AudioSegment.from_wav(wave_files[i])
			final_wav = match_target_amplitude(final_wav, TARGET_AMP)

			if i in idx_comma:
				final_wav = final_wav + COMMA_PAUSE

			else:
				final_wav = final_wav + END_PAUSE

		else:
			wav = AudioSegment.from_wav(wave_files[i])
			wav = match_target_amplitude(wav, TARGET_AMP)

			if i in idx_comma:
				final_wav = final_wav + wav + COMMA_PAUSE

			else:
				final_wav = final_wav + wav + END_PAUSE

	out_dir = os.path.dirname(outpath)
	
	if not os.path.isdir(out_dir):
		os.mkdir(out_dir)

	print("exporting: %s" % out_dir)
	final_wav.export(outpath, format = "wav")

# wav amplitude normalisation
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)	

#Cutting silences from wav files
def format_wav_files():

	lines = open(hp.test_data, "r").read().split("\n")

	for i, line in enumerate(lines):
		wav = AudioSegment.from_wav("./"+hp.sampledir+"/" + str(i+1) +".wav")
		newdur = len(line) * 100 #Trim

		if not newdur > len(wav):
			# wav = wav[:- int(len(wav)/6)]
			# else:
			wav = wav[:newdur]

		wav.export("./"+hp.sampledir+"/" + str(i+1) +".wav", format = "wav")	


#Main trigger for voice synthesis, input is text and output directory
def voice_synthesis(text, outaudio):

	

	if not check_string(text):
		print("Text input is incorrect")
		print("Please note:\nMinimum word number is "
				+ str(MIN_WORD_NUM) + "\nMaximum word number is " 
				+ str(MAX_WORD_NUM) + "Numbers need to be written in text\n"
				+ "Characters accepted: [a-z, A-Z, ., ', ?]")
		
		return False

	text = process_text(text)
	write_text(text)

	for i in glob.glob("./"+hp.sampledir+"/*"):
		os.remove(i)	

	synthesize()
	format_wav_files()
	merge_wav(outaudio)



if __name__ == "__main__":

	text = sys.argv[1] #argument for input text
	outaudio = sys.argv[2] #argument for outpath
	voice_synthesis(text, outaudio)




