#!/usr/bin/env python
from time import sleep
import copy
import pudb

'''
A class that contains the name of the group and the
members that are associated with that group
'''
class Group:
    def __init__(self):
        self.name = ""
        self.members = []

        
'''
A class that contains the location of the directory
and the groups/permissions that they are given for
each directory
'''
class ACL():
    def __init__(self):
        self.location = ""
        self.group_permissions = []
        
        
'''
A class that contains the information relating
to an action atempt, based on the users name,
what they wanted to do, and the directory that
they plan on doing it to
'''
class Action():
    def __init__(self):
        self.name = ""
        self.action = ""
        self.location = ""
        

def getGroupInfo(line):
    temp_Group = Group()
    mid_index = line.find(":")
    temp_Group.name = line[:mid_index]
    temp_Group.members.extend(line[mid_index+2:].rstrip("\n").rstrip("\r").split(", "))
    return temp_Group


def getGroups(filename):
    Groups_ary = []
    with open(filename+".txt") as f:
        for line in f:
            Groups_ary.append(getGroupInfo(line))
    return Groups_ary


def Display_ACLs(AC):
    for i in range(len(AC)):
        print("File # " + str(i) + " is ")
        print("ACL file name is: " + str(AC[i].location))
        print("The users/permissions for those files are")
        for j in range(len(AC[i].group_permissions)):
            print(str(AC[i].group_permissions[j].name))
            print(str(AC[i].group_permissions[j].members))
        print("\n")



def Update_Permissions(group, ACL_directory):
    Update_Ary = []
    temp = Group()

    #Loops based on how many groups there are in a directory (ex: alice,admins for /home/alice)
    for i in range(len(ACL_directory.group_permissions)):
        current_directory_row = ACL_directory.group_permissions[i]
        #print("ACL DIrectory groups permissions are " + str(ACL_directory.group_permissions[i].__dict__))
        print("ACL DIrectory groups permissions are " + str(current_directory_row.__dict__))
        
        value_location = [x for x, q in enumerate(group) if ACL_directory.group_permissions[i].name ==  q.name][0]
        print("Value location is index " + str(value_location))
        print("Group values are " + str(group[value_location].__dict__))

        #Loops based on how many members are in the group array (after the semicolon)
        for k in range(len(group[value_location].members)):
            current_group_member = group[value_location].members[k]
            print("Group value members are " + str(current_group_member))
            # if(group[value_location].members[k] not in ACL_directory.group_permissions[i].name):

            #CONTINUE FROM HERE~~~ Needs enumeration
            # Checks if the name is in any of the directory rows
            zz = [x for x, q in enumerate(ACL_directory.group_permissions) if current_group_member ==  q.name]
            print("ZZ is " + str(zz))

            # Checks if the name is in Update array or not
            qq = [x for x, q in enumerate(Update_Ary) if current_group_member == q.name]
            print("QQ is " + str(qq))
            
            #if(current_group_member not in current_directory_row.name):
            #    if (current_group_member not in Update_Ary):
            if (len(zz) == 0):
                if (len(qq) == 0):
                    #pudb.set_trace()
                    temp.name = current_group_member
                    temp.members = copy.deepcopy(ACL_directory.group_permissions[i].members)
                    print("VVVV is " + str(temp.members))
                    Update_Ary.append(copy.deepcopy(temp))
                    del temp.members[:]
                    print("Adding " + str(current_group_member) + " to directory " + str(ACL_directory.location))
                    print("update Ary is " + str(Update_Ary))
                    print("The users/permissions for those locations are")
                    for j in range(len(Update_Ary)):
                        print(str(Update_Ary[j].name))
                        print(str(Update_Ary[j].members))
                    print("\n")
                # The person is not in the directory, has already been added to the
                # Updated_Array, but may have some new permissions (because its in a different group)
                else:
                    pp = [x for x, q in enumerate(Update_Ary) if current_group_member == q.name][0]
                    print("pp is " + str(pp))
                    for value in current_directory_row.members:
                        if value not in Update_Ary[pp].members:
                            Update_Ary[pp].members.append(value)

            # if the name is in the directory rows
            else:
                print("HI")
                rr = [x for x, q in enumerate(ACL_directory.group_permissions) if current_group_member == q.name][0]
                print("rr is " + str(rr))
                print("Current group member is " + str(ACL_directory.group_permissions[rr].members))
                print("Opposing group is " + str(current_directory_row.members))
                #sleep(10)
                for value in current_directory_row.members:
                    if value not in ACL_directory.group_permissions[rr].members:
                        ACL_directory.group_permissions[rr].members.append(value)
                        print("new value appended is " + str(ACL_directory.group_permissions[rr].members))
                        #sleep(10)

    ACL_directory.group_permissions.extend(copy.deepcopy(Update_Ary))
    del Update_Ary[:]

def getACLs(filename):
    ACL_file = open(filename + ".txt", "r")
    ACL_array = []
    temp_ACL = ACL()
    while True:
        line = ACL_file.readline()
        if (line == ""):
            break
        mid_index = line.find(":")
        temp_ACL.location = line[:mid_index]
        while True:
            line = ACL_file.readline()
            if (line == "\r\n" or line == "\n" or line == ""):
                break
            temp_ACL.group_permissions.append(getGroupInfo(line))
        ACL_array.append(copy.deepcopy(temp_ACL))
        del temp_ACL.group_permissions[:]
    return ACL_array


def getActions(filename):
    Action_array = []
    temp_Action = Action()
    with open(filename+".txt") as f:
        for line in f:
            temp_list = line.rstrip("\n").rstrip("\r").split(" ")
            temp_Action.name = temp_list[0]
            temp_Action.action = temp_list[1]
            temp_Action.location = temp_list[2]
            Action_array.append(copy.copy(temp_Action))
    return Action_array


def JudgeActions(ACLs, Actions):
    
    try:
        
        location = [x for x, q in enumerate(ACLs) if Actions.location == q.location][0]
        
        name = [x for x, q in enumerate(ACLs[location].group_permissions) if Actions.name == q.name][0];
        
        action_index = ACLs[location].group_permissions[name].members.index(Actions.action)
        
    except:
        return "DENY"
    
    return "ALLOW"


Groups = getGroups("groups")
for i in range(len(Groups)):
    print("Group name is: " + str(Groups[i].name))
    print("Group members are: " + str(Groups[i].members))
    print("\n")

ACLs = getACLs("resources")
for i in range(len(ACLs)):
    print("ACL file name is: " + str(ACLs[i].location))
    print("The users/permissions for those files are")
    for j in range(len(ACLs[i].group_permissions)):
        print(str(ACLs[i].group_permissions[j].name))
        print(str(ACLs[i].group_permissions[j].members))
    print("\n")

User_Actions = getActions("attempts")
for i in range(len(User_Actions)):
    print("User performing the action is: " + str(User_Actions[i].name))
    print("User Action that it wants to perform is: " + str(User_Actions[i].action))
    print("User location for that action is at: " + str(User_Actions[i].location))
    print("\n")

for i in range(len(ACLs)):
    Update_Permissions(Groups, ACLs[i])

Display_ACLs(ACLs)

for i in range(len(User_Actions)):
    print(JudgeActions(ACLs, User_Actions[i]) + " " + User_Actions[i].name + " " + User_Actions[i].action + " " + User_Actions[i].location)
    
