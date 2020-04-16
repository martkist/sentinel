#!/bin/sh
env | grep SENTINEL_RPCHOST >> /etc/environment
cron -f
