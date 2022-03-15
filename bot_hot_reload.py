import time

while True:
	try:
		# import helium
		print('a')
		time.sleep(10000)
	except KeyboardInterrupt:
		print("LOOP", flush=True)
		time.sleep(1)