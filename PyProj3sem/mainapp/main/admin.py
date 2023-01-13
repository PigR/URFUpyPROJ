from django.contrib import admin
from .models import ContentAbout, Charts, TableSalaryYear, TablesVacanciesYears, TableVacanciesInCityYear, TableSkillsInYear
# Register your models here.


class TablesSalaryYearAdmin(admin.ModelAdmin):
    list_display = ("currency", "year", "salary")


class TablesVacanciesYearsAdmin(admin.ModelAdmin):
    list_display = ("year", "vacanсies")


class TableVacanciesInCityYearAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "salary")


class TableSkillsInYearAdmin(admin.ModelAdmin):
    list_display = ("year", "title", "counter")


admin.site.register(ContentAbout)
admin.site.register(Charts)
admin.site.register(TableSalaryYear, TablesSalaryYearAdmin)
admin.site.register(TablesVacanciesYears, TablesVacanciesYearsAdmin)
admin.site.register(TableVacanciesInCityYear, TableVacanciesInCityYearAdmin)
admin.site.register(TableSkillsInYear, TableSkillsInYearAdmin)