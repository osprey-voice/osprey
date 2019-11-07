from . import gi_require_version as _
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator


class Indicator():
    def __init__(self, app_name):
        icon_path = gtk.STOCK_INFO
        self._indicator = appindicator.Indicator.new(
            app_name,
            icon_path,
            appindicator.IndicatorCategory.OTHER)
        self._indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self._indicator.set_menu(self._create_menu())

    def _create_menu(self):
        menu = gtk.Menu()

        microphone = gtk.MenuItem('Microphone')
        menu.append(microphone)

        speech_recognition = gtk.MenuItem('Speech Recognition')
        menu.append(speech_recognition)

        menu_separator = gtk.SeparatorMenuItem()
        menu.append(menu_separator)

        open_config_directory = gtk.MenuItem('Open Config Directory')
        menu.append(open_config_directory)

        open_log_file = gtk.MenuItem('Open Log File')
        menu.append(open_log_file)

        menu_separator = gtk.SeparatorMenuItem()
        menu.append(menu_separator)

        quit = gtk.MenuItem('Quit')
        menu.append(quit)
        quit.connect('activate', self._quit)

        menu.show_all()
        return menu

    def _quit(self, source):
        gtk.main_quit()
