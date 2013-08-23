#!/usr/bin/env python
from PIL import Image
from PIL.ExifTags import TAGS

import os
import os.path
from datetime import datetime
import shutil
import sys
import getopt

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
  
if sys.argv[1:]:
  if sys.argv[2:]:
    parameter = sys.argv[1:]
    
    args = parameter
    optlist, args = getopt.getopt(args, 'i:o:h:')
  

    for sublist in optlist:
      result = sublist[0].find("-h")
      if result == 0:
        input_parameter = "help" 
        help_print()     
        
           
      result = sublist[0].find("-i")
      if result == 0:
        input_parameter = sublist[1]
      
      result = sublist[0].find("-o")
      if result == 0:
        output_parameter = sublist[1]
       
  else:
    input_parameter = "help"      
    help_print()
              
 
else:
  input_parameter = "help"
  output_parameter = "help"
  help_print()

if input_parameter != "help":
  for a in find_jpgs(input_parameter):
    move_file( a, dest(a,input_parameter))
  


        
