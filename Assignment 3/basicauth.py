#!/usr/bin/env python

from scapy.all import *
import base64
import socket


def summarize(pkt):
    print("New spot\n")
    if pkt.haslayer(TCP):
        if (pkt.getlayer(Raw)):
            val = str(pkt[TCP].payload)
            #pkt[TCP].show()
            #temp = str(export_object(pkt.load))
            #temp = temp.decode('base64')
            #print(temp)
            val = str(pkt[Raw].load)
            print(val)
            if (val.find("Authorization") != -1):
                print("Found me a winner!!!" + val)
            #val = (str(pkt[Raw].load))
            #val = str(pkt[TCP].payload)
            #print val
            #val.decode('base64')
            #print val.decode('base64')
        
    #print base64.b64decode(val)
    #print val
    #if (val.find("Authorization: Basic") != -1):
    #    print "Found something!!\n" + val
    #val = pkt.payload
    #print val
    #base64.b64decode(val)
    #val.decode('base64')
    #print str(val)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
j = s.getsockname()[0]
print "socketname is " + j
sniff(prn=summarize, store=0, filter='host ' + j + ' and dst port 80')
#sniff(prn=summarize, store=0)
