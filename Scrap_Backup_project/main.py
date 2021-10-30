# Scrap_Backup_project #
# Main.py #
#Author: ElPoireau #

###### IMPORT #######

### GUI ###
import dearpygui.dearpygui as dpg

### FILES PROCESSING ###
import os
import os.path
import shutil
import csv
import json
import sqlite3

### OTHER ###
import time
import random as rd

###### CLASS ######

class Button: # class for dearpygui buttons items.

	def __init__(self,window_parent,GUI_text,map_name,is_bk,index,path): # init of the class, create the buttons
		self.window_parent = window_parent # parent(LIST WINDOWS) button
		self.GUI_text = GUI_text # if you don't know what is this variable, your very smart...
		self.map_name = map_name # map_name, just for regonize in software data
		self.is_bk = is_bk # if the map are backup by the system
		self.index = index #index of the object in list
		self.path = path # path of the map
		dpg.add_button(tag=self.index+9999,parent=self.window_parent,label=self.GUI_text,callback=self.call,user_data=self.map_name)

	def call(self,sender,app_data,user_data): #callback function. windowing the map parameters
		self.pos = window_position_tuple(self.index)
		with dpg.window(label="Map parameters",pos=self.pos,width=220,height=110,on_close=window_position_end,user_data=self.pos):
			self.text_map = dpg.add_text("Map name: {}".format(self.map_name))
			if self.is_bk:
				self.label_text="Remove map from backup system"
			else:
				self.label_text="Add map from backup system"
			self.button = dpg.add_button(label=self.label_text,callback=self.bk_state)
			dpg.add_button(label="Backup the map",callback=backup_map_init,user_data=self.map_name)
			dpg.add_button(label="Show extended information",callback=self.pick_stats)


	def bk_state(self,sender,app_data,user_data): # change the text
		if self.is_bk:
			if self.remove_path(self.map_name) == False:
				return False
			self.is_bk = False
			self.label_text="Add map from backup system"
		else:
			if self.add_path(self.map_name) == False:
				return False
			self.is_bk = True
			self.label_text="Remove map from backup system"
		dpg.set_item_label(sender,label=self.label_text)
		dpg.set_item_label(self.index+9999,label=self.map_name + " | " + "Bk: {}".format(self.is_bk))
		#dpg.set_value(sender,"label")
		print(sender)

	def remove_path(self,name): # remove path from files_path.txt
		try:
			with open("files_path.txt", "r") as f:
				lines = f.readlines()
			with open("files_path.txt", "w") as f:
				for line in lines:
					if line.strip("\n") != self.path: #+",mapname=" + name :
						f.write(line)
			return True
		except:
			return False

	def add_path(self,name): #add path from files_path.txt
		try:
			with open("files_path.txt", "r") as f:
				lines = f.readlines()
			with open("files_path.txt", "w") as f:
				for line in lines:
					f.write(line)
					f.write(self.path) #+ map +",mapname=" + map
			return True
		except:
			return False

	def pick_stats(self): # pick the stats of the file
		self.csv_list = []
		self.stat = os.stat(self.path)
		self.stat = str(self.stat)
		self.c_time = self.stat[self.stat.rfind("=",self.stat.rfind("st_ctime"))+1:self.stat.rfind(",",self.stat.rfind("st_ctime"))] # i spent an hour to make the parenthesis # time when the file was create
		self.c_time = time.localtime(int(self.c_time))
		self.c_time = time.strftime("%d %b %Y %H:%M",self.c_time)
		self.m_time = self.stat[self.stat.rfind("=",self.stat.rfind("st_mtime"),self.stat.rfind("st_ctime"))+1:self.stat.rfind(",",self.stat.rfind("st_mtime"),self.stat.rfind("st_ctime"))] # time when the file was modificated
		self.m_time = time.localtime(int(self.m_time))
		self.m_time = time.strftime("%d %b %Y %H:%M",self.m_time)
		self.a_time = self.stat[self.stat.rfind("=",self.stat.rfind("st_atime"),self.stat.rfind("st_mtime"))+1:self.stat.rfind(",",self.stat.rfind("st_atime"),self.stat.rfind("st_mtime"))] # time when they are last acces
		self.a_time = time.localtime(int(self.a_time))
		self.a_time = time.strftime("%d %b %Y %H:%M",self.a_time)
		self.size = self.stat[self.stat.rfind("=",self.stat.rfind("st_size"),self.stat.rfind("st_atime"))+1:self.stat.rfind(",",self.stat.rfind("st_size"),self.stat.rfind("st_atime"))] # size of the file
		try:
			connection = sqlite3.connect(self.path)
			table = connection.cursor()
			sqlite_select_query = "SELECT * from Game"
			table.execute(sqlite_select_query)
			line = table.fetchone()
			self.g_tick = line[3]
			cursor.close()
			connection.close()
		except:
			connection.close()
		self.write_stats()

	def write_stats(self): # write stats in the stats.csv (the stats are pick in pick_stats function).
		backup_folder_check(self.map_name)
		try:
			with open("Backup/{}/stats.csv".format(self.map_name.replace(".db","")), 'r') as file:
				csv_file = csv.DictReader(file)
				for row in csv_file:
					self.csv_list.append(dict(row))
		except:
			pass

		try:
			with open("Backup/{}/stats.csv".format(self.map_name.replace(".db","")), 'w', newline='') as file:
				fieldnames = ["time","crte_time","mod_time","accs_time","size","gme_tick"]
				writer = csv.DictWriter(file, fieldnames=fieldnames)
				writer.writeheader()
				for line in self.csv_list:
					writer.writerow(line)
				writer.writerow({"time":"{}".format(the_time()),"crte_time":"{}".format(self.c_time),"mod_time":"{}".format(self.m_time),"accs_time":"{}".format(self.a_time),"size":"{}".format(self.size),"gme_tick":"{}".format(self.g_tick)}) #this line is tooooooooooooooooooooooooooooooooo fucking long
		except:
			pass

	def graphics(self): # add some info of your map
		self.data = [0,10,100,600,800]
		#with dpg.window(label="Extended map information"):
			#dpg.add_simple_plot(tag=self.index+19999,label="Size",min_scale=0,max_scale=1000,width=200,height=200)
			#dpg.set_value(self.index+19999,self.data)

###### VARIABLE ######

active_window = [False]*11
Xcol1 = 500
Xcol2 = 720
ref_y = 110
pos_x = [Xcol1]*5 + [Xcol2] * 6
pos_y = [ref_y*1,ref_y*2,ref_y*3,ref_y*4,ref_y*5,ref_y*0,ref_y*1,ref_y*2,ref_y*3,ref_y*4,ref_y*5]

###### FUNCTIONS ######

def window_position_tuple(index): # return a Tuple(X,Y) for map window.
	for i in range(len(active_window)):
		if active_window[i] == False:
			active_window.pop(i)
			active_window.insert(i,True)
			return (pos_x[i],pos_y[i])
	return(0,0)

def scan_names(local_path,user_path): # Scan all map or backup in a specified file. for the GUI
	names_list = []
	with os.scandir(local_path) as path:
		for entries in path:
			name = entries.name
			if local_path == user_path:
				if name[len(name)-3:] == ".db":
					names_list.append(name)
				else:
					names_list.append(name)
	return names_list

def the_time(): # send time.
	time_raw = time.localtime() # LOCAL TIME - Year,Month,Day,Hours,Minutes
	time_now = time.strftime("%Y-%m-%d_%H-%M",time_raw)
	return time_now

def window_position_end(sender,app_data,user_data):
	for i in range(len(active_window)):
		if user_data == (pos_x[i],pos_y[i]):
			active_window.pop(i)
			active_window.insert(i,False)

def create_folder(name): # create new folder
	os.mkdir("Backup/{}".format(name[:len(name)-3]))

def backup_folder_check(map): # Check and create folder for map in \Backup
	with os.scandir("Backup/") as files:
		for names in files:
			if names.name == map[:len(map)-3]:
				return False
	create_folder(map)
	return True

def backup_files(path,map): # backup and zip the map
	backup_name = map[:len(map)-3] + "_&_" + the_time()
	shutil.make_archive("backup/{}/{}".format(map[:len(map)-3],backup_name),"zip",root_dir=path[:path.rfind("\\")],base_dir=map) # I HATE THE FUCKING DEV OF ZIP

def is_bk_verif(map_name): # check if the map are already in my database of backuped map. return true if they are.
	with open("files_path.txt","rt") as inline:
		for line in inline:
			if line[line.rfind("\\"):line.rfind("\n")] == map_name:
				return True
	return False

def user_path_modif(sender,user_data,app_data): # change the user path in user_path.txt
	with open("user_path.txt", "w") as file:
		file.write(user_data)

###### INITALIZATION ######

def user_path_init(): # init the user directory of the SM db of the player
	with open("user_path.txt","rt") as useless:
		path = useless.read()
		if path == "":
			u_path = os.path.expanduser("~") + "\\AppData\\Roaming\\Axolot Games\\Scrap Mechanic\\User"
			with os.scandir(u_path) as line:
				for entries in line:
					name = entries.name
					u_path += "\\" + name + "\\Save"
					user_path_modif(False,u_path,False)
					return u_path
		elif path[len(path)-1:] == "\n":
			return path[:len(path)-1]
	return path

def backup_map_init(sender,App_data,user_data): #init the backup to backup a map.
	if user_data == " ": # [SECURITY] : this code activate the backup for all map.
	# if you have the same map name, plz kill me.
		with open("files_path.txt", "r") as lines:
			line = lines.readlines()
			for path in line:
				name = path[path.rfind("\\"):path.rfind("\n")]
				path_map = path[:path.rfind("\\")]
				if backup_folder_check(name) == False:
					backup_files(path_map,name)
				else:
					backup_files(path_map,name)
	else:
		path = str(user_path_init()) + "\\" + str(user_data)
		if backup_folder_check(user_data) == False:
			backup_files(path,user_data)
		else:
			backup_files(path,user_data)

def dearpygui_init(): # init dearpygui and send to button class the button object.
	user_path = user_path_init()
	names_list = scan_names(user_path,user_path)
	map_buttons = []
	dpg.create_context()
	dpg.create_viewport(title='SM backup System', width=1000, height=700) # REAL WINDOWS
	with dpg.window(label="SM Creative Map ({} Map detected)".format(len(names_list)),width=500,no_move=True) as map_window_parent: # LIST WINDOWS [WITH WITH EXPRESSION]
		for i in range(len(names_list)): # i just dont want make list comprension today, sry.
			full_path = user_path + "\\"+ names_list[i]
			map_name = names_list[i]
			map_name.replace(".db","")
			is_bk = is_bk_verif(map_name)
			text = names_list[i] + " | " + "Bk: {}".format(is_bk)
			map_buttons.append(Button(map_window_parent,text,map_name,is_bk,i,full_path))
	with dpg.window(label="Backup",pos=(500,0),no_move=True,width=220,height=110):
		dpg.add_button(label="Backup all map",width=200,height=50,callback=backup_map_init,user_data=" ")
		dpg.add_input_text(label="SM path",hint=user_path_init(),on_enter=True,callback=user_path_modif)
	dpg.setup_dearpygui()
	dpg.show_viewport()
	dpg.start_dearpygui()
	dpg.destroy_context()

###### STARTING ######

if __name__ == '__main__':
	dearpygui_init()
