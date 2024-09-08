#!/bin/sh
controlfolder="/mnt/SDCARD/Apps/aROMa"
source /mnt/SDCARD/System/etc/ex_config
exec > >(tee "$controlfolder/log.txt") 2>&1
export PYSDL2_DLL_PATH="/usr/trimui/lib"
echo "Starting aROMa."
chmod -R +x .
./init
unset LD_LIBRARY_PATH
