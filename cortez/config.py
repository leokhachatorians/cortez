import configparser
import sys
import urwid

class Config(object):
	def __init__(self):
		self.path = 'config.cfg'
		self.config = configparser.ConfigParser()
		self.config.read(self.path)

		self.CLIENT_ID = self.config.get('app_settings', 'client_id')
		self.CLIENT_SECRET = self.config.get('app_settings', 'client_secret')
		self.REDIRECT_URI = self.config.get('app_settings', 'redirect_uri')
		self.SAVE_PATH = self.config.get('general', 'where_to_save')
		self.SAVE_TOKEN = self.config.getboolean('oauth', 'save_token')

		self.where = urwid.Text(u"""
		######################################################
		# Replace:
		#    [where_to_save]
		#       If you want to change where files should be
		#       downloaded to
		######################################################""")

		self.client_stuff = urwid.Text(u"""
		######################################################
		# Replace:
		#   [client_id]
		#   [client_secret]
		#   [redirect_uri]
		#       If you wish to run your own SoundCloud
		#       application
		######################################################""")

		self.token_stuff = urwid.Text(u"""
		######################################################
		# Change:
		#    [save_token]
		#       [yes] or [no] depending on whether or not
		#       you want to keep an access token within the
		#       program directory.
		#
		#       If set to False, then you must always
		#       authorize the application upon login
		######################################################""")

		self.palette = [('I say', 'default,bold', 'default', 'bold'),]

		self.where_to_save = urwid.Edit(('I say', u'where_to_save='))
		self.where_to_save.set_edit_text(self.SAVE_PATH)
		self.where_to_save.set_edit_pos(len(self.SAVE_PATH))

		self.client_id = urwid.Edit(('I say', u'client_id='))
		self.client_id.set_edit_text(self.CLIENT_ID)

		self.client_secret = urwid.Edit(('I say', u'client_secret='))
		self.client_secret.set_edit_text(self.CLIENT_SECRET)

		self.redirect_uri = urwid.Edit(('I say', u'redirect_uri='))
		self.redirect_uri.set_edit_text(self.REDIRECT_URI)

		self.save_token = urwid.Edit(('I say', u'save_token='))
		self.save_token.set_edit_text(str(self.SAVE_TOKEN))

		self.save_button = urwid.Button(u'Save')
		self.exit_button = urwid.Button(u'Exit')
		self.div = urwid.Divider()

		self.pile = urwid.Pile(
			[
				self.where,
				self.where_to_save,
				self.client_stuff,
				self.client_id,
				self.client_secret,
				self.redirect_uri,
				self.token_stuff, 
				self.save_token,
				self.save_button,
				self.exit_button
			])

		self.top = urwid.Filler(self.pile, valign='top')

		urwid.connect_signal(self.exit_button, 'click', self.on_exit_clicked)
		urwid.connect_signal(self.save_button, 'click', self.on_save_clicked)

	def open_config(self):
		urwid.MainLoop(self.top, self.palette).run()

	def on_exit_clicked(self, button):
		raise urwid.ExitMainLoop()

	def on_save_clicked(self, button):
		if self.check_if_valid_config():
			self.save_config()

	def check_if_valid_config(self):
		if self.save_token.get_edit_text().lower() not in (1, 0, 'true','false', 'yes', 'no'):
			raise urwid.ExitMainLoop()
		else:
			return True

	def save_config(self):
		self.change('general', 'where_to_save', str(self.where_to_save.get_edit_text()))
		self.change('app_settings', 'client_id', str(self.client_id.get_edit_text()))
		self.change('app_settings', 'client_secret', str(self.client_secret.get_edit_text()))
		self.change('app_settings', 'redirect_uri', str(self.redirect_uri.get_edit_text()))
		self.change('oauth', 'save_token', str(self.save_token.get_edit_text()))
		self.write()
		raise urwid.ExitMainLoop()

	def check_save_token(self):
		try:
			self.SAVE_TOKEN = self.config.getboolean('oauth', 'save_token')
		except ValueError:
			print('<SAVE_TOKEN> value was invalid, defaulting to True')
			self.SAVE_TOKEN = True

	def change(self, section, option, value):
		self.config.set(section, option, value)

	def write(self):
		with open(self.path, 'w') as configfile:
			self.config.write(configfile)