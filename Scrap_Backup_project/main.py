# Scrap_Backup_project #
# Main.py #
#Author: ElPoireau le Hucker #

###### IMPORT #######

import dearpygui.dearpygui as dpg
import time
import os
import shutil
import random as rd

###### CLASS ######

class Button: # class for dearpygui buttons items.

	def __init__(self,window_parent,first_text,map_name,is_bk,index): # init of the class, create the buttons
		self.window_parent = window_parent # parent(LIST WINDOWS) button
		self.text_first = first_text # if you don't know what is this variable, your very smart...
		self.map_name = map_name # map_name, just for regonize in software data
		self.is_bk = is_bk # if the map are backup by the system
		self.index = index #index
		dpg.add_button(tag=self.index+9999,parent=self.window_parent,label=self.text_first,callback=self.call,user_data=self.map_name)

	def call(self,sender,app_data,user_data):  #callback function. windowing the map parameters
		self.pos = window_position_tuple(self.index)
		with dpg.window(label="Map parameters",pos=self.pos,width=220,height=110,on_close=window_position_end,user_data=self.pos):
			self.text_map = dpg.add_text("Map name: {}".format(self.map_name))
			if self.is_bk:
				self.label_text="Remove map from backup system"
			else:
				self.label_text="Add map from backup system"
			self.button = dpg.add_button(label=self.label_text,callback=self.bk_state)
			dpg.add_button(label="Backup the map",callback=backup_map_init,user_data=self.map_name)
			dpg.add_button(label="Show extended information",callback=self.graphics)

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
					if line.strip("\n") != user_path_init() + "\\" + name +",mapname=" + name :
						f.write(line)
			return True
		except:
			return False

	def add_path(self,map): #add path from files_path.txt
		try:
			with open("files_path.txt", "r") as f:
				lines = f.readlines()
			with open("files_path.txt", "w") as f:
				for line in lines:
					f.write(line)
				f.write(user_path_init() + "\\" + map +",mapname=" + map + "\n")
			return True
		except:
			return False

	def graphics(self):
		self.data = [0,10,100,600,800]
		with dpg.window(label="Extended map information"):
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

def scan_map_or_backup(local_path,user_path): # Scan all map or backup in a specified file. for the GUI
	entries_list = []
	with os.scandir(local_path) as path:
		for entries in path:
			name = entries.name
			if local_path == user_path:
				if name[len(name)-3:] == ".db":
					entries_list.append(name)
				else:
					entries_list.append(name)
					return entries_list

def the_time(): # send time.
	time_raw = time.localtime() # LOCAL TIME - Year,Month,Day,Hours,Minutes
	time_now = time.strftime("%Y-%m-%d_%H-%M",time_raw)
	return time_now

def window_position_end(sender,app_data,user_data):
	for i in range(len(active_window)):
		if user_data == (pos_x[i],pos_y[i]):
			active_window.pop(i)
			active_window.insert(i,False)

def backup_folder_check(map): # Check and create folder for map in \Backup
	with os.scandir("Backup/") as files:
		for names in files:
			if names.name == map[:len(map)-3]:
				return False
	return True

def backup_files(path,map):
	backup_name = map[:len(map)-3] + "_&_" + the_time()
	shutil.make_archive("backup/{}/{}".format(map[:len(map)-3],backup_name),"zip",root_dir=path[:path.rfind("\\")],base_dir=map) # I HATE THE FUCKING DEV OF ZIP

def is_bk_verif(map_name):
	with open("files_path.txt","rt") as inline:
		for line in inline:
			if line[line.rfind(",mapname=")+9:line.rfind("\n")] == map_name:
				return True
	return False

###### INITALIZATION ######

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

def backup_map_init(sender,App_data,user_data): #init the backup to backup a map.
	if user_data == "62329f196cÉ84ffbb37f7c4aà8914a60": # [SECURITY] : this code activate the backup for all map.
	# if you have the same map name, plz kill me.
		with open("files_path.txt", "r") as lines:
			line = lines.readlines()
			for path in line:
				map = path[path.rfind(",mapname=")+9:path.rfind("\n")]
				path_map = path[:path.rfind(",mapname=")+9]
				if backup_folder_check(map) == False:
					backup_files(path_map,map)
				else:
					os.mkdir("Backup/{}".format(map[:len(map)-3]))
					backup_files(path_map,map)
	else:
		path = str(user_path_init()) + "\\" + str(user_data)
		if backup_folder_check(user_data) == False:
			backup_files(path,user_data)
		else:
			os.mkdir("Backup\{}".format(user_data[:len(user_data)-3]))
			backup_files(path,user_data)

def dearpygui_init(): # init dearpygui and send to button class the button object.
	user_path = user_path_init()
	name_list = scan_map_or_backup(user_path,user_path)
	map_buttons = []
	dpg.create_context()
	dpg.create_viewport(title='SM backup System', width=1000, height=700) # REAL WINDOWS
	with dpg.window(label="SM Creative Map ({} Map detected)".format(len(name_list)),width=500,no_move=True) as map_window_parent: # LIST WINDOWS [WITH WITH EXPRESSION]
		for i in range(len(name_list)): # i just dont want make list comprension today, sry.
			map_name = name_list[i]
			map_name.replace(".db","")
			is_bk = is_bk_verif(map_name)
			text = name_list[i] + " | " + "Bk: {}".format(is_bk)
			map_buttons.append(Button(map_window_parent,text,map_name,is_bk,i))
	with dpg.window(label="Backup",pos=(500,0),no_move=True,width=220,height=110):
		dpg.add_button(label="Backup all map",width=200,height=50,callback=backup_map_init,user_data="62329f196cÉ84ffbb37f7c4aà8914a60")
		dpg.add_input_text(label="SM path",hint=user_path_init())
	dpg.setup_dearpygui()
	dpg.show_viewport()
	dpg.start_dearpygui()
	dpg.destroy_context()

###### STARTING ######

if __name__ == '__main__':
	dearpygui_init()
