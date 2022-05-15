import time
import string
import threading
from datetime import datetime


from user_api import User
from token_secret import *

write_lock = threading.Lock()

def send_msg(user, msg, thread=False):
	global write_lock
	if thread:
		return threading.Thread(target=send_msg, args=(user, msg, False)).start()

	if isinstance(msg, str):
		msg = {
			'content': msg
		}
	try:
		with write_lock:
			m = user.createMessage(channel=channel, content=msg)
			if 'retry_after' in m:
				print('retry_after:', m['retry_after'])
				time.sleep(m['retry_after'])
			else:
				if 'timestamp' in m:
					print(m['timestamp'] + ' - ' + m['content'])
				else:
					print(m)
	except Exception as e:
		print("Error:", e)

if __name__ == "__main__":
	tokens = [will_i_am, adithiii]
	users = [User(token) for token in tokens if token is not None]

	guild = 724303646443044995  # TITANIUM
	# channel = 944888647080116224  # global-chat
	channel = 945569239576764426 # spam

	# guild = 946832192531734579 #adii x lyn x william
	# channel = 957717058169217094 # william-is-lazy-aka...

	mode = "timestamp"
	i = 1
	first = time.time()
	while True:
		if mode == "timestamp":
			msg = {
				'content': datetime.now().isoformat()
			}
			for user in users:
				send_msg(user, msg)
			next_timestamp = first + (i * 30)
			sleep_time = max(0, next_timestamp - time.time())
			time.sleep(sleep_time)
			i += 1
		if mode == "msg":
			msg = {
				'content': ":parrot:"
			}
			for user in users:
				send_msg(user, msg)
			time.sleep(1)
		if mode == "alphabet":
			for l in string.ascii_lowercase:
				for user in users:
					send_msg(user, l, True)
				time.sleep(1)