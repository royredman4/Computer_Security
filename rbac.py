from time import sleep
import copy

class Group:
    def __init__(self):
        self.name = ""
        self.members = []


def getGroups(filename):
    Groups_ary = []
    temp_Group = Group()
    with open(filename+".txt") as f:
        for line in f:
            mid_index = line.find(":")
            temp_Group.name = line[:mid_index]
            temp_Group.members.extend(line[mid_index+2:].rstrip("\n").rstrip("\r").split(", "))
            Groups_ary.append(copy.deepcopy(temp_Group))
            del temp_Group.members[:]
    return Groups_ary


Groups = getGroups("groups")
for i in range(len(Groups)):
    print("Group name is: " + str(Groups[i].name))
    print("Group members are: " + str(Groups[i].members))
    print("\n")
