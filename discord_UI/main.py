from tkinter import *
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


import sys
sys.path.append('../')

from user_api import User


class HTTPGui(BaseHTTPRequestHandler):
	def do_GET(self):
		data = urlparse(self.path)
		host = f'{data.scheme}://{data.netloc}'
		path = data.path
		query = parse_qs(data.query)
		fragment = data.fragment

		if path == "/":
			self.send_response(301)
			self.send_header('Location','main')
			self.end_headers()

		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		
		self.main_page()

	def send(self, *args):
		for arg in args:
			self.wfile.write(bytes(str(arg), "utf-8"))

	def get_page_data(self, path, query):
		if 'guild' in query:
			self.currentGuild = query['guild']
		if 'channel' in query:
			self.currentChannel = query['channel']
		if path == "/main":
			if self.userGuilds is None:
				self.userGuilds = sorted(self.user.getUserGuilds(), key=lambda e: e['name'])

			if self.currentGuild is not None:
				if self.guildChannels[self.currentGuild] is None:
					self.guildChannels[self.currentGuild] = sorted(self.user.getGuildChannels(guild=self.currentGuild), key=lambda e: e['name'])

	def main_page(self, **kwargs):
		with open('main_page.html', 'r') as f:
			fields = f.readline().split()

			fields = {f: kwargs.get(f, 'EMPTY') for f in fields}

			page = f.read().format(**fields)
			self.send(page)


class Account_Viewer():
	def __init__(self, token, *args):
		self.token = token
		self.user = User(token)

		self.userGuilds = []
		self.guildChannels = {}

		self.currentGuild = None
		self.currentChannel = None

		self.init_window()
		self.root.mainloop()

	def init_window(self):
		self.root = Tk()
		self.root.geometry('1000x500')
		self.root.grid_columnconfigure(2, weight=1)
		self.update_root()

	def update_root(self):
		for c in self.root.winfo_children():
			c.destroy()

		guildsFrame = Frame(self.root)
		for i, g in enumerate(sorted(self.user.getUserGuilds(), key=lambda e: e['name'])):
			guild = Button(guildsFrame, text=g['name'], command=lambda g=g: self.open_guild(g['id']))
			guild.grid(row=i, column=0, sticky='ew')

		guildsFrame.grid(row=0, column=0, sticky='ns')

		if self.currentGuild is not None:
			channelFrame = Frame(self.root)
			for i, c in enumerate(sorted(self.user.getGuildChannels(guild=self.currentGuild), key=lambda e: e['name'])):
				channel = Button(channelFrame, text=c['name'], command=lambda c=c: self.open_channel(c['id']))
				channel.grid(row=i, column=0, sticky='ew')
			channelFrame.grid(row=0, column=1, sticky='ns')

		if self.currentChannel is not None:
			textFrame = Frame(self.root)
			for i, t in enumerate(self.user.getChannelMessages(channel=self.currentChannel)):
				text = Label(textFrame, text=t['content'])
				text.grid(row=i, column=0, sticky='ew')
			textFrame.grid(row=0, column=2, sticky='nsew')

	def open_guild(self, guild):
		self.currentGuild = guild
		self.update_root()

	def open_channel(self, channel):
		self.currentChannel = channel
		self.update_root()


if __name__ == "__main__":
	ip = ('', 8000)

	from token_secret import *

	# token = lynapse
	# token = deathwind
	token = will_i_am

	Account_Viewer(token)

	# with HTTPServer(ip, lambda *args, t=token: Account_Viewer(t, *args)) as server:
	# 	print(f'Serving on {ip[0]}:{ip[1]}')
	# 	server.serve_forever()
	# print('Server stopped!')