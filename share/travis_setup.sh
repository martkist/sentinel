#!/bin/bash
set -evx

mkdir ~/.martkistcore

# safety check
if [ ! -f ~/.martkistcore/.martkist.conf ]; then
  cp share/martkist.conf.example ~/.martkistcore/martkist.conf
fi
