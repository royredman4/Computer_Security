#!/usr/bin/env python
from time import sleep
import copy
import sys

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
        
'''
    Outputs an error message if the user message if enough
    arguments aren't passed through
'''        
def usage(scriptname):
    msg = "Error too few files!!"
    sys.exit(msg)

'''
    breaks down a string to the group name and their users that
    are in the group, or the groups permissions inside a directory
'''    
def getGroupInfo(line):
    temp_Group = Group()
    mid_index = line.find(":")
    temp_Group.name = line[:mid_index]
    temp_Group.members.extend(line[mid_index+2:].rstrip("\n").rstrip("\r").split(", "))
    return temp_Group


'''
    Grabs the group information based on the file passed and
    saves it into a class list
'''
def getGroups(filename):
    Groups_ary = []
    with open(filename+".txt") as f:
        for line in f:
            Groups_ary.append(getGroupInfo(line))
    return Groups_ary


def Display_Groups(Groups):
    for i in range(len(Groups)):
        print("Group name is: " + str(Groups[i].name))
        print("Group members are: " + str(Groups[i].members))
        print("\n")
    
    
def Display_Actions(User_Actions):
    for i in range(len(User_Actions)):
        print("User performing the action is: " + str(User_Actions[i].name))
        print("User Action that it wants to perform is: " + str(User_Actions[i].action))
        print("User location for that action is at: " + str(User_Actions[i].location))
        print("\n")


def Display_ACLs(AC):
    for i in range(len(AC)):
        print("File # " + str(i) + " is ")
        print("ACL file name is: " + str(AC[i].location))
        print("The users/permissions for those files are")
        for j in range(len(AC[i].group_permissions)):
            print(str(AC[i].group_permissions[j].name))
            print(str(AC[i].group_permissions[j].members))
        print("\n")
        
'''
    Updates the users with their exact permissions
    in a specific directory
'''
def Update_Permissions(group, ACL_directory):
    Update_Ary = []
    temp = Group()

    #Loops based on how many groups there are in a directory (ex: alice,admins for /home/alice)
    for i in range(len(ACL_directory.group_permissions)):
        current_directory_row = ACL_directory.group_permissions[i]

        # looks for the group name based on the group name in the directory
        value_location = [x for x, q in enumerate(group) if current_directory_row.name ==  q.name][0]

        # Loops based on how many users are in the group list
        for k in range(len(group[value_location].members)):
            current_group_member = group[value_location].members[k]

            # Checks if the user name is in any of the directory rows
            zz = [x for x, q in enumerate(ACL_directory.group_permissions) if current_group_member ==  q.name]
            
            # Checks if the name is in Update array or not
            qq = [x for x, q in enumerate(Update_Ary) if current_group_member == q.name]
            
            # if the current member is not located in the directory
            if (len(zz) == 0):
                # if the current member is not located in Update_Ary
                if (len(qq) == 0):
                    
                    # temporary class storage to add to the main list later
                    temp.name = current_group_member
                    temp.members = copy.deepcopy(ACL_directory.group_permissions[i].members)

                    # Adds it to a temporary list to be added to the main one later
                    Update_Ary.append(copy.deepcopy(temp))

                    # Clears out the class list for reusage
                    del temp.members[:]
                    
                     
                # The person is not in the directory, has already been added to the
                # Updated_Ary, but may have some new permissions (because its in a different group)
                else:
                    # Finds the index where of the user in the temporary list
                    pp = [x for x, q in enumerate(Update_Ary) if current_group_member == q.name][0]

                    # If a user has extra permissions that isn't in the temporary
                    # list, then we will add it to the list
                    for value in current_directory_row.members:
                        if value not in Update_Ary[pp].members:
                            Update_Ary[pp].members.append(value)

            # if the name is in the directory rows
            else:
                # Finds the location of the user in the directory
                rr = [x for x, q in enumerate(ACL_directory.group_permissions) if current_group_member == q.name][0]

                # If a user has extra permissions that isn't in the temporary
                # list, then we will add it to the list
                for value in current_directory_row.members:
                    if value not in ACL_directory.group_permissions[rr].members:
                        ACL_directory.group_permissions[rr].members.append(value)

    # Adds the users and permissions from the
    # temporary list into the actual list
    ACL_directory.group_permissions.extend(copy.deepcopy(Update_Ary))

    # Clears the temporary list for later use
    del Update_Ary[:]
    
'''
    grabs the resources information based on
    the file passed through the command line
'''    
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

'''
    Grabs the Attempted actions information
    from the file given
'''
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


'''
    Determines if the user is granted
    or denied the attemped actions based
    on if they have the permissions to do it
'''
def JudgeActions(ACLs, Actions):

    # If there is an error trying to find the
    # index of the location/name/action, then
    # the attempt will be denied, otherwise it
    # will be accepted
    try:
        
        location = [x for x, q in enumerate(ACLs) if Actions.location == q.location][0]
        
        name = [x for x, q in enumerate(ACLs[location].group_permissions) if Actions.name == q.name][0];
        
        action_index = ACLs[location].group_permissions[name].members.index(Actions.action)
        
    except:
        return "DENY"
    
    return "ALLOW"


if __name__ == '__main__':

    if (len(sys.argv) != 4):
        usage(sys.argv[0])
        
    Groups = getGroups(sys.argv[1])
    #Display_Groups(Groups)
    
    ACLs = getACLs(sys.argv[2])
    #Display_ACLs(ACLs)
    
    User_Actions = getActions(sys.argv[3])
    #Display_Actions(User_Actions)
    
    for i in range(len(ACLs)):
        Update_Permissions(Groups, ACLs[i])

    #Display_ACLs(ACLs)

    # Checks to see if the attempted actions are accepted or denied
    for i in range(len(User_Actions)):
        print(JudgeActions(ACLs, User_Actions[i]) + " " + User_Actions[i].name + " " + User_Actions[i].action + " " + User_Actions[i].location)
    
