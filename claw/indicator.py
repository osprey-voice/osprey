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

        item = gtk.MenuItem('Speech Recognition')

        def create_speech_recognition_menu():
            sub_menu = gtk.Menu()

            sub_item = gtk.CheckMenuItem('Enable')
            sub_menu.append(sub_item)

            separator = gtk.SeparatorMenuItem()
            sub_menu.append(separator)

            sub_item = gtk.MenuItem('Language:')

            def create_language_menu():
                sub_menu = gtk.Menu()

                sub_item = gtk.MenuItem('English')
                sub_menu.append(sub_item)

                return sub_menu

            sub_item.set_submenu(create_language_menu())
            sub_menu.append(sub_item)

            return sub_menu

        item.set_submenu(create_speech_recognition_menu())
        menu.append(item)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        item = gtk.MenuItem('Open Config Directory')
        menu.append(item)

        item = gtk.MenuItem('Open Log File')
        menu.append(item)

        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        item = gtk.MenuItem('Quit')
        item.connect('activate', self._quit)
        menu.append(item)

        menu.show_all()
        return menu

    def _quit(self, source):
        gtk.main_quit()
