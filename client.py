#!/usr/bin/env python2
# coding: utf-8
"""Quiz Bowl Reader for Python

Reads quiz bowl questions from an xml database

Usage: python reader.py [options] [source]

Options:
  -d ..., --database=...   use specified database file or URL
  -s ..., --speed=...      reads the text at the following speed (chars/s)
  -h, --help              show this help

Examples:
  reader.py                  prints this help message
  reader.py -d pace.xml      reads a random question from the specified database
  reader.py -d pace.xml  -s 40  reads pace at 40 chars/s
"""

import time
import sys
import getopt
import re
import random


def delay_print(s):
    for c in s:
        sys.stdout.write('%s' % c)
        sys.stdout.flush()
        time.sleep(0.04)

def usage():
    print __doc__

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()

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
        question2 = sub[index1 + 5:index2]
    else:
        question2 = sub[index1 + 4:index2]
    delay_print(question2)

if __name__ == "__main__":
    main(sys.argv[1:])

