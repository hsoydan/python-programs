#!/usr/bin/env python
import os
import eyeD3
import MySQLdb as sq



def find_mp3(top):
  retval = []
  for dirpath, dirnames, filenames in os.walk(top):
    for f in filenames:
      if f.endswith((".mp3")):
        f = os.path.abspath(os.path.join(dirpath, f))
        retval.append(f)
  return retval


vt = sq.connect("localhost","root", "0000","mp3_db" )
x = vt.cursor()
file_path = "/home/hsoydan/Desktop"
for a in find_mp3(file_path):
  tag = eyeD3.Tag()
  tag.link(a)
  artist =  tag.getArtist()  
  album = tag.getAlbum()  
  genre = tag.getGenre()
  title = tag.getTitle()
  year = tag.getYear()
  publisher = tag.getPublisher()
    
  print artist
  try:  
    x.execute("""INSERT INTO `mp3_table` (`ID`, `ARTIST`, `ALBUM`, `GENRE`, `TITLE`, `YEAR`, `PUBLISHER`, `FILE_PATH`) VALUES (NULL, "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" %(artist, album, genre, title, year, publisher, a))
    vt.commit()
  except:
    pass
