"""
 Markdown.py
 0. just print whatever is passed in to stdin
 0. if filename passed in as a command line parameter, 
    then print file instead of stdin
 1. wrap input in paragraph tags
 2. convert single asterisk or underscore pairs to em tags
 3. convert double asterisk or underscore pairs to strong tags

"""

import fileinput
import re

def convertStrong(line):
  line = re.sub(r'\*\*(.*)\*\*', r'<strong>\1</strong>', line)
  line = re.sub(r'__(.*)__', r'<strong>\1</strong>', line)
  return line

def convertEm(line):
  line = re.sub(r'\*(.*)\*', r'<em>\1</em>', line)
  line = re.sub(r'_(.*)_', r'<em>\1</em>', line)
  return line

def convertHeader(line):
  if not re.search(r'^#{1,3}\s+.*$', line):
    line = '<p>' + line + '</p>'
  else:
    line = re.sub(r'^#\s+(.*)$', r'<h1>\1</h1>', line)
    line = re.sub(r'^##\s+(.*)$', r'<h2>\1</h2>', line)
    line = re.sub(r'^###\s+(.*)$', r'<h3>\1</h3>', line)
  if changed and quoted:
    line = '<blockquote>' + line
  elif changed and not quoted:
    line = '</blockquote>' + line
  return line

def convertBlockquote(line):
  global quoted
  global changed
  if not quoted and line.startswith('> '):
    quoted = True
    changed = True
    line = line[2:]
  elif quoted and not line.startswith('> '):
    quoted = False
    changed = True
  else:
    changed = False
    if quoted:
      line = line[2:]
  return line

quoted = False
changed = False
for line in fileinput.input():
  line = line.rstrip() 
  line = convertStrong(line)
  line = convertEm(line)
  line = convertBlockquote(line)
  line = convertHeader(line)
  print line,

