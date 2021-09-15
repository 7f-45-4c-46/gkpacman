import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys

#read gui files and declare some variables:
handlers = {
    "Close": Gtk.main_quit,
    "Install": install
}

Gtk.Builder().add_from_file("gui.xml")
Gtk.Builder().get_objects()
Gtk.Builder().connect_signals(handlers)

################################
#		functions
################################

def get_info(info, filename):
	with open(filename) as file:
		while (line := file.readline().rstrip()):
			if line[:len(info)] == info:
				return(line[len(info)+3:])
def install():
	
	
################################
#		gui
################################
def draw_gui():
	window = builder.get_object("window1")
	desc = builder.get_object("desc_lab")
	desc.set_text(get_info(pkgdesc, packageFile))
	window.show_all()
	window.connect("destroy", Gtk.main_quit)
	Gtk.main()

################################
#		errors
################################
if len(sys.argv) > 1:
	print("too much arguments")
	err_arg_window = builder.get_object("err_arg")
	err_arg_window.show_all()
else:
	draw_gui()
