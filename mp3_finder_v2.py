#!/usr/bin/env python
import Levenshtein
import os
import eyeD3
import MySQLdb as sq
import os.path
import sys
import getopt
ratio_const = 0.7


def help_print():
  print """ ================ HELP =================
Parameter format: 'program_name.py -i input_path '
======================================================"""

def find_mp3(top):
  retval = []
  for dirpath, dirnames, filenames in os.walk(top):
    for f in filenames:
      if f.endswith((".mp3")):
        f = os.path.abspath(os.path.join(dirpath, f))
        retval.append(f)
  return retval

def lev(old_mp3, new_mp3):
    result = Levenshtein.ratio(old_mp3, new_mp3)
    return result   
    

if sys.argv[1:]:
  if sys.argv[2:]:
    parameter = sys.argv[1:]
    
    args = parameter
    optlist, args = getopt.getopt(args, 'i:h:')
  

    for sublist in optlist:
      result = sublist[0].find("-h")
      if result == 0:
        input_parameter = "help" 
        help_print()     
        
           
      result = sublist[0].find("-i")
      if result == 0:
        input_parameter = sublist[1]
      
   
       
  else:
    input_parameter = "help"      
    help_print()
              
 
else:
  input_parameter = "help"
  help_print()

levn = {}
vt = sq.connect("localhost","root", "0000","mp3_db" )
x = vt.cursor()

x.execute("SELECT`TITLE`,`ARTIST`  FROM `mp3_table`")
numrow = int(x.rowcount)
old = x.fetchall()
for a in range(0,numrow):
  levn["TITLE"] = old
  values = levn.values()
  

for values in levn.itervalues():
  for counter in range(0,numrow):
    old_titlee=values[counter]

file_path = input_parameter
for file_name in find_mp3(file_path):
  tag = eyeD3.Tag()  
  tag.link(file_name)
  artist = tag.getArtist() 
  album = tag.getAlbum()
  genre = tag.getGenre()
  title = tag.getTitle()
  year = tag.getYear()
  publisher = tag.getPublisher()
  y = 0
  for i in range(0,numrow):
    ratio=lev(str(values[i]),str(title+" "+artist))
    if ratio > ratio_const:
      y = 1

  if y == 0:
    if len(artist) > 0: 
      try:
        x.execute("""INSERT INTO `mp3_table` (`ID`, `ARTIST`, `ALBUM`, `GENRE`, `TITLE`, `YEAR`, `PUBLISHER`, `FILE_PATH`) VALUES (NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" %(artist, album, genre, title, year, publisher, file_name))
        vt.commit()
      except:
        pass 
