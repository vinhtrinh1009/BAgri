import os
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, related
# Create your models here.


class TokenShared(models.Model):
    token = models.CharField(default="", max_length=200)


# class Certificate(models.Model):
#     student_name = models.CharField(default="", max_length=50)
#     birth = models.DateField()
#     gender = models.CharField(default="Unknown", max_length=10)
#     university = models.CharField(default="", max_length=70)
#     faculty = models.CharField(default="", max_length=70)
#     degree = models.CharField(default="", max_length=20)
#     gradyear = models.DateField()  # năm tốt nghiệp
#     level = models.CharField(default="", max_length=20)  # xếp loại
#     eduform = models.CharField(default="", max_length=50)  # hình thức đào tạo
#     issuelocation = models.CharField(default="", max_length=70)  # nơi cấp
#     issuedate = models.DateField()  # ngày cấp
#     headmaster = models.CharField(default="", max_length=50)  # hiệu trưởng
#     globalregisno = models.CharField(default="", max_length=50)  # số hiêu vào sổ


# class SubjectScore(models.Model):
#     semester = models.CharField(default="", max_length=10)
#     subjectId = models.CharField(default="", max_length=10)
#     subjectName = models.CharField(default="", max_length=100)
#     credit = models.IntegerField(default=0)
#     halfSemesterPoint = models.FloatField(default=0)
#     finalSemesterPoint = models.FloatField(default=0)
#     teacherId = models.CharField(default="", max_length=10)
#     teacherName = models.CharField(default="", max_length=50)
#     txid = models.CharField(default="", max_length=500)
#     isIntegrity = models.BooleanField()
