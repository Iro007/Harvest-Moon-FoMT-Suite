#!/bin/bash

ROM=${ROM-baserom.gba}
BEG=$1
LEN=${2-0x100}

BEG_OFF=$((BEG & 0x1FFFFFF))
END_OFF=$((BEG_OFF + LEN))

arm-none-eabi-objdump -b binary -D --start-address=$BEG_OFF --stop-address=$END_OFF "$ROM" -marmv4t -Mforce-thumb
