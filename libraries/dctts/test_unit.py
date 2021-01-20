import unittest
from run import *
import os
from hyperparams import Hyperparams as hp


class TestVoiceSynthesis(unittest.TestCase):


	#Testing normal text between 1-50 words (1)
	def test_text_length_normal(self):

		result = check_string("Hello.")

		self.assertTrue(result, msg= "This is the minimum length that is accepted (1).")



	#Testing normal text between 1-50 words (33)
	def test_text_length_normal2(self):

		result = check_string("""It is hard to remain motivated when attempting to 
			complete tasks or reach goals that seem overwhelming or are not enjoyable, 
			and lack of motivation significantly affects 
			productivity in all aspects of life.""")

		self.assertTrue(result, msg="This is a normal length of text. Should be accepted.")


	#No text is provided
	def test_no_text(self):

		result = check_string("")

		self.assertFalse(result)


	#Test 50 words
	def test_text_limit(self):

		result = check_string("""By the end of this project, 
			we will deliver a framework to the client that will 
			take text input from a user as a script, 
			and output a video of a motivational figure delivering that script. 
			The project scope includes designing, 
			documenting and delivering this framework where quality and realism.""")

		self.assertTrue(result, msg="This is the word limit that is accepted (50).")

	#Test more than 50 words
	def test_text_over_limit(self):
		
		result = check_string("""By the end of this project, 
			we will deliver a framework to the client that will 
			take text input from a user as a script, 
			and output a video of a motivational figure delivering that script. 
			The project scope includes designing, 
			documenting and delivering this framework where quality 
			and realism is paramount, without the need to implement any user interface.""")


		self.assertFalse(result, msg="This text should not be accepted. Length is 60 words")


	#Unusual character
	def test_unusual_char(self):
		
		result = check_string("This is # some $ unusual \\% ch4r.")

		self.assertFalse(result, msg = "Should not return True for special character.")


	#Check if input text is separated by commas and dots.
	#Result should be lsit of sentences/phrases with no white space
	def test_process_text_normal(self):

		text = "This is a test. There should be three sentences. We will see what happens."

		list_text = process_text(text)

		self.assertEqual(len(list_text), 3, msg = "Number of sentences is 3. List should have length 3.")

		check_whitespace = True

		for line in list_text:

			if line.startswith(" ") or line.endswith(" "):
				check_whitespace = False


		self.assertTrue(check_whitespace, msg="There must be no white space at the beginning and end of sentences")


	#Check text lines when there are commas
	def test_process_text_comma(self):

		text = "This is a test, and there should be four sentences. We will see what happens, and make a judgement."

		list_text = process_text(text)

		self.assertEqual(len(list_text), 4, msg = "Number of phrases is 4. List should have length 4.")

		check_whitespace = True

		for line in list_text:

			if line.startswith(" ") or line.endswith(" "):
				check_whitespace = False


		self.assertTrue(check_whitespace, msg="There must be no white space at the beginning and end of sentences")


	#Check if list of text is written to the right file
	def test_write_text_to_file(self):

		lines = ["This is one sentence.", "This is another sentence.", "This should be it."]

		write_text(lines)

		with open(hp.test_data, "r") as file:
			text = file.read().split("\n")


		result = True
		for idx, line in enumerate(text):

			if line != lines[idx]:
				result = False


		self.assertTrue(result, msg ="Content is wrong or missing!")


	#Check if merge wav works correctly
	def test_merge_wav_files(self):

		path_name = os.getcwd() + "/test/output.wav"

		merge_wav(path_name)

		self.assertTrue(os.isfile(path_name))






if __name__ == "__main__":

	unittest.main()