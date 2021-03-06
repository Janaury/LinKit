#!/bin/bash
# Date: Sun Sep  8 10:22:41 2019
# Author: January
set -o errexit

start_script_dir="$HOME/.start"
start_log_name="start.log"
profile_path="$HOME/.profile"

# 加入profile中用于执行脚本
run_start_script=$(cat << eof
############################################
#                                          #
# run startup script in $start_script_dir  #
#     code generated by january            #
#                                          #
############################################
if [ -z \$JAN_STARTED ] && [ -d "$start_script_dir" ]; then
    dir="$start_script_dir"
    for script in \$(ls \$dir)
    do
        if [ -x "\$dir/\$script" ]; then
            time=\$(date +%Y-%m-%d_%H:%M:%S)
            \$dir/\$script
            if [ \$? -eq 0 ]; then
                echo "\$time \$script ok" >> $start_script_dir/$start_log_name
            else
                echo "\$time \$script failed to start" >> $start_script_dir/$start_log_name
            fi
        fi
    done
    export JAN_STATED="started"
fi
############### end of code ##################
eof
)

if [ -d $start_script_dir ]; then
    echo "directory $start_script_dir already exists, add -f and try again"
    # 字符串比较时最好都加上引号，避免特殊符号引起的问题
    if [ "$1" != "-f" ]; then
        echo "aborting..."
        exit -1
    else
        echo "use existing diretory $start_script_dir"
    fi
else
    mkdir $start_script_dir
fi

already_put_script=$(cat $profile_path | grep "code generated by january") || true
if [ -z "$already_put_script" ]; then
    echo "puting script into $profile_path..."
    # 使用双引号包围变量可已让echo输出变量中的换行符, 使用-e选项让echo把\n解析为换行符
    echo -e "$run_start_script" >> $profile_path
else
    echo "script has already been added, no need to do again"
fi

echo "ok"
echo "Now, you can put the scripts you want to run when staring
into $start_script_dir and they will be executed automatically 
everytime you log into your computer. "
