# Main.py #
# ElPoireau le Hucker #

import time
import os

def illegal_caracter(string): # replace illegal caracter.
	string = string.replace(" ","_")
	string = string.replace(":","_")
	string = string.replace("\\","_")
	return string

def backup_creation(db,file_path,folder): # Create backup
	time_raw = time.gmtime() # UTC TIME - Week,Month,Day,Hour,Minute,Second,Year
	time_now = time.asctime(time_raw)
	backup = open("Backup/{}/{}-{}".format(folder,illegal_caracter(time_now),illegal_caracter(file_path)),"xb")
	backup.write(db.read())

def file_init(file_path,folder): #init and test files
	try:
		db = open(r"{}".format(file_path),'rb')
		backup_creation(db,file_path,folder)
		print("File {} Backup".format(file_path))
	except:
		print("Error: can't open file. File Name: {}".format(file_path))

def files_backup(): # init the backup of files that are in the files_path.txt
	with open("files_path.txt","rt") as path:
		for file_path in path:
			file_path = file_path.replace("\n","")
			file_init(file_path[:file_path.rfind(",mapname=")],file_path[file_path.rfind(",mapname=")+9:])

def path_writing(path): # Write the new path to the files_path.txt
	try:
		open(path,"rb")
	except:
		print("Error: file not found")
		return False
	all_line = ""
	with open("files_path.txt","rt") as inline:
		for line in inline:
			if line == "{}\n".format(path):
				print("Error: file path already exist.")
				return False
			all_line = "{}{}".format(all_line,line)
	file_name = "\\{}.".format(path) # security for rfind
	file_name = file_name[file_name.rfind("\\")+1:file_name.rfind(".db")]
	os.mkdir("Backup/{}".format(file_name))
	file = open("files_path.txt","wt")
	file.write("{}{},mapname={}\n".format(all_line,path,file_name))
	print("Path sucessfully enter.")

def scan_map_or_backup(local_path,user_path):
	with os.scandir(local_path) as path:
		for entries in path:
			name = entries.name
			if local_path == user_path:
				if name[len(name)-3:] == ".db":
					print(" ",name)
			else:
				print(" ", name)

def user_path_init(): # init the user directory of the SM db of the player
	try:
		with open("user_path.txt","rt") as useless:
			path = useless.read()
			if path == "":
				print("WARNING! No SM Path.")
			elif path[len(path)-1:] == "\n":
				return path[:len(path)-1]
			return path
	except:
		print("Error: Initilazation of user path failed.")
		return False

def new_user_path(path): # change path in user_path.txt
	try:
		with open("user_path.txt","wt") as newpath:
			newpath.write(path)
		print("Path for the sm map has been change.")
	except:
		print("Error: Path change failed")
		return False
def main(): # the main of the file. are all command system and program loop
	os.system("cls")
	user_path = user_path_init()
	print(user_path)
	print("Welcome. 'help' for help.")
	while True: #CMD, my life is potatos.
		command = input("SM Backup System Facilites: ")
		if command == "help":
			print("Avaliable command:\n backup\n backupall\n pullpath\n showbackup\n showuserdb\n addmap\n newuserpath\n exit\n")
		elif command == "backup":
			path = input("Enter your path: ")
			file_init(path,"other")
		elif command == "backupall":
			print("All knowed map will be backup.")
			files_backup()
		elif command == "pullpath":
			path = input("Enter your path: ")
			path_writing(path)
		elif command == "showuserdb":
			print("All Map Scan from SM database: ")
			scan_map_or_backup(user_path,user_path)
		elif command == "showbackup":
			print("All map Backuped: ")
			scan_map_or_backup("Backup",user_path)
		elif command == "exit":
			break
		elif command == "addmap":
			path = input("Enter the name of you map(Without .db and /): ")
			real_path = user_path + "\\" + path + ".db"
			print(real_path)
			path_writing(real_path)
		elif command == "newuserpath":
			path = input("Enter the new path to acess to your map: ")
			new_user_path(path)
		else:
			print("Unkown command.")

if __name__ == '__main__':
	main()
