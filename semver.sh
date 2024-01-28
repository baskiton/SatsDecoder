#!/bin/bash

V0=$(git describe --tags --long --match="[0-9].[0-9].[0-9]" | sed -n 's/v\?\([0-9\.]*\)-\([0-9]*\)-.*/\1.\2/p')
IFS='.' read -d "" -ra arr0 <<< $V0
V=${arr0[0]}.${arr0[1]}.$((arr0[2] + arr0[3]))
echo "__version__ = '$V'" > SatsDecoder/version.py
echo $V
