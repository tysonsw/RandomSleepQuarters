#!/usr/bin/env python3

'''
This program has been created by Mattias Tauson mattias.tauson.reg(a)gmail.com.
This program takes two input files with lists of participants and a list of
rooms and decides who gets to sleep where.


'''

import csv
from random import *
import random
import logging
import os

clear = lambda: os.system('cls')
secure_random = random.SystemRandom()

decided_location = []


def read_file(rfile):
    try:
        f = open(rfile, 'r', encoding='latin')

    except FileNotFoundError as e:
        print("Couldn't find file. Please try again. ")
        raise

    reader = csv.reader(f, delimiter=";")
    return reader


# This function reaturns a list of participants with needs defined by "x"
def parti_needs_list(all_participant, parti):

    with_needs = []

    for x in all_participant:
        for i in parti:
            if x[i] == "x":
                with_needs.append(x)
                break

    return with_needs


def top_row(top_parti, top_room):

    participant_row = list(top_parti[0])
    room_row = list(top_room[0])

    add_output(output_parti = participant_row, output_room = room_row)


def find_room(parti, room, room_file_input, parti_file_input, group_choice=None, find_room_name=None):

    removed_room = []
    same_room = []
    room_group = []

    all_rooms = list(read_file(room_file_input))
    all_participant = list(read_file(parti_file_input))

    top_row(all_participant, all_rooms)

    all_rooms.pop(0)
    all_participant.pop(0)
    needs_participants = parti_needs_list(all_participant, parti)

    for x in needs_participants:  # find all participants that have specific needs

        hits = []
        for z in all_rooms:

            for i in range(len(parti)):

                if x[parti[i]] == z[room[i]]:
                    if z in hits:
                        continue
                    hits.append(z)
                    continue

                if x[parti[i]] in (None, "") and z[room[i]] == "x":
                    if z in hits:
                        continue
                    hits.append(z)

                # breaks out and discards the chosen room since it doesn't fit the need.
                if x[parti[i]] == "x" and z[room[i]] in (None, ""):
                    if z in hits:
                        hits.remove(z)
                    break

        try:
            random_room = secure_random.choice(hits)
            if random_room in all_rooms:
                add_output(output_parti=x, output_room=random_room)
                all_rooms.remove(random_room)
            if group_choice is not None:
                room_group.append([x[group_choice], random_room[find_room_name]])

        except IndexError:
            add_output(output_parti=x, output_exception="Can't find room that meet needs")
            continue

        if x in all_participant:
            all_participant.remove(x)

    if group_choice is not None:

        for j in room_group:
            for k in all_rooms:
                if k[find_room_name] == j[1]:
                    same_group = []
                    for l in all_participant:
                        if l[group_choice] == j[0]:
                            same_group.append(l)

                    try:
                        print("same_group")
                        random_participant = secure_random.choice(same_group)

                        add_output(output_parti=random_participant, output_room=k)
                        all_rooms.remove(k)
                        removed_room.append([random_participant[group_choice], k[find_room_name]])
                        if l in all_participant:
                            all_participant.remove(l)
                        continue

                    except IndexError:
                        try:
                            random_room = secure_random.choice(all_rooms)
                            if random_room in all_rooms:
                                add_output(output_parti=l, output_room=random_room)
                                all_rooms.remove(random_room)
                                removed_room.append([l[group_choice], random_room[find_room_name]])
                                all_participant.remove(l)
                        except IndexError:
                            add_output(output_parti=l, output_exception="Missing Room")
                            if l in all_participant:
                                all_participant.remove(l)
                            continue

    if group_choice is not None:

        for e in all_participant:
            same_room = []
            for m in removed_room:
                if e[group_choice] == m[0]:
                    for n in all_rooms:
                        if n[find_room_name] == m[1]:
                            same_room.append(n)

                    try:
                        print("same_room")
                        random_room = secure_random.choice(same_room)

                        if random_room in all_rooms:
                            add_output(output_parti=e, output_room=random_room)
                            all_rooms.remove(random_room)
                            removed_room.append([e[group_choice], random_room[find_room_name]])
                            if e in all_participant:
                                all_participant.remove(e)
                    except IndexError:
                        try:
                            random_room = secure_random.choice(all_rooms)
                            if random_room in all_rooms:
                                add_output(output_parti=e, output_room=random_room)
                                all_rooms.remove(random_room)
                                removed_room.append([e[group_choice], random_room[find_room_name]])
                                if e in all_participant:
                                    all_participant.remove(e)
                        except IndexError:
                            add_output(output_parti=e, output_exception="Missing Room")
                            if e in all_participant:
                                all_participant.remove(e)
                            continue

    if group_choice is None:
        for p in all_participant:
            try:
                random_room = secure_random.choice(all_rooms)
                if random_room in all_rooms:
                    add_output(output_parti=p, output_room=random_room)
                    all_rooms.remove(random_room)

            except IndexError:
                add_output(output_parti=p, output_exception="Missing Room")
                if p in all_participant:
                    all_participant.remove(p)
                continue

    # add all unused rooms to the output file
    for o in all_rooms:
        add_output(output_room=o)

    return decided_location

# Cleans the input and removes "," and
# the extra 1 that has been added to the column number by the user.


def clean_input(clean):
    clean = clean.split(',')

    for f in range(len(clean)):
        clean[f] = int(clean[f]) - 1

    return clean

# Prints the headers of the csv files and add ones for simplisity for the user.


def print_first(column_name):
    number = 1
    rows = list(column_name)
    for x in rows[0]:
        print("{}. {}".format(number, x))
        number += 1

# Checks with rows the user ha chosen for the output fil
# and adds these to decided_location for later write to the output file.


def add_output(output_parti=None, output_room=None, output_exception=None):
    output_row = []
    print(output_parti, output_room)
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


def write_output(result):
    while True:
        try:
            with open('output_file.csv', 'w', encoding='latin') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n', delimiter=";")
                for place in result:
                    writer.writerows([place])
                break
        except PermissionError:
            input("Can't create the output file. \nPlease check that it isn't open and make sure that you have permission to the location and then press Enter...")

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
        parti_file_input = input("What is the name of your participant file? ")
        parti_file = read_file(parti_file_input)
        break
    except FileNotFoundError as e:
        print()

while True:

    try:
        room_file_input = input("What is the name of your room file? ")
        room_file = read_file(room_file_input)
        break
    except FileNotFoundError as e:
        print()


clear()
print("=================================")
print("====Participant configuration====")
print("=================================")
print("")
print("We found the following columns in this file: ")
print_first(parti_file)
parti_columns = clean_input(input("Which columns do you want added to the output file? \nSeperate by \",\" and no spaces: "))

parti_needs = clean_input(input("Which numbers include specific needs? \nSeperate by \",\" and no spaces:"))
group_answer = input("Do you want to keep groups together?\n This will require that you specify a room column in the roomoutline file (Y/N): ")
if group_answer == "Y" or group_answer == "y":
    parti_group_column = int(input("Which column holds the names of the group?:")) - 1
else:
    parti_group_column = None

clear()
print("==========================")
print("====Room configuration====")
print("==========================")
print("")
print("We found the following columns in this file: ")
print_first(room_file)
room_columns = clean_input(input("Which columns do you want added to the output file? \nSeperate by \",\" and no spaces: "))
room_needs = clean_input(input("Which numbers include specific needs? Seperate by \",\" and no spaces:"))
if group_answer == "Y" or group_answer == "y":
    room_name = int(input("Which column includes the name of the rooms?: ")) - 1
else:
    room_name = None

result = find_room(parti_needs, room_needs, room_file_input, parti_file_input, group_choice=parti_group_column, find_room_name=room_name)
write_output(result)
