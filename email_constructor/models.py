#-*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Template(models.Model):
	class Meta:
		db_table = 'Templates'
		verbose_name = 'Шаблон'
		verbose_name_plural = 'Шаблоны'

	template_name = models.CharField(verbose_name='Название', max_length=50)
	template_html = models.TextField(verbose_name='Шаблон')

	def __unicode__(self):
		return self.template_name