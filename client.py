import requests
import serial

#url = 'http://field-test.iv-labs.org/post'
url = 'http://iv-labs.org:4489/post'
#url = 'http://localhost:4489/post'
values = {'identity' : 'bond/james/bond',
          'content' : "{'temperature':28, 'trap':0, 'water':25}"}


ser = serial.Serial("/dev/ttyUSB0", 57600, timeout=1)
while True:
	s=""
	while len(s)==0:
		s=ser.read()
	
	byte=ord(s[0])
	values = {'identity' : 'bond/james/bond',
	          'content' : "{'temperature':"+str(byte)+", 'trap':0, 'water':25}"}
	r = requests.post(url, data=values)
	print r.text
ser.close()



