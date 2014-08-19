# -*- coding: UTF-8-*-
from pykml import parser
import urllib2
import json
import smtplib
from email.mime.text import MIMEText

''' helper per comprovar si és un enter'''
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

''' busco els radars '''
def find_radar(obj):
	for elem in dades_radars:
		if (obj == elem['coords']):
			return elem

''' llegeix els radars del txt i comprova si se n'ha actualitzat algun '''
def read_radars(radars):
  error = True  
  with open('radars.txt') as f:
    content = f.readlines()

  content = map(lambda s: s.strip(), content)
  
  for elem in radars:
    val = elem['id'].encode('UTF-8')

    try:
      if content.index(val) == ValueError:
        error = False
    except ValueError:
      return False

  return True

''' desa els radars al TXT '''
def save_radars(radars):
  f = open('radars.txt', 'w')

  for elem in radars:
    f.write(elem['id'])
    f.write('\n')
  
  f.close

''' envia el mail '''
def envia_mail(toAddress, radars):
  print toAddress

  r1 = radars[0]
  r2 = radars[1]
  r3 = radars[2]

  print r1
  
  msg = "\r\n".join([
    "From: frommail@gmail.com",
    "CCO: {0}".format(toAddress),
    "Subject: Radars actius",
    "",
    "Avui son: ", r1['properties']['name'], ", ", r2['properties']['name'], " i ", r3['properties']['name']]).encode('UTF-8')

  print msg

  try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("frommail", "password")
    server.sendmail('frommail@gmail.com', toAddress, msg)
    server.quit()
  except:
    print 'Error'

''' FUNCIÓ PRINCIPAL '''
''' dades propies de coordenades dels radars '''
dades = '[{"id":"v1","coords":"0.6133676,41.616613400000006,0.0","properties":{"tipus":"velocitat","name":"Passeig de Ronda - Bisbe Irurita"}},{"id":"v2","coords":"0.6206524,41.61528990000001,0.0","properties":{"tipus":"velocitat","name":"Rambla d\'Aragó - Ramón y Cajal (direcció riu)"}},{"id":"v3","coords":"0.6184643,41.6071648,0.0","properties":{"tipus":"velocitat","name":"Cos-Gayón - Ton Sirera (Entrada pont dels instituts)"}},{"id":"s1","coords":"0.6277791,41.6227932,0.0","properties":{"tipus":"semàfor vermell","name":"Príncep de Viana - Prat de la Riba (direcció RENFE)"}},{"id":"s2","coords":"0.6181848,41.6213857,0.0","properties":{"tipus":"semàfor vermell","name":"Rovira Roure (abans del Passeig de Ronda direcció Alpicat)"}},{"id":"s3","coords":"0.6196037,41.6131001,0.0","properties":{"tipus":"semàfor vermell","name":"Rambla d\'Aragó (abans del Col·legi Santa Anna direcció riu)"}}]'

''' arxiu KML amb els radars actius '''
url = "https://mapsengine.google.com/map/kml?mid=z45kZP3x8ooc.kaMHfWOv6yyY&amp;lid=z45kZP3x8ooc.kowx9AmEjT18"

file = urllib2.urlopen(url)

root = parser.parse(file).getroot()

nodo = root.Document

''' radars actius de velocitat '''
v1 = root.Document.Folder[0].Placemark[0].Point.coordinates.text.encode('UTF-8')
v2 = root.Document.Folder[0].Placemark[1].Point.coordinates.text.encode('UTF-8')
v3 = root.Document.Folder[0].Placemark[2].Point.coordinates.text.encode('UTF-8')

''' radars de semàfor vermell actius '''
s1 = root.Document.Folder[1].Placemark[0].Point.coordinates.text.encode('UTF-8')
s2 = root.Document.Folder[1].Placemark[1].Point.coordinates.text.encode('UTF-8')
s3 = root.Document.Folder[1].Placemark[2].Point.coordinates.text.encode('UTF-8')

dades_radars = json.loads(dades)

radarv1 = find_radar(v1)
radarv2 = find_radar(v2)
radarv3 = find_radar(v3)

radars1 = find_radar(s1)
radars2 = find_radar(s2)
radars3 = find_radar(s3)

check = read_radars([radarv1, radarv2, radarv3, radars1, radars2, radars3])

''' check = False -> algun radar actualitzat, guardo i envio mail '''
if check == False:
  save_radars([radarv1, radarv2, radarv3, radars1, radars2, radars3])

  envia_mail('toMail', [radarv1, radarv2, radarv3, radars1, radars2, radars3])  