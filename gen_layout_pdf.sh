#!/bin/bash

out_file=${1:-layout}

setxkbmap -model thinkpad -layout el -variant basic -print | xkbcomp - - > keyboards/keyboard.xkm 2>/dev/null
xkbprint -label symbols -color keyboards/keyboard.xkm keyboards/${out_file}.ps
convert keyboards/${out_file}.ps -crop 380x720+115+35 -rotate -90 keyboards/${out_file}.png
rm keyboards/keyboard.xkm

# This reset the keyboard to sanity
setxkbmap 'us,gr' -variant ',' -option '' -option 'terminate:ctrl_alt_bksp,grp:alt_shift_toggle,terminate:ctrl_alt_bksp,compose:rctrl'