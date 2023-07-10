#!/bin/bash
cat /root/cronset >> /etc/crontab
service cron stop
service cron start
