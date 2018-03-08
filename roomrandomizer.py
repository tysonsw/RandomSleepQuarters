#!/usr/bin/env python3

'''
This program has been created by Mattias Tauson mattias.tauson.reg(a)gmail.com.
This program takes two input files with lists of participants and a list of rooms and decides who gets to sleep where.


'''


import csv 
from random import *
import random
import locale
import logging
from sys import argv
import os
#locale.getpreferredencoding(do_setlocale=True)
clear = lambda: os.system('cls')
#logging.basicConfig(level=logging.INFO)
secure_random = random.SystemRandom()

decided_location = []
parti_file_input =""
parti_file = ""
room_file_input = ""
room_file = ""
parti_columns =""
parti_needs =""
room_columns = ""
room_needs =""


def read_file(rfile):
	try:
		f = open (rfile, 'r', encoding = 'latin')

	except FileNotFoundError as e:
		print ("Couldn't find file. Try again. ")
		raise
	
	reader = csv.reader(f, delimiter=";")
	return reader

	

def parti_needs_list(all_participant,parti):
	
	with_needs = []

	for x in all_participant:
		for i in parti:
			if x[int(i)]== "x":
				with_needs.append(x)
				break

	return with_needs

def top_row(top_parti, top_room):

	
	participant_row=list(top_parti[0])	
	room_row = list(top_room[0])

	add_output(participant_row,room_row)


def find_room(parti,room, room_file_input, parti_file_input):
	
	output_file = []
	
	all_rooms = list(read_file(room_file_input))
	all_participant = list(read_file(parti_file_input))

	top_row(all_participant,all_rooms)

	all_rooms.pop(0)	
	all_participant.pop(0)

	
	for x in parti_needs_list(all_participant,parti): #hitta behovs personer och loopa listan
		hits = []
		for z in all_rooms:
			for i in range(len(parti)): #loopa behovs kolumnerna
				if x[int(parti[i])] == z[room[i]]:
					#print ("Add 1: {}".format(z))
					if z in hits:
						continue
					hits.append(z)
					continue

				if x[int(parti[i])] in (None, "") and z[room[i]] =="x" :
					#print ("Add 2: {}".format(z))
					if z in hits:
						continue
					hits.append(z)

					
				if  x[int(parti[i])] == "x" and z[room[i]] in (None, "") :
					#print ("Remove 1: {}".format(z))
					if z in hits:
						hits.remove(z)
					break				

		try:
			random_room = secure_random.choice(hits)
			
		except IndexError:
			add_output(output_parti=x,output_exception="Can't find room that meet needs")
			continue
		
		try: 
			if random_room in all_rooms:
			
				all_rooms.remove(random_room)
				add_output(output_parti=x,output_room=random_room)

		except IndexError:
			add_output (output_parti=x,output_exception="Can't find room that meet needs")
			continue

		if x in all_participant:
			
			all_participant.remove(x)

	
	for e in all_participant:
		
		try: 
			random_room = secure_random.choice(all_rooms)
			
		except IndexError:
			add_output(output_parti=e,output_exception="Missing Room")
			continue
			
		try:
			if random_room in all_rooms:
				
				add_output(output_parti=e,output_room=random_room)
				all_rooms.remove(random_room)
				
		except IndexError:
			add_output(output_parti=e,output_exception="Missing Room")
			continue

	#add all unused rooms to the output file
	for i in all_rooms:
		add_output(output_room=i)


	return decided_location
	
def add_output(output_parti=None,output_room=None,output_exception=None):
	output_row = []
	
	if output_parti:
		for x in parti_columns:
			output_row.extend([output_parti[x]])

	if output_exception:
		output_row.append(output_exception)
		decided_location.append(output_row)
		return 

	if output_room:
		for x in room_columns:
			output_row.extend([output_room[x]])

	decided_location.append(output_row)

def clean_input(clean):
	clean = clean.split(',')

	for f in range(len(clean)):
		clean[f] = int(clean[f]) - 1
	
	return clean

def print_first(column_name):
	number = 1
	rows = list(column_name)
	for x in rows[0]:
		print ("{}. {}".format(number, x))
		number += 1

def write_output(result):

	with open('output_file.csv', 'w', encoding = 'latin') as csvoutput:
		writer = csv.writer(csvoutput, lineterminator='\n', delimiter=";")
		for place in result:
			writer.writerows([place])

	print("")			
	print("The sleeping locations has now been saved to output_file.csv")
	input('Press Enter to end the program...')


clear()
print("=================================================================")
print("Welcome to this sleeping area randomizer.")
print("The input files must be csv files and saved as generic csv files.")
print("=================================================================")
print("")

while True:
		
	try:
		parti_file_input = input ("What is the name of your participant file? ")
		parti_file = read_file(parti_file_input)
		break
	except FileNotFoundError as e:
		print ()

while True:

	try:
		room_file_input = input ("What is the name of your room file? ")
		room_file = read_file(room_file_input)
		break
	except FileNotFoundError as e:
		print ()
		
	
clear()
print("=================================")
print("====Participant configuration====")
print("=================================")
print("")
print("We found the following columns in this file: ")
print_first(parti_file)
parti_columns = clean_input(input("Which columns do you want added to the output file? \nSeperate by \",\" and no spaces: "))
parti_needs = clean_input(input("Which numbers include specific needs? \nSeperate by \",\" and no spaces:"))


clear()
print("==========================")
print("====Room configuration====")
print("==========================")
print("")
print("We found the following columns in this file: ")
print_first(room_file)
room_columns = clean_input(input("Which columns do you want added to the output file? \nSeperate by \",\" and no spaces: "))
room_needs = clean_input(input("Which numbers include specific needs? Seperate by \",\" and no spaces:"))

result = find_room(parti_needs, room_needs,room_file_input, parti_file_input)
write_output(result)

