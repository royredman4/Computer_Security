#!/usr/bin/env python

from scapy.all import *
import socket


def GetCurrentIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def Vulnerability_Check(pkt):
    if pkt.haslayer(TCP):
        if (pkt.getlayer(Raw)):
            val = str(pkt[TCP].payload)
            identifying_name = "Authorization: Basic"
            index = val.find(identifying_name)
            if (index != -1):
                #print("Found me a winner!!!\n\n" + val)
                user_info = val[index+len(identifying_name)+1: -1]
                try:
                    print("WARNING: Unprotected credentials! " + user_info.decode('base64'))
                except:
                    print("Error Decoding the following Authorization flaw " + user_info)


sniff(prn=Vulnerability_Check, store=0, filter='host ' + GetCurrentIP() + ' and dst port 80')
