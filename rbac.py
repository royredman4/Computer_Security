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
        
        
def getGroupInfo(line):
    temp_Group = Group()
    mid_index = line.find(":")
    temp_Group.name = line[:mid_index]
    temp_Group.members.extend(line[mid_index+2:].rstrip("\n").rstrip("\r").split(", "))
    return temp_Group
    
        
def getGroups(filename):
    Groups_ary = []
    temp_Group = Group()
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


Groups = getGroups("groups")
for i in range(len(Groups)):
    print("Group name is: " + str(Groups[i].name))
    print("Group members are: " + str(Groups[i].members))
    print("\n")

ACL = getACLs("resources")
for i in range(len(ACL)):
    print("ACL file name is: " + str(ACL[i].location))
    print("The users/permissions for those files are")
    for j in range(len(ACL[i].group_permissions)):
        print(str(ACL[i].group_permissions[j].name))
        print(str(ACL[i].group_permissions[j].members))
        
    print("\n")
