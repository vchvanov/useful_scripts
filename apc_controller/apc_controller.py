#!/usr/bin/python3

import sys
import os
import apc_desc

os.system("echo Starting script")

# Script is doing filtering in 3 iterations of apc_hosts.txt based on user inputs
#
# 3rd iteration is separated in 2 types of device :
#
# Multiple Device - in case of multiple devices connected to this port. Available values:
#                   MultipleDevice1
#                   MultipleDevice2
# Single Device - in case single device connected per port. Any value can be used except Multiple Device values
#
# After filtered list received, script one by one perform with port chosen action (reboot/power on/power off)

# Filtering iteration 1
# Filter by setup number

while True :
    try :
        inputFile = []
        my_file = open(os.path.join(sys.path[0], "apc_hosts.txt"), "r")
        inputFile = my_file
        setup_table = []
        setup_number = input("What is your Setup Id? : ")
        if setup_number == "exit" :
            sys.exit()

        for line in inputFile :
            values = line.split()
            if setup_number == values[0] :
                setup_table.append(line)

        if len(setup_table) == 0 :
            print("There is no such setup number in apc_hosts ! Please enter another one or exit")
            continue
        break

    except KeyboardInterrupt :
        print("Wrong input !")
        continue

# Filtering iteration 2
# Filter by device type

while True :
    try :
        node_table = []
        node_type = input("What is your device type? : ")
        if node_type == "exit" :
            sys.exit()

        for line in setup_table :
            values = line.split()
            if node_type == values[1] :
                node_table.append(line)

        if len(node_table) == 0 :
            print("There is no such device type for this setup ! Please, enter correct value")
            continue
        break

    except KeyboardInterrupt :
        print("Wrong input !")
        continue

# Filtering iteration 3
# Filter by device id

if node_type == "CM" or node_type == "ONU":
    print("Next APC ports were selected for action :")

    for line in node_table :
        values = line.split()
        print(values[3], values[8])
        
else :
    while True :
        try :
            nodeid_table = []

            for line in node_table :
                values = line.split()
                print(values[2])


            node_id = input("What is your device id? ")
            if node_id == "exit" :
                sys.exit()

            for line in node_table :
                values = line.split()
                if node_id == values[2] :
                    nodeid_table.append(line)
            
            print("Next APC ports were selected for action :")

            for line in nodeid_table :
                values = line.split()
                print(values[3], values[8])

            if len(nodeid_table) == 0 :
                print("There is no such node id in this setup! Please, check apc_hosts.txt and enter correct value")
                continue
            break
        except KeyboardInterrupt :
            print("Wrong input !")
            continue

# Performing chosen action with filtered pots

while True :
    try:
        choice = input("Please, select which action to perform with node [off reboot on] : ")
        if choice == "exit" :
            sys.exit()

        if choice == "on" or choice == "off" or choice == "reboot" :
            if node_type == "MultipleDevice1" or node_type == "MultipleDevice2":
                for line in node_table :
                    values = line.split()
                    inputFile = []
                    my_file = open(os.path.join(sys.path[0], "apc_type_mapping.txt"), "r")
                    inputFile = my_file
                    for line in inputFile :
                        types = line.split()
                        if values[3] == types[0] :
                            if types[1] == "type1" :
                                apc_desc.type1(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type2" :
                                apc_desc.type2(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type3" :
                                apc_desc.type3(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type4" :
                                apc_desc.type4(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type5" :
                                apc_desc.type5(values[3], values[4], values[5], values[6], values[7], values[8], choice)

            else :
                for line in nodeid_table :
                    values = line.split()
                    inputFile = []
                    my_file = open(os.path.join(sys.path[0], "apc_type_mapping.txt"), "r")
                    inputFile = my_file
                    for line in inputFile :
                        types = line.split()
                        if values[3] == types[0] :
                            if types[1] == "type1" :
                                apc_desc.type1(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type2" :
                                apc_desc.type2(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type3" :
                                apc_desc.type3(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type4" :
                                apc_desc.type4(values[3], values[4], values[5], values[6], values[7], values[8], choice)
                            elif types[1] == "type5" :
                                apc_desc.type5(values[3], values[4], values[5], values[6], values[7], values[8], choice)

        else :
            print("Unknown action ! Please, enter correct action")
            continue
        break
    except KeyboardInterrupt :
        print("Wrong input !")
        continue
