#!/bin/sh
aroma_dir="/mnt/SDCARD/Apps/aroma"
source /mnt/SDCARD/System/etc/ex_config
PATH="/mnt/SDCARD/System/usr/trimui/scripts:$PATH"

rom_file=$1
launch_script=$2

line_count=0
extension="${rom_file##*.}"
if [ "$extension" = "txt" ]; then
    while IFS= read -r line; do
        [ -n "$line" ] && [ "$line" != " " ] && line_count=$((line_count + 1))
    done < "$rom_file"
fi

button_state.sh R
if [ $? -eq 10 ] || [ "$line_count" -gt 1 ]; then
    "$aroma_dir/bin/sdl2imgshow" -z "$aroma_dir/resources/ui/splash.ini" &
    sleep 0.5
    pkill -f sdl2imgshow
    export PYSDL2_DLL_PATH="/usr/trimui/lib"
    cd $aroma_dir
    chmod -R +x .
    out=$(./init --launch "$1")
    result="${out#*"AROMA LAUNCH RESULT: "}"
    launch_script=$(echo "$result" | jq -r '.launch')
    rom_file=$(echo "$result" | jq -r '.rom')
else
    [ -f "$launch_script" ] && exit 1
    [ "$extension" = "txt" ] && rom_file=$(head -n 1 "$rom_file")
    rel_path="${rom_file#"/mnt/SDCARD/Roms/"}"
    system="${rel_path%%/*}"
    emu_config="/mnt/SDCARD/Emus/$system/config.json"
    launcher=$(jq -r '.launch' "$emu_config")
    launch_script="/mnt/SDCARD/Emus/$system/$launcher"
fi

[ -f "$rom_file" ] && [ -f "$launch_script" ] && "$launch_script" "$rom_file"
