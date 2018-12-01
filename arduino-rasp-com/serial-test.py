import serial
import time
import enum

MESSAGE_FIELDS = ['lat', 'lng']
ser = serial.Serial('/dev/ttyACM0',9600)

while True:
	read_serial=ser.readline()
	# print(type(read_serial))
	values = read_serial.split('-')
	# ser.reset_input_buffer()
	ser.flushInput()

	if len(values) != len(MESSAGE_FIELDS):
		print('Invalid format')
	else:		
		for value in values:
			print(value)
	print("")
	# print(read_serial)
	time.sleep(0.1)
	# s[0] = str(int (ser.readline(),10))
	# print s[0]
	# print read_serial
