#!/bin/bash

out='docs/layout.pdf'

# The geometry file
# ls /usr/share/X11/xkb/geometry
geometry='thinkpad'

setxkbmap -model ${geometry} -layout el -variant basic -print |
  xkbcomp - - |
  xkbprint -label symbols -color - - |
  ps2pdf - > ${out}

evince ${out} &