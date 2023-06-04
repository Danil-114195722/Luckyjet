#!/bin/bash


py=$(which python3)
cur_dir=$(pwd)

$py $cur_dir/utils/schedulers/schedule.py &
$py $cur_dir/utils/schedulers/schedule_after_term.py &
