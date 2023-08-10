#!/bin/bash

set -x
set -e

export LC_ALL=C

sudo systemctl enable pioreactor_startup_run@logs2slack.service
