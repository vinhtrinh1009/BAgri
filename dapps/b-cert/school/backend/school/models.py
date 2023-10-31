import datetime
import os
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.urls.base import reverse
from model_utils import Choices
import math
# Create your models here.


class University(models.Model):
    university_id = models.CharField(default="", null=False, unique=True, max_length=256)
    university_name = models.CharField(default="", null=False, max_length=256)
    phone = models.CharField(default="", max_length=12)
    address = models.CharField(default="", max_length=200)
    email = models.EmailField('Email address', unique=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    public_key = models.TextField(default="", null=False)
    private_key = models.TextField(default="", null=False)
    description = models.TextField(default="", null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "University: {} - id: {}".format(self.university_name, self.id)


class customUser(AbstractUser):
    email = models.EmailField('Email address', unique=True)
    avatar = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')
    phone = models.CharField(default="", max_length=12)
    address = models.CharField(default="", max_length=60, null=True)
    public_key = models.TextField(default="", null=False)
    private_key = models.TextField(default="", null=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='members')
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return "username: {} - id: {} - {}".format(self.username, self.id, self.public_key)

    def save(self, *args, **kwargs):
        super(customUser, self).save(*args, **kwargs)

        # shrink avatar image if it's too large
        img = Image.open(self.avatar.path)

        if img.height > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def full_name(self):
        return "{} {}".format(self.first_name, self. last_name)


class Student(models.Model):
    user = models.OneToOneField(customUser, on_delete=models.CASCADE, primary_key=True)
    student_id = models.CharField(default="", max_length=16, unique=True)
    blockchain_key = models.CharField(default="", max_length=128, null=True)
    unit = models.CharField(default="", null=True, max_length=128)
    education_form = models.CharField(default="", null=True, max_length=128)
    major = models.CharField(default="", null=True, max_length=128)
    # birth = models.DateField(null=True)

    def __str__(self, *args, **kwargs):
        return "student: {} - unit: {}".format(self.user.username, self.unit)


class Professor(models.Model):
    user = models.OneToOneField(customUser, on_delete=models.CASCADE, primary_key=True)
    professor_id = models.CharField(default="", max_length=16, unique=True)
    blockchain_key = models.CharField(default="", max_length=128, null=True)
    department = models.CharField(default="", null=True, max_length=128)

    def __str__(self, *args, **kwargs):
        return "professor: {} - blockchain_key: {}".format(self.user.username, self.blockchain_key)


class Staff(models.Model):
    user = models.OneToOneField(customUser, on_delete=CASCADE, primary_key=True)
    staff_id = models.CharField(default="", null=True, max_length=16)
    blockchain_key = models.CharField(default="", max_length=128, null=True)

    def __str__(self, *args, **kwargs):
        return "staff: {} ".format(self.user.username)


class Subject(models.Model):
    subject_id = models.CharField(default="", null=True, max_length=10)
    blockchain_key = models.CharField(default="", max_length=128, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name="subjects")
    name = models.CharField(default="", max_length=50)
    credits = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "subject name: {} |   blockchain_key: {}".format(self.name, self.blockchain_key)


class Class(models.Model):
    class_id = models.CharField(default="", unique=True, max_length=16)
    blockchain_key = models.CharField(default="", max_length=128, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='classes')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='classes')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classes')
    timestamp = models.DateTimeField(null=True, blank=True)
    semester = models.CharField(default="", max_length=5)
    status = models.BooleanField(default=True)
    students = models.ManyToManyField(Student, through='Result', related_name='classes')

    def __str__(self):
        return "ID: {}  |  blockchain_key: {}".format(self.class_id, self.blockchain_key)


class Result(models.Model):
    result_id = models.CharField(default="", max_length=128, null=True)
    blockchain_key = models.CharField(default="", max_length=128, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='results')
    class_detail = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='results')
    middle_score = models.FloatField(default=-1)
    final_score = models.FloatField(default=-1)
    timestamp = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "result_id: {} | middle: {} - final: {}".format(self.result_id,self.middle_score, self.final_score)


class Certificate(models.Model):
    student = models.OneToOneField(Student, default="", on_delete=models.CASCADE, primary_key=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='certificate')
    blockchain_key = models.CharField(default="", max_length=128, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    cpa = models.FloatField(default=0)
    grad_year = models.CharField(default="", null=True, max_length=10)
    certificate_level = models.CharField(default="", null=True, max_length=10)
    register_id = models.CharField(default="", null=True, max_length=128)
    status = models.BooleanField(default=True)

    def __str__(self):
        return "student: {} - certificate_level: {}".format(self.student.user.username, self.certificate_level)

class Transaction(models.Model):
    CREATE = 1
    UPDATE = 2
    NONE = 0

    TRANSACTION_TYPES = (
        (NONE, "none"),
        (CREATE, "create"),
        (UPDATE, "update"),
    )
    transaction_id = models.TextField(default="", null=True)
    transaction_type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPES, null = True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.timestamp)
    
class UniversityTransactions(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "{}".format(self.university.university_name)

class ProfessorTransactions(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "{}".format(self.professor.user.get_full_name())

class StudentTransactions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "{}".format(self.student.user.get_full_name())

class StaffTransactions(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "{}".format(self.staff.user.get_full_name())

class SubjectTransactions(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return '{}'.format(self.subject.name)

class ClassTransactions(models.Model):
    class_detail = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "{}".format(self.class_detail.class_id)

class ResultTransactions(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "id_db:{} class {} - student {}  ".format(self.id, self.result.class_detail.class_id, self.result.student.student_id)

class CertificateTransactions(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name='transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return "{} - {}".format(self.certificate.university.university_name, self.certificate.student.student_id)


class ShareCertificateToken(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name="share_certi")
    token = models.CharField(default="", unique=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

