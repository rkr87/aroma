#!/bin/sh
controlfolder="/mnt/SDCARD/Apps/aroma"
source /mnt/SDCARD/System/etc/ex_config
exec > >(tee "$controlfolder/log.txt") 2>&1
export PYSDL2_DLL_PATH="/usr/trimui/lib"
echo "Starting aROMa."
chmod -R +x .
./sdl2imgshow -z "./splash.ini" &
sleep 0.5
pkill -f sdl2imgshow
./init
unset LD_LIBRARY_PATH