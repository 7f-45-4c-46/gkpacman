import magic
import gi
import tarfile
import random
import os
import subprocess
import zstandard
import getpass
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import sys

rand = str(random.random())[2:7]

################################
#		functions
################################

def get_info(info, file):
	#while (line := file.readline().rstrip()):
	for line in file.splitlines():
		if line[:len(info)] == info:
			return(line[len(info)+3:])
				
def install():
	command='pacman --noconfirm -U '+packageFile = sys.argv[1]
	
def is_deb(packageFile):
	packageMime = magic.from_file(packageFile, mime=True)
	if packageMime == 'application/zstd':
		if checkValidArch(packageFile) == 'valid':
			return('arch')
		else:
			return('invalid')
	elif packageMime == 'application/vnd.debian.binary-package':
		return('debian')
	else:
		return('invalid')

def checkValidArch(package):
	#tar = tarfile.open(package)
	decomp = zstandard.ZstdDecompressor()
	if os.path.isdir('/tmp/gkpac/') != True:
		os.mkdir('/tmp/gkpac/')
	FilePackage = open(package, 'rb')
	FileDestTmp = open('/tmp/gkpac/'+rand+'.tar', 'wb')
	decomp.copy_stream(FilePackage, FileDestTmp)
	FileDestTmp.close()
	FileDestTmp = tarfile.open('/tmp/gkpac/'+rand+'.tar', 'r')
	try:
		FileDestTmp.extractfile('.PKGINFO')
	except:
		return('no')
	else:
		return('valid')
###############################
#read gui files and declare some variables:
handlers = {
    "Close": Gtk.main_quit,
    "install": install
}

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(handlers)
	
################################
#		gui
################################
def draw_gui():
	window = builder.get_object("window1")
	#description of package
	desc = builder.get_object("desc_lab")
	desc_text = get_info("pkgdesc", packageFile)
	if len(desc_text) > 157:
		desc.set_label(str(desc_text)[:156]+"...")
	else:
		desc.set_label(str(desc_text))
	#name of package
	titlepkg = builder.get_object("title_lab")
	title_text = get_info("pkgname", packageFile)
	titlepkg.set_label(str(title_text))
	#author
	author = builder.get_object("author_lab")
	author_text = get_info("packager", packageFile)
	author.set_label("package author: "+str(author_text))
	#size
	size = builder.get_object("size_lab")
	sizepkg = int(get_info("size", packageFile))
	if len(str(sizepkg)) >= 16: #pb
		sizepkg_text = str(sizepkg/1000000000000000)[:4]
		prefix_size = "Pd "
	elif len(str(sizepkg)) >= 13: #tb
		sizepkg_text = str(sizepkg/1000000000000)[:4]
		prefix_size = "Tb "
	elif len(str(sizepkg)) >= 10: #gb
		sizepkg_text = str(sizepkg/1000000000)[:4]
		prefix_size = "Gb "
	elif len(str(sizepkg)) >= 7: #mb
		prefix_size = "Mb "
		sizepkg_text = str(sizepkg/1000000)[:4]
	elif len(str(sizepkg)) >= 4: #kb
		sizepkg_text = str(sizepkg/1000)[:4]
		prefix_size = "Kb "
	else:
		titlepkg.set_label("size: bytes "+str(title_text))
	size.set_label("size: "+prefix_size+str(sizepkg_text))
	#icons
	icon = builder.get_object("icon")
	icon.set_from_file("/home/"+getpass.getuser()+"/.local/share/icons/Papirus-Breeze-Dark/128x128/apps/"+str(title_text)+".svg")
	#show window
	window.set_title("installing "+str(title_text))
	window.show_all()
	window.connect("destroy", Gtk.main_quit)
	Gtk.main()

################################
#		errors
################################
if sys.argv == None:
	print("no arguments")
else:
	packageFile = sys.argv[1]
	arch = is_deb(packageFile)
	if arch == 'arch':
		FileDestTmp = tarfile.open('/tmp/gkpac/'+rand+'.tar', 'r')
		packageFile = FileDestTmp.extractfile('.PKGINFO')
		packageFile = str(packageFile.read().decode("utf-8"))
	#elif arch == 'debian':
	#	subprocess.call(['sh', '/usr/local/etc/debtap '+packageFile])
	else:
		print('not suported')	
	draw_gui()
