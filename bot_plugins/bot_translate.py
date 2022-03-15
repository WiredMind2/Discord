#Discord_bot.py translate module

try:
	from googletrans import Translator, LANGUAGES
except ImportError:
	print('googletrans module not found!')
	exit()

class Translate:
	def initialize(self):
		txt_cmds = {
			self.translate: ['translate', 'uh', 'huh']
		}
		self.translator = Translator()

		return txt_cmds

	async def translate(self, msg, *args):
		"Translate a message or a text:\n > .uh J'aime les pâtes!"
		if len(args) > 0:
			orig = ' '.join(args)
		elif msg.reference is not None and msg.reference.resolved is not None and hasattr(msg.reference.resolved, 'content') and msg.reference.resolved.content is not None:
			orig = msg.reference.resolved.content
		else:
			await msg.channel.send('You must specify a text or a message to translate!')

		print(f'Translating {orig}')
		try:
			trans = self.translator.translate(text=orig)
		except Exception as e:
			print(f'Error while translating {orig}: {e}')
			await msg.reply(f'Internal error while translating:sob:')
		else:
			await msg.reply(f'From {LANGUAGES[trans.src].capitalize()}: {trans.text}')

module_class = Translate
