#-*- coding:utf8 -*-
import xlrd
import os
from HR_project.settings import BASE_DIR
file_location =  os.path.join(BASE_DIR,'utils/parsing/candidates.xls')
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
sheet.cell_value(0,0) == u'№'
