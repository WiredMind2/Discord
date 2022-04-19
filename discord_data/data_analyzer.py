import os
import json
import csv
from datetime import datetime

def servers():
	path = 'package/servers'

	with open(os.path.join(path, 'index.json')) as f:
		index = json.load(f)

	for g_hash, g_name in index.items():
		f_path = os.path.join(path, g_hash)
		for f in os.listdir(f_path):
			print(g_name, '-', f)

def messages():
	path = 'package/messages'

	with open(os.path.join(path, 'index.json')) as f:
		index = json.load(f)

	total = 0

	first, last = None, None

	channels = {}
	msgs_count = {}

	for m_id, m_name in index.items():
		with open(os.path.join(path, 'c' + m_id, 'messages.csv'), encoding='utf-8') as f:
			msgs = csv.DictReader(f)
			count = 0
			for msg in msgs:
				count += 1

				timestamp = datetime.fromisoformat(msg['Timestamp'])
				if first is None or timestamp < first['time']:
					first = {
						'time': timestamp,
						'msg': msg,
						'channel': m_name
					}
				
				if last is None or timestamp > last['time']:
					last = {
						'time': timestamp,
						'msg': msg,
						'channel': m_name
					}

				if msg['Contents'] != '':
					for word in msg['Contents'].lower().split():
						if word in msgs_count:
							msgs_count[word] += 1
						else:
							msgs_count[word] = 1


		total += count
		channels[m_name] = count

	# for channel, count in sorted(channels.items(), key=lambda e: e[1]):
	# 	print(f'{channel}: {count} msgs')

	print('Most sent words:')
	for msg, count in sorted(msgs_count.items(), key = lambda e: e[1])[-3:]:
		print(f'{msg}: {count} times')


	print(f'Total: {total} msgs, {len(channels)} channels')
	print('')

	f_time = first['time'].strftime('%d/%m/%Y, %H:%M')
	first = f"{first['channel']}, {f_time}: {first['msg']['Contents']} / {first['msg']['Attachments']}"

	l_time = last['time'].strftime('%d/%m/%Y, %H:%M')
	last = f"{last['channel']}, {l_time}: {last['msg']['Contents']} / {last['msg']['Attachments']}"

	print(f'First message: {first}, \nLast message: {last}')

messages()