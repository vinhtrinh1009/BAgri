from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'subject_id')
    pass

@admin.register(customUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'first_name', 'last_name')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')

# @admin.register(TeamRole)
# class TeamRoleAdmin(admin.ModelAdmin):
#     pass

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'university')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'class_detail')
    pass

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'university')
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')
    pass

@admin.register(UniversityTransactions)
class UniversityTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(StaffTransactions)
class StaffTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(ProfessorTransactions)
class ProfessorTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(StudentTransactions)
class StudentTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(SubjectTransactions)
class SubjectTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(ClassTransactions)
class ClassTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(ResultTransactions)
class ResultTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(CertificateTransactions)
class CertificateTransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass

@admin.register(ShareCertificateToken)
class ShareCertificateTokenAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    pass