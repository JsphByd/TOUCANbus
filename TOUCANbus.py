import os
import time
import signal
import subprocess
import random

def error(message):
		print("\n\n[\033[31mERROR\033[0m] "+ message)

def status(canFile, bitRate, pluggedIn):
	print("       Bit Rate: \033[32m" + bitRate + "\033[0m")
	print("Loaded CAN file: \033[32m" + canFile + "\033[0m")
	if pluggedIn == 1:
		print("     CAN Device: \033[92mFOUND\033[0m")
	else:
		print("     CAN Device: \033[91mNOT FOUND\033[0m")

def help():
	os.system("clear")
	print("\n\n                          _                                     ")
	print("                         ( ) Egg                                ")
	print("+--------------------------------------------------------------+")
	print("| This is a CANBus Tool designed by Ben Bowman and Joseph Boyd |")
	print("| to help automate pentesting on cars because no other good    |")
	print("| tools were on the market. The current usage is to record     |")
	print("| with the 1. Once the log file is recorded you must           |")
	print("| select the log file with the 2 option and then click 3 to    |")
	print("| replay the entire log file back into the can bus             |")
	print("+--------------------------------------------------------------+")
	input("\n[ENTER] to Return")

def playCode(canFile, bitRate, pluggedIn):
	os.system("clear")
	
	print("\n\n              ,-,---.    ")
	print("             /( ,----`   ")
	print("         ____) (____     ")
	print("       //'--;   ;--'\\   ")
	print("      ///////\_/\\\\\\\  ")
	print("             m m		")
	print("+------------------------+")
	print("|  TOUCANbus automation  |")
	print("|  v.1      |   \033[38;5;196mATTACK\033[0m   |")
	print("+------------------------+")
	status(canFile, bitRate, pluggedIn)
	indCode = input(" Enter CAN Code: ")
	print("\nReplaying Code", end="")

	for i in range(10):
		time.sleep(0.5)
		print(".", end="", flush=True)
	os.system("cansend can0 "+ indCode)

def fileParse(canFile, bitRate, pluggedIn):
	errorThree = "Invalid Option"
	os.system("clear")
	print("\n\n\n                ,-,---.\n             __/( ,----`\n         _,-'    ;\n       ;;.---..-'\n              ,")
	print("+------------------------+")
	print("|  TOUCANbus automation  |")
	print("|  v.1      |   \033[38;5;27mIDLE\033[0m     |")
	print("+------------------------+")
	print("       Bit Rate: \033[32m" + bitRate + "\033[0m")
	print("Loaded CAN file: \033[32m" + canFile + "\033[0m")
	if pluggedIn == 1:
		print("     CAN Device: \033[92mFOUND\033[0m\n")
	else:
		print("     CAN Device: \033[91mNOT FOUND\033[0m\n")
	print("     1         2     3     4 ")
	print("(000.000000)  can0  0XX   [0]  00 00 00 00 00 00 00 00\n")
	portion = 0
	while portion != "Q":
		portion = input("Enter Number to Remove Portion (Q to Quit): ") 
		if portion == "1":
			print("hi")
		elif portion == "2":
			os.system("grep -v "+ can +" " + canFile + " > new.log")
			os.system("cp new.log " + canFile)
			os.system("rm new.log") 
		elif portion == "3":
			print("Good")
		elif portion == "4":
			print("Good")
		else:
			error(errorThree)
	
def canFiles(canFile, bitRate, pluggedIn):
	os.system("clear")
	print("\n\n\n                ,-,---.\n             __/( ,----`\n         _,-'    ;\n       ;;.---..-'\n              ,")
	print("+------------------------+")
	print("|  TOUCANbus automation  |")
	print("|  v.1      |   \033[38;5;27mIDLE\033[0m     |")
	print("+------------------------+")
	status(canFile, bitRate, pluggedIn)
	print("\n")
	files = os.listdir("logs")

	log_files = {}
	i = 0
	for filename in files:
		if filename.endswith(".log") and os.path.isfile("logs/" + filename):
			log_files[i] = filename
			i += 1

	for key in log_files.keys():
		print("[" + str(key) + "] " + log_files[key])
	print("[B] Back\n")
	
	try:    
		selection = input("Select Number: ")
		if selection == "B":
			return "\033[91mNONE\033[0m"
		else:
			return log_files[int(selection)]
	except KeyError:
		error(errorTwo)
		time.sleep(2)
		return "\033[91mNONE\033[0m"

def canFilter(canFile, bitRate, pluggedIn):
	errorThree = "Invalid Option"	
	os.system("clear")
	print("\n\n\n                ,-,---.\n             __/( ,----`\n         _,-'    ;\n       ;;.---..-'\n              ,")
	print("+------------------------+")
	print("|  TOUCANbus automation  |")
	print("|  v.1      |   \033[38;5;27mIDLE\033[0m     |")
	print("+------------------------+")
	status(canFile, bitRate, pluggedIn)
			
	choice = input("\n [1] Manual Filters \n [2] Load Filters from File \n [3] Filter Help \n [4] Reset Filter \n [B] Back \n\n Enter your choice: ")
	filterValues = 'NONE'
	log_files = {}
	while choice != 'B':
		if(int(choice) == 1):
			os.system("clear")
			print("\n\n\n                ,-,---.\n             __/( ,----`\n         _,-'    ;\n       ;;.---..-'\n              ,")
			print("+------------------------+")
			print("|  TOUCANbus automation  |")
			print("|  v.1      |   \033[38;5;27mIDLE\033[0m     |")
			print("+------------------------+")
			status(canFile, bitRate, pluggedIn)
			fileName = input("\nInput String configuration file name: ")
			fileName += ".txt"

			print("\n\033[33m [!]\033[0m Filter String is appended to the end of candump -l can0 command, only input a comma separated list of filters using the syntax in the filter help menu\n")
			filterStr = input("Input Filter String: ")

			filePointer = open(fileName, 'w')
			filePointer.write(filterStr)
			filePointer.close()
			canFilter(canFile, bitRate, pluggedIn)
			
		elif(int(choice) == 2):
			files = os.listdir()

			os.system("clear")
			print("\n\n\n                ,-,---.\n             __/( ,----`\n         _,-'    ;\n       ;;.---..-'\n              ,")
			print("+------------------------+")
			print("|  TOUCANbus automation  |")
			print("|  v.1      |   \033[38;5;27mIDLE\033[0m     |")
			print("+------------------------+")
			status(canFile, bitRate, pluggedIn)
			print("\n+========Filters=========+")

			i = 0
			for filename in files:
				if filename.endswith(".txt") and os.path.isfile(filename):
					log_files[i] = filename
					i += 1

			for key in log_files.keys():

					print("[" + str(key) + "] " + log_files[key])

			try: #There's a logic issue here :(
				fileName = int(input("\nSelect Filter: "))
				filePointer = open(log_files[fileName],'r')
				filterValues = filePointer.read()
			except KeyError:
				print("INVALID KEY OPTION") 
			except FileNotFoundError:
				print("INVALID FILENAME")
					
			return filterValues			
		elif(int(choice) == 3):

			print("\n- Filters are always placed at the end of the candump command after the interface.\n\t Example: candump -l can0,128:7FF \n - Commands should \
				  follow the following format : <canID>:<mask>\n\tuse mask 7FF to filter for an exact match\n - : correlates ==, ~ correlates to != ")
			input("\n[ENTER] to continue\n")
		elif(int(choice) == 4):
			return "NONE"
		elif(choice == "B"):
			return
		else:
			error(errorThree)
			time.sleep(2)
			return

def recordCan(canFile, bitRate, pluggedIn, filterConfigurations):
	os.system("clear")
	print("\n\n\n                ,-,---.\n       \033[38;5;226m) ) )\033[0m __/( ,----` \033[38;5;226m( ( (\033[0m\n         _,-'    ;\n       ;;.---..-'\n              ,")
	print("+------------------------+")
	print("|  TOUCANbus automation  |")
	print("|  v.1      |  \033[38;5;226mRECORDING\033[0m |")
	print("+------------------------+")
	status(canFile, bitRate, pluggedIn)
	run = False
	runAsk = 'j'

	fileName = input(" Input Filename: ")
	fileName += ".log"
	print("\033[31m     [Press Q to stop]\033[0m")

	if filterConfigurations != "NONE":
		recorder = subprocess.Popen(["candump","-l","can0"+filterConfigurations])
	else:
		recorder = subprocess.Popen(["candump","-l","can0"])


	pid = recorder.pid

	while run == False:
		if runAsk == 'q' or runAsk == 'Q':
			run = True
			os.kill(pid, signal.SIGTERM)
		else:
			runAsk = input("")
			
	os.system("find . -type f -name 'candump*' -exec cp {} logs/" + fileName + " \;")
	os.system("find -type f -name 'candump*' -delete")
	print("File Created Successfully!")
		
def dumpCan(canFile, bitRate, pluggedIn):
	os.system("clear")
	os.system("cansniffer -c can0")

def playFile(canFile, bitRate, pluggedIn):
	os.system("clear")
	
	print("\n\n              ,-,---.    ")
	print("             /( ,----`   ")
	print("         ____) (____     ")
	print("       //'--;   ;--'\\   ")
	print("      ///////\_/\\\\\\\  ")
	print("             m m		")
	print("+------------------------+")
	print("|  TOUCANbus automation  |")
	print("|  v.1      |   \033[38;5;196mATTACK\033[0m   |")
	print("+------------------------+")
	status(canFile, bitRate, pluggedIn)
	print("\nReplaying Codes", end="")

	for i in range(10):
		time.sleep(0.5)
		print(".", end="", flush=True)
	os.system("cd logs && canplayer -I "+ canFile)
	
def main():

	os.system("apt-get install can-utils")
	if not os.path.exists("logs"):
		os.makedirs("logs")
	if not os.path.exists("filters"):
		os.makedirs("filters")
	if not os.path.exists("checks"):
		os.makedirs("checks")
	#------------------ERROR MESSAGES------------------
	errorOne = "Please select a valid CAN File"
	errorThree = "Invalid Option"
	errorTwo = "No CAN File Selected"
	errorSix = "Please Plug in CAN Device"
	#----------------END ERROR MESSAGES----------------
	os.system("clear")
	bitRate = input("Enter desired Bitrate (default: 500000): ")
	if bitRate == "":
			bitRate = "500000"
	filterConfigurations = "NONE"
	os.system("sudo ip link set can0 up type can bitrate "+ bitRate)
	os.system("sudo ifconfig can0 txqueuelen 1000")
	os.system("clear")
	canFile = ("\033[91mNONE\033[0m")

	while True:
		os.system("cd checks && ifconfig | grep -o 'can0' > checkDevice.txt")
		with open('checks/checkDevice.txt', 'r') as file:
			file_contents = file.read()
			if "can0" in file_contents:
				pluggedIn = 1
			else:
				pluggedIn = 0
			
		os.system("clear")
		print("\n\n\n                ,-,---.\n             __/( ,----`\n         _,-'    ;\n       ;;.---..-'\n              ,")
		print("+------------------------+")
		print("|  TOUCANbus automation  |")
		print("|  v.1      |   \033[38;5;27mIDLE\033[0m     |")
		print("+------------------------+")
		status(canFile, bitRate, pluggedIn)
		print("ADD FILTER SELECTED HERE")
		print("\n [1] Record CAN \n [2] Dump CAN \n [3] CAN files \n [4] Parse File - Ben \n [5] Play file \n [6] Find Code - Ben and Joe\n [7] Play Specific Code \n [8] Filter - JOE \n [9] Help \n [R] Refresh \n [B] Exit \n")
		choice = input("Enter your choice: ")

		if pluggedIn == 1:
			if choice == "1":
				recordCan(canFile, bitRate, pluggedIn, filterConfigurations)
			elif choice == "2":
				dumpCan(canFile, bitRate, pluggedIn)
			elif choice == "3":
				canFile = canFiles(canFile, bitRate, pluggedIn)
			elif choice == "4":
				if canFile == "\033[91mNONE\033[0m":
					error(errorOne)
					time.sleep(2)
				else:
					fileParse(canFile, bitRate, pluggedIn)
			elif choice == "5":
				if canFile == "\033[91mNONE\033[0m":
					error(errorOne)
					time.sleep(2)
				else:
					playFile(canFile, bitRate, pluggedIn)
			elif choice == "6":
				print("You chose Option 4.")
			elif choice == "7":
				playCode(canFile, bitRate, pluggedIn)
			elif choice == "8":
				canFilter(canFile, bitRate, pluggedIn)
			elif choice == "9":
				help()
			elif choice =="R":
				print("Refreshing...")
			elif choice == "B":
				print("Exiting the program...")
				break
			else:
				error(errorThree)
				time.sleep(2)
		else:
			if choice == "10":
				help()
			elif choice =="R":
				os.system("cd checks && ifconfig | grep -o 'can0' > checkDevice.txt")
				with open('checks/checkDevice.txt', 'r') as file:
					file_contents = file.read()
					if "can0" in file_contents:
						pluggedIn = 1
					else:
						pluggedIn = 0
			elif choice == "4":
				if canFile == "\033[91mNONE\033[0m":
					error(errorOne)
					time.sleep(2)
				else:
					fileParse(canFile, bitRate, pluggedIn)
			elif choice == "3":
				canFile = canFiles(canFile, bitRate, pluggedIn)
			elif choice == "8":
				canFilter(canFile, bitRate, pluggedIn)
			elif choice == "9":
				help()
			elif choice == "4":
				if canFile == "\033[91mNONE\033[0m":
					error(errorOne)
					time.sleep(2)
				else:
					fileParse(canFile, bitRate, pluggedIn)
			elif choice == "B":
				print("Exiting the program...")
				break
			else:
				error(errorSix)
				time.sleep(2)

if __name__ == "__main__":
	main()
