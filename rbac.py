from time import sleep
import copy


class Group:
    def __init__(self):
        self.name = ""
        self.members = []
        
        
class ACL():
    def __init__(self):
        self.location = ""
        self.group_permissions = []
        
        
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
