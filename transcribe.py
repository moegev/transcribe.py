'''
transcribe target file
any of deepgrams models
any of deepgrams languages

save json output
display transcript or words or metadata or word count or silence amount 
'''
import os
import argparse
import json

def welcome():
	clear_screen()

	print(f"WELCOME TO RAPPY WRAPPER\n Rappy Wrapper is an inchoate Deepgram wrapper. Pass the \'--readme\'' argument to learn more.  ")
	print("\n This script only works with api.deepgram.com NOT the old brain.deepgram.com endpoint. \n ", 
		"##################################################################################################")
	pass
def requestsParser(r):
	from requests_toolbelt.utils import dump
	data = dump.dump_all(r)
	print(data.decode('utf-8'))
## detecting the OS running. 
def os_detect():
	import platform
	# n = os.name()
	system,node,release,version,machine = os.uname()
	out = '\n'.join([system,node,release,version,machine])
	p = platform.system()
	print("\n", out)
	return system

#based on OS, clear the terminal screen. 
def clear_screen():
	system = os_detect()
	print(system, "\n")
	unix = ['darwin', 'linux']
	if system.lower() == "windows":
		os.system('cls')
	elif system.lower() in unix:
		os.system('clear')
	else:
		print("You OS was not recognized")
		pass
#display the readme file
def readme(args):
	if args.readme == True:
		system = os_detect()
		clear_screen()
		script_path, filename, file_extension = fileNames(args.file_path)
		readme = os.path.join(script_path, 'readme.txt')
		with open('readme.txt', 'r') as infile:
			print(infile.read())
		exit()
	else:
		pass


#return all the critical file paths needed to send audio to DG, save the json, retrieve the json
def fileNames(args_filepath):
	script_path = os.path.dirname(os.path.realpath(__file__))
	textDataPath = os.path.join(script_path,'json_outputs')
	pathname, file_extension = os.path.splitext(args_filepath)
	filename = pathname[(pathname.rfind("/") + 1):len(pathname)]
	savename = os.path.join(textDataPath, filename + '.json')

	return script_path, filename, file_extension #this is the audio file extention

#pass hidden or un-hidden API key
def getAPIKey(args):
	print(args.apikey)

	if args.apikey == None:
		raise ValueError("you need to pass either the 40 character DG api key, \
				or unix env variable that points to your api key. ")
	elif len(args.apikey) == 40:
		try:
			return args.apikey
		except:
			raise ValueError("you need to pass either the 40 character DG api key, \
				or unix env variable that points to your api key. ")
	else:
		try:
			os.getenv(args.apikey)
			return os.getenv(args.apikey)
		except:
			raise ValueError("you need to pass either the 40 character DG api key, \
				or unix env variable that points to your api key. ")
# load the local audio file 
def loadAudio(fileName, filetype=str):
	try:
		print(f'loading audio{fileName}')
		data = None
		infile = open(fileName, 'rb')
		return infile
	except:
		print("Looks like the file you wanted to load does not exist. Check the file path ")
		raise ValueError("The file path you shared is wrong somehow.")

# sends data to api.deepgram.com. This is a curl command using requests. 
def dg_transcribe(args): #audio, options=list
	#passing so we can run other functions. 
	if args.transcribe_new == False:
		print("\n Going to load an old transcript with the same filename as this audio file!\n")
		pass
	elif args.transcribe_new == True:
	#ok so you do want to transcribe this
		try:
			import requests
			audio_path = args.file_path
			data = loadAudio(audio_path)

			headers = {'Authorization': 'Token ' + getAPIKey(args), 'Content-Type': 'audio/wav'}
			print(f"sending data to api.deepgram.com {audio_path}.wav")
			r = requests.post('https://api.deepgram.com/v1/listen', headers=headers, data=data)
			data = json.loads(r.content)
			saveJson(data, audio_path)
			return data
		except:
			R = requestsParser(r)
			print(R)
			print("SOMETHING WENT WRONG WITH DEEPGRAM\n Check your API key!")
			exit()

#since we want to minimize 
def checkFile(args_filepath):
	textDataPath, filename, audioFileExtention = fileNames(args_filepath)
	jsonFile = os.path.join(textDataPath, 'json_outputs/' + filename + '.json')

	if os.path.isfile(jsonFile):
		infile = open(jsonFile, 'r')
		print(f'FOUND JSON FILE: {jsonFile}')
		return json.load(infile)
	else:
		message = f"Could not find saved json transcription object {jsonFile}"
		raise Exception(message)

def saveJson(data, audioFileName=str):
	textDataPath, filename, audioFileExtention = fileNames(audioFileName)
	textDataPath = os.path.join(textDataPath,'json_outputs')
	
	
	if os.path.isdir(textDataPath):
		print(f"FOUND THE RIGHT DIRECTORY: {textDataPath}")
	else:
		print(f"CREATING JSON STORAGE DIRECTORY: {textDataPath}")
		os.mkdir(textDataPath)

	savename = os.path.join(textDataPath, filename + '.json')
	with open(savename, 'w') as outfile:
		json.dump(data, outfile)
		print(f'SAVE SUCCESSFUL! {savename}')

def returnWords(jsonFile=dict, options=list):
	print('\n')
	for word in jsonFile["results"]["channels"][0]["alternatives"][0]["words"]:
		print("word : ", word["word"])
		print("duration : ", word["end"]-word["start"])
		print("confidence : ", word["confidence"])
		print('\n')

def returnTranscript(jsonFile=dict):

	print("\n",json.dumps(jsonFile["results"]["channels"][0]["alternatives"][0]["transcript"], indent=3),"\n")

def returnMetaData(jsonFile=dict):

	for item in jsonFile["metadata"]:
		print(item, ": ", jsonFile["metadata"][item])

	print("file-level confidence : ", json.dumps(jsonFile["results"]["channels"][0]["alternatives"][0]["confidence"], indent=3))


def prettyPrint(args): #jsonFile=dict
	actions = ['transcript', 'words', 'metadata', 'results']
	j = checkFile(args.file_path)

	if args.pretty_print not in actions:
		raise Exception("you did not pass a valid keyword")

	elif args.pretty_print == 'metadata':
		returnMetaData(j)

	elif args.pretty_print == 'transcript':
		returnTranscript(j)

	elif args.pretty_print == 'words':
		returnWords(j)
	elif args.pretty_print == 'results':
		print(json.dumps(j["results"], indent=2))

		
def youtubeDL(youtubeID=str):
	pass

def playAudio(audioFileName, duration=int):
	pass

def command_line():
	parser = argparse.ArgumentParser(description='Automaticaly Transcribe audio, do stuff with the transcripts')
	parser.add_argument('--file_path', '-fp', type=str, 
		help='Please provide the path to the file you wish to transcribe. We assume it is a local file.')

	parser.add_argument('--transcribe_new', '-t', action='store_true', default=False, 
		help='You want to send the data to DG and get a new transcript. Leave blank if you want to use an old json stored in memory')

	parser.add_argument('--apikey', '-ak', type=str, default=None, 
		help='Please pass your API key or the env variable name were you keep you DG api key.')

	parser.add_argument('--pretty_print', '-pp', type=str, default='transcript', help='Please specify what \
		you wish to pretty print: \'transcript\'  \'words\'  \'metadata\'')

	parser.add_argument('--readme', action='store_true', default=False, help='pass --readme to learn more about this script and the project in general')

	return parser.parse_args()

def main():
	welcome()
	args = command_line()
	readme(args)
	data = dg_transcribe(args)
	prettyPrint(args)

if __name__ == '__main__':

	main()

