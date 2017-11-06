#!/bin/bash

DISPLAY=${DISPLAY:-:0}
out_file=${1:-layout}
rulesFile=${out_file}.kmap

rm -f ${out_file}.png ${out_file}.ps

xmodmap ${rulesFile}
xkbprint $DISPLAY -label symbols -o ${out_file}.ps
if [ -f ${out_file}.ps ] ; then
    gs -r300 -dTextAlphaBits=4 -sDEVICE=png16m -sOutputFile=${out_file}.png -dBATCH -dNOPAUSE ${out_file}.ps >/dev/null
    convert ${out_file}.png  +repage  -rotate -90 -crop 2000x700+260+1020 -resize 800x280 -size 800x280 +repage ${out_file}.png
    montage -label "${2}" ${out_file}.png -geometry +0+0 -background Khaki ${out_file}.png
fi
rm -f ${out_file}.ps $rulesFile

# This reset the keyboard to sanity
setxkbmap 'us,gr' -variant ',' -option '' -option 'terminate:ctrl_alt_bksp,grp:alt_shift_toggle,terminate:ctrl_alt_bksp,compose:rctrl'