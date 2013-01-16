#!/usr/bin/env python2


import re
import random


input = open('output.xml', 'r').read()
packets = [m.start() for m in re.finditer('packet', input)]
packet = random.randint(0, (len(packets) / 2) - 1) * 2
packetname = input[packets[packet] + 11:]
packetname = packetname[:packetname.find("\"")]
sub = input[packets[packet]:]
question = random.randint(1, 20)
index1 = sub.find("<q" + str(question) + ">")
index2 = sub.find("</q" + str(question) + ">")
print "packet: " + packetname + ", question: " + str(question) + "\n"
if question > 9:
    print sub[index1 + 5:index2]
else:
    print sub[index1 + 4:index2]
