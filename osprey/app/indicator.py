from gi.repository import AppIndicator3 as appindicator, Gtk as gtk

from ..control import quit_program
from ..open import open_config_dir, open_history_file, open_log_file


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

        item = gtk.MenuItem('Microphone')

        def create_microphone_menu():
            sub_menu = gtk.Menu()

            sub_item1 = gtk.RadioMenuItem('None')
            sub_menu.append(sub_item1)

            sub_item2 = gtk.RadioMenuItem('System Default', group=sub_item1)
            sub_item2.set_active(True)
            sub_menu.append(sub_item2)

            separator = gtk.SeparatorMenuItem()
            sub_menu.append(separator)

            return sub_menu

        item.set_submenu(create_microphone_menu())
        menu.append(item)

        item = gtk.CheckMenuItem('Enable Speech Recognition')
        item.set_active(True)
        menu.append(item)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        item = gtk.MenuItem('Open Config Directory')
        item.connect('activate', self._open_config_dir)
        menu.append(item)

        item = gtk.MenuItem('Open History File')
        item.connect('activate', self._open_history_file)
        menu.append(item)

        item = gtk.MenuItem('Open Log File')
        item.connect('activate', self._open_log_file)
        menu.append(item)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        item = gtk.MenuItem('Quit')
        item.connect('activate', self._quit)
        menu.append(item)

        menu.show_all()
        return menu

    def _open_config_dir(self, source):
        open_config_dir()

    def _open_history_file(self, source):
        open_history_file()

    def _open_log_file(self, source):
        open_log_file()

    def _quit(self, source):
        quit_program()
