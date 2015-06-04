#-*- coding:utf8 -*-
import xlrd
import os
from HR_project.settings import BASE_DIR
from applicants.models import Applicant,Phone
from events.models import Event


class ApplicantInfo(object):
    def __init__(self):
        self.applicant = Applicant()
        self.phone = ""
        self.interviews = []

    def __unicode__(self):
        return self.applicant.first_name + self.applicant.last_name

    def save(self):
        self.applicant.save()
        Phone.objects.create(phone = self.phone,applicant=self.applicant)



def nameConverter(name,applicant_info):
    first_name, last_name,middle_name = name.strip().split()
    applicant_info.applicant.first_name = first_name
    applicant_info.applicant.last_name = last_name
    applicant_info.applicant.middle_name = middle_name

def phoneConverter(phone,applicant_info):
    applicant_info.phone = int(phone)

def emailConverter(email,applicant_info):
    applicant_info.applicant.email = email

def interviewConverter():
    pass


#словарь, сопостовляющий заголовок поля и функцию-конвертер, которую необходимо применить к данному полю для его добавления в качестве атрибута объекта класса Кандидат
matcher = {u'ФИО':nameConverter,u'Телефон':phoneConverter,u'Email':emailConverter,
           u'1-е соб-е (дата)':interviewConverter, u'2-е соб-е (дата)':interviewConverter}




file_location =  os.path.join(BASE_DIR,'utils/parsing/candidates.xls')
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

applicants_info_list = []

#создаём список с индексами валидных стобцов
valid_columns = []
for col in xrange(sheet.ncols):
     if sheet.cell_value(0,col) in matcher:
         valid_columns.append(col)


for row in xrange(1,sheet.nrows ):
    applicant_info = ApplicantInfo()
    for col in valid_columns:
        #если значение в ячейке не пусто, то конвертируем значение в необходимый формат и сохраняем в виде атрибута объекта класса Кандидат
        if sheet.cell_value(row,col) != u"":
            matcher[sheet.cell_value(0,col)](sheet.cell_value(row,col),applicant_info)
    applicants_info_list.append(applicant_info)


