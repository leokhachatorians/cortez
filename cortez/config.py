import configparser
import urwid
import tkinter
from tkinter.filedialog import askdirectory

class Config(object):
	def __init__(self):
		self.path = 'config.cfg'
		self.config = configparser.ConfigParser()
		self.config.read(self.path)

		# Config General Settings
		self.SAVE_PATH = self.config.get('general', 'where_to_save')
		self.MAX_THREADS = self.config.getint('general', 'max_threads')

		# Config App Settings
		self.CLIENT_ID = self.config.get('app_settings', 'client_id')
		self.CLIENT_SECRET = self.config.get('app_settings', 'client_secret')
		self.REDIRECT_URI = self.config.get('app_settings', 'redirect_uri')
		
		# Config OAuth Settings
		self.SAVE_TOKEN = self.config.getboolean('oauth', 'save_token')

# The text for where, client_stuff, and token_stuff NEED to be
# formatted as such otherwise urwid does some funky stuff 
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
#       Set to [True] or [False] depending on whether
#       or you want to keep an access token within the
#       program directory.
#
#       If set to False, then you must always
#       authorize the application upon login
######################################################""")

		self.palette = [
		('I say', 'default,bold', 'default', 'bold'),
		('Error', 'default, bold', 'dark red', 'black'),
		('reversed', 'standout', '')]

		self.where_to_save = urwid.Text(('I say', u'where_to_save='))
		self.save_path = urwid.Text(self.SAVE_PATH)

		self.client_id = urwid.Edit(('I say', u'client_id='))
		self.client_id.set_edit_text(self.CLIENT_ID)

		self.client_secret = urwid.Edit(('I say', u'client_secret='))
		self.client_secret.set_edit_text(self.CLIENT_SECRET)

		self.redirect_uri = urwid.Edit(('I say', u'redirect_uri='))
		self.redirect_uri.set_edit_text(self.REDIRECT_URI)

		self.save_token = urwid.Edit(('I say', u'save_access_token?='))
		self.save_token.set_edit_text(str(self.SAVE_TOKEN))

		self.error_message = urwid.Text(u'')
		self.div = urwid.Divider()

		self.directory_selector = urwid.Button(u'Directory Path')
		self.save_button = urwid.Button(u'Save')
		self.exit_button = urwid.Button(u'Exit')
		self.div = urwid.Divider()

		self.pile = [
				self.client_stuff,
				self.client_id,
				self.client_secret,
				self.redirect_uri,
				self.where,
				urwid.Columns(
					[('pack', self.where_to_save),
					self.save_path]),
				urwid.AttrMap(self.directory_selector, None, focus_map='reversed'),
				self.token_stuff, 
				self.save_token,
				self.div,
				self.error_message,
				urwid.AttrMap(self.save_button, None, focus_map='reversed'),
				urwid.AttrMap(self.exit_button, None, focus_map='reversed')]

		self.top = urwid.ListBox(urwid.SimpleFocusListWalker((self.pile)))
		self.main_widget = urwid.Padding(self.top, left=0, right=0)

		urwid.connect_signal(self.exit_button, 'click', self.exit_program)
		urwid.connect_signal(self.save_button, 'click', self.on_save_clicked)
		urwid.connect_signal(self.directory_selector, 'click', self.open_directory_browser)

	def open_config(self):
		urwid.MainLoop(self.main_widget, self.palette).run()

	def exit_program(self, button):
		raise urwid.ExitMainLoop()

	def open_directory_browser(self, button):
		root = tkinter.Tk()
		root.withdraw()
		chosen_directory = askdirectory(initialdir=self.SAVE_PATH)
		if chosen_directory:
			self.save_path.set_text(chosen_directory + '/')

	def on_save_clicked(self, button):
		if self.check_if_valid_config():
			self.ask_to_save()

	def check_if_valid_config(self):
		if self.save_token.get_edit_text().lower() not in ('true','false'):
			self.error_message.set_text(('Error','<save_access_token> only takes [True] or [False]'))
		else:
			return True

	def ask_to_save(self):
		self.main_widget_holder = self.main_widget.original_widget
		self.error_message.set_text(u'')
		save_changes = urwid.Text([u'Save Changes?'])
		yes = urwid.Button(u'Yes')
		no = urwid.Button(u'No')
		urwid.connect_signal(yes, 'click', self.save_config)
		urwid.connect_signal(no, 'click', self.go_back_to_config)
		self.main_widget.original_widget = urwid.Overlay(
			urwid.Filler(urwid.Pile(
				[save_changes,
				 urwid.AttrMap(yes, None, focus_map='reversed'),
				 urwid.AttrMap(no, None, focus_map='reversed')])),
			urwid.SolidFill(u'\N{MEDIUM SHADE}'),
				align='center', width=('relative', 30),
				valign='middle', height=('relative', 20),
				min_width=20, min_height=9)

	def save_config(self, button):
		self.change('general', 'where_to_save', str(self.save_path.get_text()[0]))
		self.change('app_settings', 'client_id', str(self.client_id.get_edit_text()))
		self.change('app_settings', 'client_secret', str(self.client_secret.get_edit_text()))
		self.change('app_settings', 'redirect_uri', str(self.redirect_uri.get_edit_text()))
		self.change('oauth', 'save_token', str(self.save_token.get_edit_text()))
		self.write()
		raise urwid.ExitMainLoop()

	def go_back_to_config(self, button):
		self.main_widget.original_widget = self.main_widget_holder

	def change(self, section, option, value):
		self.config.set(section, option, value)

	def write(self):
		with open(self.path, 'w') as configfile:
			self.config.write(configfile)
