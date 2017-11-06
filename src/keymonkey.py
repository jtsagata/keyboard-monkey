# This is for the anaconda environment
import hashlib
from pathlib import Path
from IPython.display import Image, display

from keyboard import *
from typist import *


def bash_command(cmd):
    proc = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    proc.wait()


def showkbd(keyboard, img=None, label="A Keyboard"):
    if not img:
        img = hashlib.md5(str(keyboard).encode('utf-8')).hexdigest()
        img = "/tmp/{}".format(img)
    img_file = "{}.png".format(img)
    if not Path(img_file).is_file():
        display(Image(filename=kbd_getX11_image(keyboard, fname=img, label=label)))
    else:
        display(Image(filename=img_file))


def showkbd_side(keyboard1, keyboard2, label = "A Keyboard comparison"):
    img_h1 = hashlib.md5(str(keyboard1).encode('utf-8')).hexdigest()
    img_h2 = hashlib.md5(str(keyboard2).encode('utf-8')).hexdigest()
    img_file1 = "/tmp/{}.png".format(img_h1)
    img_file2 = "/tmp/{}.png".format(img_h2)
    if not Path(img_file1).is_file():
        kbd_getX11_image(keyboard1, fname="/tmp/{}".format(img_h1), label=None)

    if not Path(img_file2).is_file():
        kbd_getX11_image(keyboard1, fname="/tmp/{}".format(img_h2), label=None)

    # cmd="montage -geometry 1600x280 {f1} {f2} -gravity east {out}".format(f1=img_file1,f2=img_file2,out="/tmp/out2.png")
    cmd = "montage -geometry 800x280 {f1} {f2} -gravity east {out}".format(f1=img_file1, f2=img_file2,
                                                                            out="/tmp/out2.png")
    # print(cmd)
    bash_command(cmd)
    display(Image(filename="/tmp/out2.png"))
