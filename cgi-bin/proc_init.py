#coding=UTF-8
#---------------------------------------------------------------------
# Copyright (c) 2013 zihuacs, Inc. All Rights Reserved
#
# @date 2013-01-15, 20:47:00 
# @file proc_init.py
# @author zihuacs(zihuacs@qq.com)
# @brief 初始化 
#--------------------------------------------------------------------- 

import sys
import os

def proc_init():
    project_dir = os.path.abspath('D:\GitHub\search_vs')
    sys.path.append(project_dir)
    py_dir = project_dir + os.path.sep + 'conf' + os.path.sep
    sys.path.append(py_dir)
    py_dir = project_dir + os.path.sep + 'cgi-bin' + os.path.sep
    sys.path.append(py_dir)
