#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Thu Feb 28 17:21:40 2019
# Author: January

import os
import sys
import re
from LinKit_lib import options as op

usage = '''[USAGE] create_entry <name> [-s <start_cmd>] [-i <icon_path>] [-t <type>] [-T <is_in_terminal>]
[NOTICE] <is_in_terminal> can only be true or false'''
tag = 'Generated by code'
desktop_entry_template='''# {tag}
[Desktop Entry]
Type={type}
Name={name}
Icon={icon}
Exec={exec}
Terminal={terminal}
'''

default={
    'name':'',
    'icon':'',
    'exec':'',
    'type':'Application',
    'terminal':'false'
}

options_map={
    'type':'t',
    'terminal':'T',
    'exec': 's',
    'icon':'i'
}

def get_options():
    options = dict()
    option_name = ''
    no_name_options_count = 0
    waiting_for_value = False
    for item in sys.argv[1:]:
        if(item.startswith('-')):
            option_name = item
            waiting_for_value = True
            options[option_name] = ''
        else:
            if waiting_for_value is True:
                options[option_name] = item
            else:
                options[no_name_options_count] = item
                no_name_options_count = no_name_options_count + 1
    # debug info
    # print(sys.argv)
    return options

# 把命令中的路径转换为绝对路径
def abs_exec_path(exec):
    part_exec = re.split(' ', exec, 1)
    if len(part_exec) == 1:
        cmd = part_exec[0]
        arg = ''
    else:
        cmd, arg = part_exec

    # 如果不是相对路径指定的可执行文件则不做转换
    if os.path.exists(cmd):
        cmd = os.path.abspath(cmd)
    else:
        print("warning: start-command is not a valid path")

    return cmd + ' ' + arg
    

def main():
    raw_args, input_options = op.get_options_v2(sys.argv, ['h','s:', 'i:', 't:', 'T:'])
    result_options = dict()
    if 'h' in input_options.keys() or len(raw_args) <= 0:
        print(usage)
        return
    if len(raw_args) > 1:
        print("warning: more than one filename are specified, but only the first will be used")

    result_options['name'] = raw_args[0]
    for option in options_map.keys():
        option_cmd_name = options_map[option]
        if option_cmd_name in input_options.keys():
            result_options[option] = input_options[option_cmd_name]
        else:
            result_options[option] = default[option]
    
    # python3中， dict的has_key方法已被弃用
    if 'i' in input_options.keys():
        if os.path.exists(result_options['icon']) is False:
            print('warning: the icon doesn\'t exist')
        # icon路径转换成绝对路径
        else:
            result_options['icon'] = os.path.abspath(result_options['icon'])

    # 执行命令中的路路径转换为绝对路径
    result_options['exec'] = abs_exec_path(result_options['exec'])

    out_put_content = desktop_entry_template.format(
        tag=tag,
        type=result_options['type'],
        name=result_options['name'],
        icon=result_options['icon'],
        exec=result_options['exec'],
        terminal=result_options['terminal']
    )

    part_filename = result_options['name'].replace(' ', '_')
    filename = part_filename  + '.desktop'
    if os.path.exists(filename):
        choice = input("'%s already' exists, overwrite it?(y/n):"%(filename))
        if choice != 'y':
            print("aborted")
            exit(1)
    desktop_entry_file = open(filename, 'w')
    desktop_entry_file.write(out_put_content)

if __name__ == '__main__':
    main()

    




