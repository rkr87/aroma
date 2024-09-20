#!/bin/sh
controlfolder="/mnt/SDCARD/Apps/aROMa"
source /mnt/SDCARD/System/etc/ex_config
exec > >(tee "./log.txt") 2>&1
export PYSDL2_DLL_PATH="/usr/trimui/lib"
echo "aROMa - Refreshing Roms."
cd $controlfolder
chmod -R +x .
./init --refresh
unset LD_LIBRARY_PATH
