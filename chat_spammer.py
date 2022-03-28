import time
import string
import random
import threading
from datetime import datetime, timedelta


from account_stealer import User
from token_secret import *

write_lock = threading.Lock()

def send_msg(msg, thread=False):
	global write_lock
	if thread:
		return threading.Thread(target=send_msg, args=(msg, False)).start()

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
	token = will_i_am
	user = User(token)

	# guild = 724303646443044995  # TITANIUM
	# channel = 944888647080116224  # global-chat
	# channel = 945569239576764426 # spam

	guild = 946832192531734579 #adii x lyn x william
	channel = 957717058169217094 # william-is-lazy-aka...

	mode = "timestamp"
	i = 1
	first = time.time()
	while True:
		if mode == "timestamp":
			msg = {
				'content': datetime.now().isoformat()
			}
			send_msg(msg)
			next_timestamp = first + (i * 60)
			sleep_time = max(0, next_timestamp - time.time())
			time.sleep(sleep_time)
			i += 1
		if mode == "msg":
			msg = {
				'content': """/// An asynchronous function that completes quickly. async fn quick_task() -> Result<&'static str> { println!("START quick_task"); await!(delay(10)).context("delay failed")?; println!("END quick_task"); Ok("quick_task result") } /// An asynchronous function that completes very slowly. async fn slow_task() -> Result<&'static str> { println!("START slow_task"); await!(delay(10_000)).context("delay failed")?; println!("END slow_task"); Ok("slow_task result") }"""
			}
			send_msg(msg)
			time.sleep(1)
		if mode == "alphabet":
			for l in string.ascii_lowercase:
				send_msg(l, True)
				time.sleep(1)