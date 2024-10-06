#!/bin/sh
controlfolder="/mnt/SDCARD/Apps/aroma"
source /mnt/SDCARD/System/etc/ex_config
exec > >(tee "./log.txt") 2>&1
"$controlfolder/bin/sdl2imgshow" -z "./splash.ini" &
export PYSDL2_DLL_PATH="/usr/trimui/lib"
echo "aROMa - Refreshing Roms."
cd $controlfolder
chmod -R +x .
./init --refresh
unset LD_LIBRARY_PATH
pkill -f sdl2imgshow