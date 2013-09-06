#!/usr/bin/env python
from PIL import Image
from PIL.ExifTags import TAGS

import os
import os.path
from datetime import datetime
import shutil
import sys
from optparse import OptionParser


dt_const = 36867

def help_print():
  print """                     ================  HELP =================
          Parameter format: 'program_name.py -i input_path -o output_path'
          ================================================================="""

def find_jpgs(top):
  retval = []
  for dirpath, dirnames, filenames in os.walk(top):
    for f in filenames:
      if f.endswith(('.jpg', '.JPG', 'jpeg', '.JPEG', '.Jpg', '.Jpeg')):
        f = os.path.abspath(os.path.join(dirpath, f))
        retval.append(f)
  return retval
  

def dest(file_path,input_parameter): 
  i = Image.open(file_path)
  dateList = []
  info = i._getexif()
  dateFound = False
  if info:
    if info.has_key(dt_const):
      date = info[dt_const]
      dateFound = True
  if dateFound:
    d = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    return os.path.join(str(output_parameter),str(d.year),str(d.month))
  else:
    return os.path.join(str(output_parameter),str("nodate"))
    
def move_file(file_path, dest_path):
  print dest_path
  if not os.path.exists(dest_path):
    os.makedirs(dest_path)
  try:
    shutil.move(file_path, dest_path)
  except:
    pass
  



parser = OptionParser()
parser.add_option("-i","--input",dest="dest_input")
parser.add_option("-o","--output",dest="dest_output")

(args, options)= parser.parse_args()


if args.dest_input:
  input_parameter = args.dest_input
else:
  help_print()
if args.dest_output:
  output_parameter = args.dest_output
else:
  help_print()
try:
  if input_parameter:
    for a in find_jpgs(input_parameter):
      move_file( a, dest(a,input_parameter))
except:
  pass


        
