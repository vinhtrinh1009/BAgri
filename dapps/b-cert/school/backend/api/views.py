from tracemalloc import Statistic
from django.urls.exceptions import NoReverseMatch
from school.models import University, Staff, Student, Professor, Subject, Class, Result, Certificate, Transaction, UniversityTransactions, SubjectTransactions, StaffTransactions, ProfessorTransactions, StudentTransactions, ClassTransactions, ResultTransactions, CertificateTransactions, customUser
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from requests.api import get, put
from rest_framework import status, generics
from rest_framework.response import Response
from datetime import timedelta, datetime, time, timezone, tzinfo
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user, get_user_model
from django.urls import reverse
from django.utils.dateparse import parse_date, parse_datetime
from .serializers import *
import requests
import json
import jwt
from bcertsdk.handler import Handler
from bcertsdk.errors import CommunicationError, InternalError
from django.utils.timezone import now, utc
from .utils import generate_key_pair, read_file
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
# from backend.models import *

# Create your views here.

###
# University API 
###

class UniversityAPIView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user')
        if not user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(get_user_model(), id=user_id)
        university = user.university
        serializer = UniversitySerializer(university, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UniversityDetailsAPIView(APIView):
    def get(self, request, pk, format=None):
        university = get_object_or_404(University, id=pk)
        serializer = UniversitySerializer(university, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUniversityAPIView(APIView):
    handler = Handler()
    def post(self, request, format=None):
        # university_id = request.data.get('university', None)
        user_id = request.data.get('user')
        if not user_id:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(get_user_model(), id=user_id)
        if user.university:
            return Response({'detail': 'University have been registed!'}, status=status.HTTP_400_BAD_REQUEST)

        university_name = request.data.get('name')
        university_id = request.data.get('university_id')
        phone = request.data.get('phone')
        address = request.data.get('address')
        email = request.data.get('email')
        timestamp = request.data.get('timestamp')
        description = request.data.get('description')

        if not university_name or not phone or not address or not email:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)

        if not timestamp:
            timestamp = now().replace(tzinfo=utc)
        
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        public_key, private_key = self.handler.gen_key_pair()
        university = University.objects.create(university_id = university_id,
                                                university_name=university_name, 
                                                phone=phone, 
                                                email=email, 
                                                address=address, 
                                                timestamp=timestamp, 
                                                private_key=private_key, 
                                                public_key=public_key, 
                                                description=description)
        serializer = UniversitySerializer(university)
        user.university = university
        user.is_staff = True
        user.save()
        staff_id = str(university.university_id)+"-"+str(user.id)
        staff = Staff.objects.create(user=user, staff_id=staff_id, blockchain_key=staff_id)
        
        staff_list = [staff_id, '']
    
        uni_response = self.handler.create_university(att_university_id=str(university.university_id), 
                                                    att_university_name=university.university_name, 
                                                    att_email = university.email,
                                                    att_phone = university.phone, 
                                                    att_address=university.address,
                                                    # timestampp = str_timestamp,
                                                    att_status = str(university.status),
                                                    att_public_key = university.public_key,
                                                    for_staff_staff_ids = staff_list,
                                                    for_professor_profess_ids=[''],
                                                    for_student_student_ids=[''],
                                                    for_certificate_certi_ids=[''],
                                                    for_subject_subject_ids=[''],                                    
                                                    private_key = university.private_key)
        
        uni_transaction = Transaction.objects.create(transaction_id=uni_response['data']['txid'],
                                                        transaction_type = Transaction.CREATE,
                                                        timestamp = timestamp)
        UniversityTransactions.objects.create(transaction=uni_transaction, university=university)

        staff_response = self.handler.create_staff(att_staff_id=str(staff.staff_id),
                                                att_name = user.get_full_name(),
                                                att_email = user.email,
                                                att_phone = user.phone,
                                                att_address = user.address,
                                                # timestampp = str_timestamp,
                                                att_status = str(user.is_active),
                                                att_public_key = public_key,
                                                for_university_university_id=str(university.university_id),
                                                private_key = private_key)
        
        staff_transaction = Transaction.objects.create(transaction_id = staff_response['data']['txid'],
                                                        transaction_type = Transaction.CREATE,
                                                        timestamp = timestamp)
        StaffTransactions.objects.create(transaction=staff_transaction, staff=staff)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUniversityAPIView(APIView):
    handler = Handler()
    def patch(self, request, pk, format=None):
        user_id = request.data.get('user')
        if not user_id:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(get_user_model(), id=user_id)
        if not user.is_staff:
            return Response({'detail': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        university = get_object_or_404(University, id=pk)
        data = request.data.get('profile')
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        serializer = UniversitySerializer(university, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            updated_university = get_object_or_404(University, id=pk)
            try: 
                uni_bkc = self.handler.get_university(att_university_id=str(university.university_id))['data']['university']
                response = self.handler.update_university(att_university_id=str(updated_university.university_id), 
                                                        att_university_name=updated_university.university_name, 
                                                        att_email = updated_university.email,
                                                        att_phone = updated_university.phone, 
                                                        att_address=updated_university.address,
                                                        # timestampp = str_timestamp,
                                                        att_status = str(updated_university.status),
                                                        att_public_key = updated_university.public_key,
                                                        private_key = updated_university.private_key,
                                                        for_professor_profess_ids=uni_bkc['professor_profess_ids'],
                                                        for_student_student_ids=uni_bkc['student_student_ids'],
                                                        for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                        for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                        for_subject_subject_ids=uni_bkc['subject_subject_ids']
                                                        )
                
                update_uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],
                                                                    transaction_type=Transaction.CREATE,
                                                                    timestamp = timestamp)
                
                UniversityTransactions.objects.create(transaction=update_uni_transaction,
                                                        university=university)
                return Response(status=status.HTTP_200_OK)
            
            except InternalError as erri:
                return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
            except CommunicationError as errc:
                return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class GetUniversityBkAPIView(APIView):
    handler = Handler()
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        
        try: 
            uni_response = self.handler.get_university(str(university_id))
            return Response(uni_response['data']['university'], status = status.HTTP_200_OK)
        except InternalError as erri:
                return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

###

###
# Subject API
###

class SubjectAPIView(APIView):
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        if not university_id:
            return Response({'detail': 'missing query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        university = get_object_or_404(University, id=university_id)
        subjects = Subject.objects.filter(university=university)

        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateSubjectAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    handler = Handler()

    def post(self, request, format=None):
        # Handle file uploaded will be added in util.py
        # Blockchain communication will be added after we had sdk

        university_id = request.data.get('university', None)
        if not university_id:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)

        university = get_object_or_404(University, id=university_id)
        excel_file = request.FILES['excel-file']
        if not excel_file:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)
        excel_data = read_file(excel_file)
        timestamp = now().replace(tzinfo=utc)
        return_data = []
        for e_id, e_info in excel_data.items():
            subject_id = e_info['subject id']
            subject_name = e_info['name']
            credits = e_info['credits']
            timestamp = now().replace(tzinfo=utc)
            blockchain_key = str(university.university_id)+"-"+str(subject_id)
            try:
                Subject.objects.get(subject_id=subject_id)
                continue
            except Subject.DoesNotExist:
                subject = Subject.objects.create(subject_id=subject_id,name=subject_name,credits=credits,timestamp=timestamp,university=university,blockchain_key=blockchain_key)
                return_data.append(subject)
                print("create new subject on database {}".format(subject_id))
                try:
                    response = self.handler.create_subject(att_subject_id=subject.blockchain_key,
                                                            att_subject_name=subject.name,
                                                            att_credit=str(subject.credits),
                                                            att_status = str(subject.status),
                                                            for_classroom_class_ids=[''],
                                                            for_university_university_id=str(subject.university.university_id),
                                                            private_key=university.private_key)
                except Exception as error:
                    print(error)
                    return Response({'error': 'Create subject fail on blockchain by id: {}'.format(subject_id)}, status=status.HTTP_400_BAD_REQUEST)

                subj_trans = Transaction.objects.create(transaction_id = response['data']['txid'],transaction_type = Transaction.CREATE,timestamp=timestamp)
                SubjectTransactions.objects.create(transaction = subj_trans,subject=subject)
                
        try:
            uni_bkc = self.handler.get_university(str(university.university_id))['data']['university']
            new_subject_list = Subject.objects.filter(university=university).values_list('blockchain_key', flat=True)
            response = self.handler.update_university(att_university_id=uni_bkc['university_id'],
                                                        att_university_name = uni_bkc['university_name'],
                                                        att_email = uni_bkc['email'],
                                                        att_phone = uni_bkc['phone'],
                                                        att_address=uni_bkc['address'],
                                                        att_status=uni_bkc['status'],
                                                        att_public_key=uni_bkc['public_key'],
                                                        for_professor_profess_ids=uni_bkc['professor_profess_ids'],
                                                        for_student_student_ids=uni_bkc['student_student_ids'],
                                                        for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                        for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                        for_subject_subject_ids=new_subject_list,
                                                        private_key = university.private_key)
            
            uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],transaction_type = Transaction.UPDATE,timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,university = university)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class SubjectDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        subject = get_object_or_404(Subject, id=pk)
        serializer = SubjectDetailSerializer(subject)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        subject = get_object_or_404(Subject, id=pk)
        serializer = SubjectDetailSerializer(Subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FixSubjectOnBKAPIView(APIView):
    handler=Handler()
    def get(self, request, format=None):
        subject_id = request.query_params.get('subject')
        # university_id = request.query_params.get('university')
        # university = get_object_or_404(University, id=university_id)
        timestamp = now().replace(tzinfo=utc)
        # str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        subject = Subject.objects.get(subject_id=subject_id)
        serializer = SubjectSerializer(subject)
        university = subject.university
        subject_class = Class.objects.filter(subject__subject_id=subject_id).values_list('blockchain_key', flat=True)
        # class_serializer = ClassSerializer(subject_class, many=True)
        try:
            # subject_id = subject_to_update[i]
            subject_bk = self.handler.get_subject(subject.blockchain_key)['data']['subject']
            subject_res = self.handler.update_subject(att_subject_id=subject.blockchain_key,
                                                    att_subject_name=subject_bk['subject_name'],
                                                    att_credit=str(subject_bk['credit']),
                                                    # timestampp=subject_bk['timestampp'],
                                                    att_status=subject_bk['status'],
                                                    for_classroom_class_ids=subject_class,
                                                    for_university_university_id= str(university.university_id),
                                                    private_key=university.private_key)

            subject_transaction = Transaction.objects.create(transaction_id=subject_res['data']['txid'],
                                                            transaction_type=Transaction.UPDATE,
                                                            timestamp = timestamp)
            
            SubjectTransactions.objects.create(transaction=subject_transaction,
                                                subject=subject)

        except InternalError as erri:
            # continue
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            # continue
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uni_bkc = self.handler.get_university(str(university.university_id))['data']['university']
            subject_list = Subject.objects.filter(university=university).values_list('blockchain_key', flat=True)
            response = self.handler.update_university(att_university_id=uni_bkc['university_id'],
                                                        att_university_name = uni_bkc['university_name'],
                                                        att_email = uni_bkc['email'],
                                                        att_phone = uni_bkc['phone'],
                                                        att_address=uni_bkc['address'],
                                                        # timestampp=uni_bkc['timestampp'],
                                                        att_status=uni_bkc['status'],
                                                        att_public_key=uni_bkc['public_key'],
                                                        for_professor_profess_ids=uni_bkc['professor_profess_ids'],
                                                        for_student_student_ids=uni_bkc['student_student_ids'],
                                                        for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                        for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                        for_subject_subject_ids=subject_list,
                                                        private_key = university.private_key)
            
            uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],
                                                            transaction_type = Transaction.UPDATE,
                                                            timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,
                                                    university = university)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(subject_class, status=status.HTTP_200_OK)

# class SubjectAddBkKeyAPIView(APIView):
#     def get(self, request, format=None):
#         subjects = Subject.objects.all()
#         for subject in subjects:
#             subject.blockchain_key = subject.subject_id
#             subject.save()
        
#         return Response(status=status.HTTP_200_OK)

# class StudentAddBkKeyAPIView(APIView):
#     def get(self, request, format=None):
#         students = Student.objects.all()
#         for student in students:
#             student.blockchain_key = student.student_id
#             student.save()
        
#         return Response(status=status.HTTP_200_OK)
###

###
# Class API
###

class ClassesAPIView(APIView):
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        prof_user_id = request.query_params.get('professor')

        if university_id and not prof_user_id:
            university = get_object_or_404(University, id=university_id)
            classes = university.classes
            serializer = ClassSerializer(classes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if not university_id and prof_user_id:
            user = get_object_or_404(get_user_model(), id=prof_user_id)
            professor = get_object_or_404(Professor, user=user)
            classes = professor.classes
            serializer = ClassSerializer(classes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if (university_id and prof_user_id):
            university = get_object_or_404(University, id=university_id)
            user = get_object_or_404(get_user_model(), id=prof_user_id)
            professor = get_object_or_404(Professor, user=user)
            classes = Class.objects.filter(university=university, professor=professor)
            serializer = ClassSerializer(classes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class CreateClassAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    handler = Handler()

    def post(self, request, format=None):
        # this will create a class and create corresponding result from file uploaded
        # result will not be created directly but only through classes.

        university_id = request.data.get('university', None)
        if not university_id:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)
        university = get_object_or_404(University, id=university_id)

        excel_file = request.data.get('excel-file')
        excel_data = read_file(excel_file)
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        professor_to_update = ['']
        subject_to_update = ['']
        student_to_update = ['']
        

        for e_id, e_info in excel_data.items():
            class_id = e_info['class id']
            try:
                class_detail = Class.objects.get(class_id = class_id)
                continue
            except Class.DoesNotExist:
                professor_id = e_info['professor id']
                subject_id = e_info['subject id']
                semester = e_info['semester']
                
                try:
                    professor = Professor.objects.get(professor_id=professor_id)
                    if professor.professor_id not in professor_to_update:
                        professor_to_update.append(professor.professor_id)
                    subject = Subject.objects.get(subject_id=subject_id)
                    if subject.subject_id not in subject_to_update:
                        subject_to_update.append(subject.subject_id)
                    blockchain_key = str(university.university_id)+"-"+str(class_id)
                    class_detail = Class.objects.create(class_id=class_id, blockchain_key=blockchain_key, university=university, subject=subject, professor=professor,timestamp=timestamp,semester=semester)
                    print("Create new class on database id: {}".format(class_id))
                except Professor.DoesNotExist:
                    professor = None
                    continue
                except Subject.DoesNotExist:
                    subject = None
                    continue
                result_to_update = ['']
                student_ids = e_info['student list'].split(',')
                for student_id in student_ids:
                    try:
                        student_id = student_id.strip()
                        student = Student.objects.get(student_id=student_id)
                        timestamp = now().replace(tzinfo=utc)
                        result_id = str(university.university_id)+"-"+str(class_detail.class_id)+"-"+student_id
                        blockchain_key = result_id
                        result = Result.objects.create(result_id=result_id, blockchain_key=blockchain_key,student=student, class_detail=class_detail, status=True, timestamp=timestamp)

                        if student.student_id not in student_to_update:
                            student_to_update.append(student.student_id)
                        
                        result_to_update.append(result.result_id)
                        try:
                            result_response = self.handler.create_result(att_result_id=result.result_id,
                                                                        att_middlescore=str(result.middle_score),
                                                                        att_finallscore=str(result.final_score),
                                                                        for_classroom_class_id=result.class_detail.blockchain_key,
                                                                        for_student_student_id=result.student.blockchain_key,
                                                                        private_key=university.private_key)
                        except Exception as error:
                            print(error)
                            return Response({"error":"create new result for studen in class fail!"},status=status.HTTP_400_BAD_REQUEST)

                        result_transaction = Transaction.objects.create(transaction_id=result_response['data']['txid'],transaction_type=Transaction.CREATE,timestamp=timestamp)
                        ResultTransactions.objects.create(transaction=result_transaction,result=result)
                    except Student.DoesNotExist:
                        student = None
                try:
                    cls_res = self.handler.create_classroom(att_class_id=class_detail.blockchain_key,
                                                            att_semester=str(class_detail.semester),
                                                            att_status=str(class_detail.status),
                                                            for_result_result_ids=result_to_update,
                                                            for_subject_subject_id=str(class_detail.subject.blockchain_key),
                                                            for_professor_profess_id=str(class_detail.professor.blockchain_key),
                                                            private_key=university.private_key)
                except Exception as error:
                    print(error)
                    return Response({'error':"Create class fail on blockchain by class id: {}".format(class_id)}, status=status.HTTP_400_BAD_REQUEST)

                cls_trans = Transaction.objects.create(transaction_id = cls_res['data']['txid'],transaction_type = Transaction.CREATE,timestamp=timestamp)
                ClassTransactions.objects.create(transaction=cls_trans,class_detail=class_detail)
        for professor_id in professor_to_update:
            try:
                prof = Professor.objects.get(professor_id=professor_id)
                try:
                    # professor_id = professor_to_update[i]
                    prof_bk = self.handler.get_professor(prof.blockchain_key)['data']['professor']
                    prof_class_list = Class.objects.filter(professor__professor_id=professor_id).values_list('blockchain_key', flat=True)
                    prof_res = self.handler.update_professor(att_profess_id=prof.blockchain_key,
                                                            att_name=prof_bk['name'],
                                                            att_email=prof_bk['email'],
                                                            att_phone=prof_bk['phone'],
                                                            att_address=prof_bk['address'],
                                                            att_status=prof_bk['status'],
                                                            att_public_key=prof_bk['public_key'],
                                                            for_classroom_class_ids=prof_class_list,
                                                            for_university_university_id=prof_bk['university_university_id'],
                                                            private_key=university.private_key)

                    prof_transaction = Transaction.objects.create(transaction_id=prof_res['data']['txid'],transaction_type=Transaction.UPDATE,timestamp = timestamp)
                    
                    ProfessorTransactions.objects.create(transaction=prof_transaction,professor=prof)

                except InternalError as erri:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
                except CommunicationError as errc:
                    continue
                    # return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
            except Professor.DoesNotExist:
                continue

        for subject_id in subject_to_update:
            try: 
                subject = Subject.objects.get(subject_id=subject_id)
                try:
                    # subject_id = subject_to_update[i]
                    subject_bk = self.handler.get_subject(subject.blockchain_key)['data']['subject']
                    subject_class_list = Class.objects.filter(subject__subject_id=subject_id).values_list('blockchain_key', flat=True)
                    subject_res = self.handler.update_subject(att_subject_id=subject.blockchain_key,
                                                            att_subject_name=subject_bk['subject_name'],
                                                            att_credit=str(subject_bk['credit']),
                                                            # timestampp=subject_bk['timestampp'],
                                                            att_status=subject_bk['status'],
                                                            for_classroom_class_ids=subject_class_list,
                                                            for_university_university_id=subject_bk['university_university_id'],
                                                            private_key=university.private_key)

                    subject_transaction = Transaction.objects.create(transaction_id=subject_res['data']['txid'],transaction_type=Transaction.UPDATE,timestamp = timestamp)
                    
                    SubjectTransactions.objects.create(transaction=subject_transaction,subject=subject)

                except InternalError as erri:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
                except CommunicationError as errc:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
            except Subject.DoesNotExist:
                continue
            

        for student_id in student_to_update:
            try:
                student = Student.objects.get(student_id = student_id)
            
                try:
                    # student_id = student_to_update[i]
                    stud_bk = self.handler.get_student(student.blockchain_key)['data']['student']
                    stud_res_list = Result.objects.filter(student__student_id=student_id).values_list('result_id', flat=True)

                    stud_res = self.handler.update_student(att_student_id=student.blockchain_key,
                                                            att_name=stud_bk['name'],
                                                            att_email=stud_bk['email'],
                                                            att_phone=stud_bk['phone'],
                                                            att_address=stud_bk['address'],
                                                            att_public_key=stud_bk['public_key'],
                                                            # timestampp=stud_bk['timestampp'],
                                                            for_certificate_certi_ids=stud_bk['certificate_certi_ids'],
                                                            for_university_university_id=stud_bk["university_university_id"],
                                                            for_result_result_ids=stud_res_list,
                                                            private_key=university.private_key)
                    student_data = Student.objects.get(student_id=student_id)

                    stud_transaction = Transaction.objects.create(transaction_id=stud_res['data']['txid'],transaction_type=Transaction.UPDATE,timestamp = timestamp)
                    StudentTransactions.objects.create(transaction=stud_transaction,student=student_data)

                except InternalError as erri:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
                except CommunicationError as errc:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                continue

        return Response(status.HTTP_200_OK)

    def put(self, request, format=None):
        return

class GetBkDataClassAPIView(APIView):
    handler = Handler()
    def get(self, request, format=None):
        class_id = request.query_params.get('class')
        try: 
            response = self.handler.get_classs(class_id)
            return Response(response['data']['classs'], status=status.HTTP_200_OK)
        except InternalError as erri:
                return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)



class AddClassBkAPIView(APIView):
    handler=Handler()
    def get(self, request, format=None):
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        class_id = request.query_params.get('class')
        university_id=request.query_params.get('university')
        university=get_object_or_404(University, id=university_id)
        class_detail = Class.objects.get(class_id = class_id)
        result_to_update=Result.objects.filter(class_detail=class_detail).values_list('result_id', flat=True)
        # str(university.university_id)+"-"+str(subject_id)
        cls_res = self.handler.create_classroom(att_class_id=class_id,
                                                # timestampp=str_timestamp,
                                                att_semester=str(class_detail.semester),
                                                att_status=str(class_detail.status),
                                                for_result_result_ids=result_to_update,
                                                for_subject_subject_id=str(class_detail.subject.blockchain_key),
                                                for_professor_profess_id=str(class_detail.professor.blockchain_key),
                                                private_key=university.private_key)
        cls_trans = Transaction.objects.create(transaction_id = cls_res['data']['txid'],
                                                transaction_type = Transaction.CREATE,
                                                timestamp=timestamp)
        # cls_trans = Transaction.objects.get(id=24)
        ClassTransactions.objects.create(transaction = cls_trans,
                                            class_detail=class_detail)

class FixClassDataBkAPIView(APIView):
    handler=Handler()
    def get(self, request, format=None):
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        class_id = request.query_params.get('class')
        university_id=request.query_params.get('university')
        university=get_object_or_404(University, id=university_id)
        class_detail = Class.objects.get(class_id = class_id)
        result_to_update=Result.objects.filter(class_detail=class_detail).values_list('result_id', flat=True)
       
        professor_id= class_detail.professor.professor_id
        try:
            prof = Professor.objects.get(professor_id=professor_id)
            try:
                # professor_id = professor_to_update[i]
                prof_bk = self.handler.get_professor(prof.blockchain_key)['data']['professor']
                prof_class_list = Class.objects.filter(professor__professor_id=professor_id).values_list('blockchain_key', flat=True)
                prof_res = self.handler.update_professor(att_profess_id=prof.blockchain_key,
                                                        att_name=prof_bk['name'],
                                                        att_email=prof_bk['email'],
                                                        att_phone=prof_bk['phone'],
                                                        att_address=prof_bk['address'],
                                                        # timestampp=prof_bk['timestampp'],
                                                        att_status=prof_bk['status'],
                                                        att_public_key=prof_bk['public_key'],
                                                        for_classroom_class_ids=prof_class_list,
                                                        for_university_university_id=prof_bk['university_university_id'],
                                                        private_key=university.private_key)

                prof_transaction = Transaction.objects.create(transaction_id=prof_res['data']['txid'],
                                                                transaction_type=Transaction.UPDATE,
                                                                timestamp = timestamp)
                
                ProfessorTransactions.objects.create(transaction=prof_transaction,
                                                        professor=prof)

            except InternalError as erri:
                return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
            except CommunicationError as errc:
                return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        except Professor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)        
        
        subject_id = class_detail.subject.subject_id
        subject=class_detail.subject
        try: 
            subject = Subject.objects.get(subject_id=subject_id)
            try:
                # subject_id = subject_to_update[i]
                subject_bk = self.handler.get_subject(subject.blockchain_key)['data']['subject']
                subject_class_list = Class.objects.filter(subject__subject_id=subject_id).values_list('blockchain_key', flat=True)
                subject_res = self.handler.update_subject(att_subject_id=subject.blockchain_key,
                                                        att_subject_name=subject_bk['subject_name'],
                                                        att_credit=str(subject_bk['credit']),
                                                        # timestampp=subject_bk['timestampp'],
                                                        att_status=subject_bk['status'],
                                                        for_classroom_class_ids=subject_class_list,
                                                        for_university_university_id=subject_bk['university_university_id'],
                                                        private_key=university.private_key)

                subject_transaction = Transaction.objects.create(transaction_id=subject_res['data']['txid'],
                                                                transaction_type=Transaction.UPDATE,
                                                                timestamp = timestamp)
                
                SubjectTransactions.objects.create(transaction=subject_transaction,
                                                    subject=subject)

            except InternalError as erri:
               return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
            except CommunicationError as errc:
                return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        except Professor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        student_to_update = Result.objects.filter(class_detail=class_detail).values_list('student__student_id', flat=True)
        for student_id in student_to_update:
            try:
                student = Student.objects.get(student_id = student_id)
            
                try:
                    # student_id = student_to_update[i]
                    stud_bk = self.handler.get_student(student.blockchain_key)['data']['student']
                    stud_res_list = Result.objects.filter(student__student_id=student_id).values_list('result_id', flat=True)

                    stud_res = self.handler.update_student(att_student_id=student.blockchain_key,
                                                            att_name=stud_bk['name'],
                                                            att_email=stud_bk['email'],
                                                            att_phone=stud_bk['phone'],
                                                            att_address=stud_bk['address'],
                                                            att_public_key=stud_bk['public_key'],
                                                            # timestampp=stud_bk['timestampp'],
                                                            for_certificate_certi_ids=stud_bk['certificate_certi_ids'],
                                                            for_university_university_id=stud_bk["university_university_id"],
                                                            for_result_result_ids=stud_res_list,
                                                            private_key=university.private_key)
                    student_data = Student.objects.get(student_id=student_id)

                    stud_transaction = Transaction.objects.create(transaction_id=stud_res['data']['txid'],
                                                                    transaction_type=Transaction.UPDATE,
                                                                    timestamp = timestamp)
                    
                    StudentTransactions.objects.create(transaction=stud_transaction,
                                                            student=student_data)

                except InternalError as erri:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
                except CommunicationError as errc:
                    continue
                    # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                continue
        return Response(status.HTTP_200_OK)

class ClassDetailAPIView(APIView):
    def get(self, request, pk, format=None):

        class_detail = get_object_or_404(Class, id=pk)
        serializer = ClassDetailSerializer(class_detail)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):

        return

###

###
# Result API
###

class ResultsAPIView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user')
        class_id = request.query_params.get('class')
        teacher_id = request.query_params.get('teacher')
        if user_id and not class_id and not teacher_id:         # l?y k?t qu? h?c t?p c?a sinh vi�n
            user = get_object_or_404(get_user_model(), id=user_id)

            if not user.is_student:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            student = Student.objects.filter(user=user).first()
            results = Result.objects.filter(student=student)
            serializer = AllResultsOfStudentSerializer(results, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif class_id and not user_id and not teacher_id:      # l?y danh s�ch sinh vi�n c?a 1 l?p
            class_detail = get_object_or_404(Class, id=class_id)
            results = Result.objects.filter(class_detail=class_detail)
            response_data = []
            for res in results:
                tranx = ResultTransactions.objects.filter(result=res).order_by("-id").first()
                response_data.append(ResultTransactionSerializer(tranx).data)
                # serializer = ResultSerializer(results, many=True)

            # return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(response_data, status=status.HTTP_200_OK)
        elif class_id and user_id:                            # l?y k?t qu? h?c t?p sinh vi�n t?i 1 l?p c? th?
            user = get_object_or_404(get_user_model(), id=user_id)
            class_detail = get_object_or_404(Class, id=class_id)
            if not user.is_student:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            student = Student.objects.filter(user=user).first()
            results = Result.objects.filter(student=student, class_detail=class_detail)
            if len(results) == 0:
                return Response("NO DATA", status=status.HTTP_200_OK)
            serializer = ResultSerializer(results[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif class_id and teacher_id:                       # l?y k?t qu? h?c t?p c?a sinh vi�n do 1 gi�o vi�n d?y
            user = get_object_or_404(get_user_model(), id=teacher_id)
            teacher = Professor.objects.filter(user=user).first()
            class_detail = Class.objects.filter(class_id=class_id, professor=teacher).first()
            if not class_detail:
                return Response("Class does not exist. Or you don't have permission to update this class", status=status.HTTP_400_BAD_REQUEST)

            results = Result.objects.filter(class_detail=class_detail)
            if len(results) == 0:
                return Response("NO DATA", status=status.HTTP_400_BAD_REQUEST)
            serializer = ResultSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'detail': 'missing query parameters'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        return

    def patch(self, request, format=None):
        class_id = request.data.get('class')
        payload = request.data.get('payload')
        if not class_id:
            return Response({'detail': 'missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        class_detail = get_object_or_404(Class, id=class_id)
        class_results = Result.objects.filter(class_detail=class_detail)

        for key, data in payload.items():
            result = get_object_or_404(Result, id=data['id'])
            serializer = ResultSerializer(result, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REUQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResultDetailAPIView(APIView):
    handler = Handler()
    def get(self, request, pk, format=None):
        result = get_object_or_404(Result, id=pk)
        serializer = ResultDetailSerializer(result)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        
        user = request.user
        if not user.is_professor:
            return Response({'detail': 'permission denied'}, status = status.HTTP_401_UNAUTHORIZED)
        
        professor = Professor.objects.get(user=user)
        if not professor:
            return Response({'detail': 'Object not found'}, status = status.HTTP_404_NOT_FOUND)
        
        result = get_object_or_404(Result, id=pk)
        if result.class_detail.professor.professor_id != professor.professor_id:
            return Response({'detail': 'permission denied'}, status = status.HTTP_401_UNAUTHORIZED)
        
        serializer = ResultSerializer(result, data=request.data, partial=True)
        timestamp = now().replace(tzinfo=utc)
        if serializer.is_valid():
            serializer.save()
            updated_result = get_object_or_404(Result, id=pk)
            result_bk = self.handler.get_result(str(result.result_id))['data']['result']
            result_res = self.handler.update_result(att_result_id=result_bk['result_id'],
                                                    att_middlescore=str(serializer.validated_data['middle_score']),
                                                    att_finallscore=str(serializer.validated_data['final_score']),
                                                    # timestampp=result_bk['timestampp'],
                                                    for_classroom_class_id=result_bk['classroom_class_id'],
                                                    for_student_student_id=result_bk['student_student_id'],
                                                    private_key = professor.user.private_key)
            res_transaction = Transaction.objects.create(transaction_id=result_res['data']['txid'],
                                                            transaction_type = Transaction.UPDATE,
                                                            timestamp=timestamp)

            ResultTransactions.objects.create(transaction=res_transaction, result=updated_result)      
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###

###
# Certificate API
###

class CertificatesAPIView(APIView):
    def get(self, request, format=None):
        user_id = request.query_params.get('user')
        university_id = request.query_params.get('university')
        if not user_id and university_id:
            certificate = Certificate.objects.filter(university__id=university_id)
            serializer = CertificateSerializer(certificate, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        user = get_object_or_404(get_user_model(), id=user_id)
        student = Student.objects.filter(user=user).first()
        if not student:
            return Response(status=status.HTTP_404_NOT_FOUND)

        certificate = Certificate.objects.filter(student=student).first()
        if not certificate:
            return Response({'data': "Bạn chưa có bằng cấp nào"},status=status.HTTP_404_NOT_FOUND)

        serializer = CertificateSerializer(certificate)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchCertificateAPIView(APIView):
    def get(self, request, format=None):
        student_id = request.query_params.get('student')
        if not student_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cert = Certificate.objects.filter(student__student_id=student_id).first()
        if not cert:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = CertificateSerializer(cert)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateCertificateAPIView(APIView):
    handler=Handler()
    def patch(self, request, pk, format=None):
        university_id = request.data.get('university')
        action = request.data.get('action')
        if not university_id:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)
        university = get_object_or_404(University, id=university_id)
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%d/%M/%Y, %H:%M:%S")
        certificate = Certificate.objects.get(student__student_id=pk)
        if not certificate:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if action == "revoke":
            certificate.status=False
            certificate.save()
        elif action == "reactive":
            certificate.status=True
            certificate.timestamp = timestamp
            certificate.save()
        try:
            cert_bk = self.handler.get_certificate(certificate.blockchain_key)['data']['certificate']
            cert_res = self.handler.update_certificate(att_certi_id=cert_bk['certificate_id'],
                                                            # timestampp=certificate.timestamp.strftime("%d/%M/%Y, %H:%M:%S"),
                                                            att_cpa = str(cert_bk['cpa']),
                                                            att_type=cert_bk['type'],
                                                            att_status = str(certificate.status),
                                                            for_student_student_id=cert_bk['student_student_id'],
                                                            for_university_university_id=cert_bk['university_university_id'],
                                                            private_key = university.private_key)
            cert_trans = Transaction.objects.create(transaction_id = cert_res['data']['txid'],
                                                    transaction_type = Transaction.UPDATE,
                                                    timestamp = timestamp)
            CertificateTransactions.objects.create(transaction = cert_trans,
                                                    certificate=certificate)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCertificateAPIView(APIView):
    handler=Handler()
    def post(self, request, format=None):
        university_id = request.data.get('university_id')
        if not university_id:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)

        university = get_object_or_404(University, id=university_id)

        excel_file = request.data.get('excel_file')
        if not excel_file:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)
        
        append_cert_list = []
        excel_data = read_file(excel_file)
        timestamp=now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        for e_id, e_info in excel_data.items():
            student_id = e_info['student_id']
            cpa = e_info['cpa']
            certificate_level = e_info['certificate level']
            grad_year = e_info["graduation year"]
            register_id = e_info["register id"]
            blockchain_key = str(university.university_id)+"-"+str(register_id)

            try:
                student = Student.objects.get(student_id=student_id)
                cer_exist = Certificate.objects.filter(student=student)
                id_exist = Certificate.objects.filter(register_id=register_id)
                if not cer_exist and not id_exist:
                    cert = Certificate.objects.create(university=university, student=student, cpa=cpa, grad_year=grad_year, certificate_level=certificate_level, timestamp=timestamp,register_id = register_id,blockchain_key=blockchain_key)
                    print("create new certificate on database register_id: {}".format(register_id))
                    append_cert_list.append(cert.student.student_id)
                    try:
                        cert_res = self.handler.create_certificate(att_certi_id=str(cert.blockchain_key),
                                                                    att_cpa= str(cert.cpa),
                                                                    att_type=cert.certificate_level,
                                                                    att_status = str(cert.status),
                                                                    for_student_student_id=str(cert.student.blockchain_key),
                                                                    for_university_university_id=str(cert.university.university_id),
                                                                    private_key=university.private_key)
                    except Exception as error: 
                        print(error)
                        return Response({'error':"Create certificate fail on blockchain by register_id: {}".format(register_id)}, status=status.HTTP_400_BAD_REQUEST)

                    cert_trans = Transaction.objects.create(transaction_id=cert_res['data']['txid'],transaction_type=Transaction.CREATE,timestamp = timestamp)
                    CertificateTransactions.objects.create(transaction = cert_trans,certificate=cert)
                    
                    try:
                        stud_bk = self.handler.get_student(str(student.blockchain_key))['data']['student']
                        stud_cert_list = Certificate.objects.filter(student=student).values_list('blockchain_key', flat=True)
                        stud_res = self.handler.update_student(att_student_id=stud_bk['student_id'],
                                                                att_name = stud_bk['name'],
                                                                att_phone = stud_bk['phone'],
                                                                att_email=stud_bk['email'],
                                                                att_address=stud_bk['address'],
                                                                att_public_key=stud_bk['public_key'],
                                                                for_certificate_certi_ids=stud_cert_list,
                                                                for_university_university_id=stud_bk["university_university_id"],
                                                                for_result_result_ids=stud_bk['result_result_ids'],
                                                                private_key = university.private_key)
                        
                        stud_transaction = Transaction.objects.create(transaction_id=stud_res['data']['txid'],transaction_type = Transaction.UPDATE,timestamp=timestamp)
                        StudentTransactions.objects.create(transaction=stud_transaction,student=student)
                    except InternalError as erri:
                        continue
                        # return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
                    except CommunicationError as errc:
                        continue
                        # return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                student = None
        try:
            uni_bk = self.handler.get_university(str(university.university_id))['data']['university']
            new_cert_list = Certificate.objects.filter(university=university).values_list('blockchain_key', flat=True)
            uni_res = self.handler.update_university(att_university_id=str(university.university_id),
                                                        att_university_name=uni_bk['university_name'],
                                                        att_email=uni_bk['email'],
                                                        att_phone=uni_bk['phone'],
                                                        att_address=uni_bk['address'],
                                                        att_status=uni_bk['status'],
                                                        att_public_key=uni_bk['public_key'],
                                                        for_professor_profess_ids=uni_bk['professor_profess_ids'],
                                                        for_student_student_ids=uni_bk['student_student_ids'],
                                                        for_staff_staff_ids=uni_bk['staff_staff_ids'],
                                                        for_certificate_certi_ids=new_cert_list,
                                                        for_subject_subject_ids=uni_bk['subject_subject_ids'],
                                                        private_key=university.private_key)
            
            uni_transaction = Transaction.objects.create(transaction_id=uni_res['data']['txid'],transaction_type = Transaction.UPDATE,timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,university=university)
        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        
        certificate = Certificate.objects.filter(university=university).order_by('-timestamp')[:20]
        serializer = CertificateSerializer(certificate, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

###

###
# Student API
###

class StudentAPIView(APIView):
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        if not university_id:
            return Response({'detail': 'missing query parameters'}, status=status.HTTP_400_BAD_REQUEST)
        university = get_object_or_404(University, id=university_id)
        students = Student.objects.filter(user__university=university_id).order_by('-user__date_joined')[:10]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        user = get_object_or_404(get_user_model(), id=pk)
        student = Student.objects.get(user=user)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        return

    def put(self, request, pk, format=None):
        return

class CreateStudentAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    handler = Handler()

    def post(self, request, format=None):
        university_id = request.data.get('university')
        university = get_object_or_404(University, id=university_id)

        excel_file = request.FILES['excel-file']
        if not excel_file:
            return Response({'detail': 'missing required field'}, status=status.HTTP_400_BAD_REQUEST)

        excel_data = read_file(excel_file)
        append_student_list = ""
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        for e_id, e_info in excel_data.items():
            public_key, private_key = self.handler.gen_key_pair()
            first_name = e_info['first name']
            last_name = e_info['last name']
            email = e_info['email']
            phone = e_info['phone']
            address = e_info['address']
            student_id = e_info['student_id']
            username = str(student_id)
            password = str(student_id)
            unit = e_info['unit']
            major = e_info['major']
            education_form = e_info['education form']
            blockchain_key = str(university.university_id)+"-"+str(student_id)
            try:
                Student.objects.get(student_id=student_id)
                continue
            except Student.DoesNotExist:
                user = get_user_model().objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,phone=phone,address=address,password=password,private_key=private_key, public_key=public_key,university=university,is_student=True)
                student = Student.objects.create(user=user, student_id=student_id, blockchain_key=blockchain_key,unit=unit, education_form=education_form,major = major)
                print("create new student on database {}".format(student_id))   

                try:
                    stud_response = self.handler.create_student(att_student_id=student.blockchain_key,
                                                            att_name=user.get_full_name(),
                                                            att_phone = str(user.phone),
                                                            att_email = user.email,
                                                            att_address=user.address,
                                                            att_public_key = user.public_key,
                                                            for_certificate_certi_ids=[''],
                                                            for_result_result_ids=[''],
                                                            for_university_university_id=user.university.university_id,
                                                            private_key = university.private_key)
                except Exception as error:
                    print(error)
                    return Response({"error":"create student fail on blockchain by id: {}".format(student_id)}, status=status.HTTP_400_BAD_REQUEST)
                
                student_create_transaction = Transaction.objects.create(transaction_id = stud_response['data']['txid'],transaction_type=Transaction.CREATE,timestamp=timestamp)
                StudentTransactions.objects.create(transaction=student_create_transaction,student=student)
        
        try:
            uni_bkc = self.handler.get_university(str(university.university_id))['data']['university']
            new_student_list = Student.objects.filter(user__university=university).values_list('blockchain_key', flat=True)
            try:
                response = self.handler.update_university(att_university_id=uni_bkc['university_id'],
                                                            att_university_name = uni_bkc['university_name'],
                                                            att_email = uni_bkc['email'],
                                                            att_phone = uni_bkc['phone'],
                                                            att_address=uni_bkc['address'],
                                                            att_status=uni_bkc['status'],
                                                            att_public_key=uni_bkc['public_key'],
                                                            for_professor_profess_ids=uni_bkc['professor_profess_ids'],
                                                            for_student_student_ids=new_student_list,
                                                            for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                            for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                            for_subject_subject_ids=uni_bkc['subject_subject_ids'],
                                                            private_key = university.private_key)
            except Exception as error:
                print(error)
                return Response({'error':"Update university: new list student fail!"}, status=status.HTTP_400_BAD_REQUEST)
            
            uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],transaction_type = Transaction.UPDATE,timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,university = university)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class GetBkDataStudentAPIView(APIView):
    handler = Handler()
    def get(self, request, format=None):
        student_id = request.query_params.get('student')
        try: 
            response = self.handler.get_student(student_id)
            return Response(response['data']['student'], status=status.HTTP_200_OK)
        except InternalError as erri:
                return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)

class FixUniversityBKStudentAPIView(APIView):
    handler=Handler()
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        university = get_object_or_404(University, id=university_id)
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        try:
            uni_bkc = self.handler.get_university(str(university_id))['data']['university']
            old_student_list = uni_bkc['student_student_ids']
            new_student_list = Student.objects.filter(user__university=university).values_list('blockchain_key', flat=True)
            response = self.handler.update_university(att_university_id=uni_bkc['university_id'],
                                                        att_university_name = uni_bkc['university_name'],
                                                        att_email = uni_bkc['email'],
                                                        att_phone = uni_bkc['phone'],
                                                        att_address=uni_bkc['address'],
                                                        # timestampp=uni_bkc['timestampp'],
                                                        att_status=uni_bkc['status'],
                                                        att_public_key=uni_bkc['public_key'],
                                                        for_professor_profess_ids=uni_bkc['professor_profess_ids'],
                                                        for_student_student_ids=new_student_list,
                                                        for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                        for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                        for_subject_subject_ids=uni_bkc['subject_subject_ids'],
                                                        private_key = university.private_key)
            
            uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],
                                                            transaction_type = Transaction.UPDATE,
                                                            timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,
                                                    university = university)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class TokenizeDataView(APIView):
    SECRET_TOKEN = 'QRA27MDAFD8A7FD6X'
    def post(self, request, format=None):
        user = request.user
        if not user.is_student:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        student = Student.objects.get(user=user)
        try:
            certificate = Certificate.objects.get(student=student)
            serializer = CertificateSerializer(certificate)
            if certificate.status == False:
                return Response({'detail': 'certificate revoked. Unable to share'}, status=status.HTTP_400_BAD_REQUEST)
            token = jwt.encode(serializer.data, self.SECRET_TOKEN, algorithm="HS256")
            return Response({"token": token}, status=status.HTTP_200_OK)
        except Certificate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
class TokenizeCertificateView(APIView):
    SECRET_TOKEN = 'QRA27MDAFD8A7FD6X'
    def get(self, request, format=None):
        user = request.user
        if not user.is_student:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        student = Student.objects.get(user=user)
        try:
            certificate = Certificate.objects.get(student=student)
            serializer = CertificateSerializer(certificate)
            if certificate.status == False:
                return Response({'detail': 'certificate revoked. Unable to share','error':"REVOKED_CERTIFICATE"}, status=status.HTTP_400_BAD_REQUEST)
            
            list_token = ShareCertificateToken.objects.filter(student=student)

            return Response(ShareCertificateTokenSerializer(list_token, many=True).data, status=status.HTTP_200_OK)
        except Certificate.DoesNotExist:
            return Response({'detail': 'Khong co bang cap'},status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user
        if not user.is_student:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        student = Student.objects.get(user=user)
        try:
            certificate = Certificate.objects.get(student=student)
            serializer = CertificateSerializer(certificate)
            if certificate.status == False:
                return Response({'detail': 'certificate revoked. Unable to share'}, status=status.HTTP_400_BAD_REQUEST)
            token = jwt.encode({"exp": datetime.now() + timedelta(days=7),"user_share_certificate":user.id}, self.SECRET_TOKEN, algorithm="HS256")
            object_token = ShareCertificateToken.objects.create(student=student, token=token.decode())
            return Response(ShareCertificateTokenSerializer(object_token).data, status=status.HTTP_200_OK)
        except Certificate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        user = request.user
        token_id = request.query_params.get("tokenId")
        if not user.is_student:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        student = Student.objects.get(user=user)
        try:
            token = ShareCertificateToken.objects.get(student=student, id=token_id)
            token.delete()
        except:
            return Response({'error':"Token does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        return Response({'data':"Delete success!"})
class DecodeTokenAPIView(APIView):
    permission_classes = [AllowAny]
    SECRET_TOKEN = 'QRA27MDAFD8A7FD6X'
    handler = Handler()
    def get(self, request, format=None):
        token = request.query_params.get('token')
        data = jwt.decode(token, self.SECRET_TOKEN, algorithms="HS256")
        exp = data["exp"]
        if datetime.now().timestamp() > exp:
            return Response({'error':"Token expired!"})
        try:
            user = customUser.objects.get(id=data["user_share_certificate"])
        except:
            return Response({'error':"Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_student:
            return Response({"error": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)
        student = Student.objects.get(user=user)
        try:
            token_obj = ShareCertificateToken.objects.get(student=student, token=token)
        except:
            return Response({'error':"Token does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        cert_tx_id = ""
        try:
            certificate = Certificate.objects.get(student=student)
            if certificate.status == False:
                return Response({'error': 'Certificate Revoked. Unable to read.'}, status=status.HTTP_400_BAD_REQUEST)
            
            certi_tranx = CertificateTransactions.objects.filter(certificate=certificate).order_by('-id').first()
            cert_tx_id = CertificateTransactionSerializer(certi_tranx).data["transaction"]["transaction_id"]
        except Certificate.DoesNotExist:
            return Response({'error': 'Certificate does not exist!'},status=status.HTTP_404_NOT_FOUND)

        result_tx_list = []
        try: 
            results = Result.objects.filter(student=student)
            for result in results:
                result_tx = ResultTransactions.objects.filter(result=result).order_by('-id').first()
                # print("xxxxxxxxxxxxxxxxxxxxxxx")
                result_tx_list.append(ResultTransactionSerializer(result_tx).data["transaction"]["transaction_id"])
        except:
            return Response({'error': 'Error get result table!'},status=status.HTTP_404_NOT_FOUND)


        return Response({"data": {"certificate":cert_tx_id, "result": result_tx_list}}, status=status.HTTP_200_OK)


###

###
# Professor API
###

class ProfessorAPIView(APIView):
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        if not university_id:
            return Response({'detail': 'missing query parameters'}, status=status.HTTP_400_BAD_REQUEST)
        university = get_object_or_404(University, id=university_id)
        professors = Professor.objects.filter(user__university=university_id).order_by('-user__date_joined')[:10]
        serializer = ProfessorSerializer(professors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessorDetailAPIView(APIView):
    def get(self, request, pk, format=None):
        user = get_object_or_404(get_user_model(), id=pk)
        professor = Professor.objects.get(user=user)
        serializer = ProfessorSerializer(professor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        return

    def put(self, request, pk, format=None):
        return

    def patch(self, request, pk, format=None):
        return

class FixUniversityBKProfessorAPIView(APIView):
    handler=Handler()
    def get(self, request, format=None):
        university_id = request.query_params.get('university')
        university = get_object_or_404(University, id=university_id)
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        try:
            uni_bkc = self.handler.get_university(str(university.university_id))['data']['university']
            new_professor_list = Professor.objects.filter(user__university=university).values_list('professor_id', flat=True)
            response = self.handler.update_university(att_university_id=uni_bkc['university_id'],
                                                        att_university_name = uni_bkc['university_name'],
                                                        att_email = uni_bkc['email'],
                                                        att_phone = uni_bkc['phone'],
                                                        att_address=uni_bkc['address'],
                                                        # timestampp=uni_bkc['timestampp'],
                                                        att_status=uni_bkc['status'],
                                                        att_public_key=uni_bkc['public_key'],
                                                        for_professor_profess_ids=new_professor_list,
                                                        for_student_student_ids=uni_bkc['student_student_ids'],
                                                        for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                        for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                        for_subject_subject_ids=uni_bkc['subject_subject_ids'],
                                                        private_key = university.private_key)
            
            uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],
                                                            transaction_type = Transaction.UPDATE,
                                                            timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,
                                                    university = university)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class CreateProfessorAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    handler = Handler()

    def post(self, request, format=None):
        university_id = request.data.get('university')
        university = get_object_or_404(University, id=university_id)

        excel_file = request.FILES['excel-file']
        excel_data = read_file(excel_file)
        timestamp = now().replace(tzinfo=utc)
        str_timestamp = timestamp.strftime("%d/%M/%Y, %H:%M:%S")
        append_professor_list = []
        for e_id, e_info in excel_data.items():
            public_key, private_key = self.handler.gen_key_pair()
            first_name = e_info['first name']
            last_name = e_info['last name']
            email = e_info['email']
            phone = e_info['phone']
            address = e_info['address']
            professor_id = e_info['professor_id']
            department = e_info['department']
            username = first_name.replace(" ", "").lower()+'.'+last_name[0].lower()+professor_id
            password = professor_id
            blockchain_key = str(university.university_id)+"-"+str(professor_id)
            try:
                Professor.objects.get(professor_id=professor_id)
                continue
            except Professor.DoesNotExist:
                user = get_user_model().objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,phone=phone,address=address,password=password,private_key=private_key, public_key=public_key,university=university,is_professor=True)
                professor = Professor.objects.create(user=user, professor_id=professor_id, blockchain_key=blockchain_key,department=department)
                
                append_professor_list.append(professor.blockchain_key)
                print("created new profess {}".format(professor_id))
                try:
                    prof_response = self.handler.create_professor(att_profess_id=professor.blockchain_key,
                                                                att_name = user.get_full_name(),
                                                                att_email = user.email,
                                                                att_phone = str(user.phone),
                                                                att_address = user.address,
                                                                att_status = str(user.is_active),
                                                                att_public_key = user.public_key,
                                                                for_classroom_class_ids=[''],
                                                                for_university_university_id=user.university.university_id,
                                                                private_key = university.private_key)
                except:
                    return Response({"error":"Created professor fail on blockchain by id: {}".format(professor_id) }, status=status.HTTP_400_BAD_REQUEST)
                
                professor_transaction = Transaction.objects.create(transaction_id = prof_response['data']['txid'],transaction_type = Transaction.CREATE,timestamp=timestamp)
                ProfessorTransactions.objects.create(transaction=professor_transaction,professor=professor)
            
        try:
            uni_bkc = self.handler.get_university(str(university.university_id))["data"]["university"]
            new_professor_list = Professor.objects.filter(user__university=university).values_list('blockchain_key', flat=True)
            response = self.handler.update_university(att_university_id=uni_bkc['university_id'],
                                                        att_university_name = uni_bkc['university_name'],
                                                        att_email = uni_bkc['email'],
                                                        att_phone = uni_bkc['phone'],
                                                        att_address=uni_bkc['address'],
                                                        att_status=uni_bkc['status'],
                                                        att_public_key=uni_bkc['public_key'],
                                                        for_professor_profess_ids=new_professor_list,
                                                        for_student_student_ids=uni_bkc['student_student_ids'],
                                                        for_staff_staff_ids=uni_bkc['staff_staff_ids'],
                                                        for_certificate_certi_ids=uni_bkc['certificate_certi_ids'],
                                                        for_subject_subject_ids=uni_bkc['subject_subject_ids'],
                                                        private_key = university.private_key)
            
            uni_transaction = Transaction.objects.create(transaction_id = response['data']['txid'],transaction_type = Transaction.UPDATE,timestamp=timestamp)
            UniversityTransactions.objects.create(transaction=uni_transaction,university = university)

        except InternalError as erri:
            return Response({'detail': erri.message}, status=status.HTTP_400_BAD_REQUEST)
        except CommunicationError as errc:
            return Response({'detail': errc.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

###

###
# Login/Logout/Register API
###

class UserAPIView(APIView):
    def get(self, request, pk, format=None):
        return


class UserRegister(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(status=status.HTTP_201_CREATED)
        # return Response(payload, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CurrentUser(APIView):
    def get(self, request, format=None):
        '''Determine the current user by their token, and return their data'''
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class UsersAPIView(APIView):
    def get(self, request, format=None):
        university_id = request.query_params.get('university', None)

        if university_id:
            university = get_object_or_404(University, id=university_id)

            members = get_user_model().objects.filter(university=university)

            serializer = UserSerializer(members, many=True, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UpdateAvatarUser(APIView):
    def patch(self, request, pk, format=None):

        user = get_object_or_404(get_user_model(), id=pk)
        # student = Student.objects.filter(user=user).first()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request, format=None):

        return Response(status=status.HTTP_200_OK)



class UpdateResultInClassAPIView(APIView):
    handler = Handler()
    def post(self, request, format=None):
        user = request.user
        if not user.is_professor:
            return Response({'detail': 'permission denied'}, status = status.HTTP_401_UNAUTHORIZED)
        
        professor = Professor.objects.get(user=user)
        if not professor:
            return Response({'detail': 'Object not found'}, status = status.HTTP_404_NOT_FOUND)
        response_data = []
        for new_result in request.data:
            result = get_object_or_404(Result, id=new_result['id'])
            if result.class_detail.professor.professor_id != professor.professor_id:
                return Response({'detail': 'permission denied'}, status = status.HTTP_401_UNAUTHORIZED)

            if new_result['middle_score'] == result.middle_score and new_result['final_score'] == result.final_score:
                response_data.append({"class_id": result.class_detail.class_id, "student": result.student.student_id, "status":"no_change"})
            else:
                data = new_result
                print(type(new_result['middle_score']))
                try:
                    result.middle_score = float(new_result['middle_score'])
                except:
                    result.middle_score = -1
                try:
                    result.final_score = float(new_result['final_score'])
                except:
                    result.final_score = -1

                try:
                    result.save()
                    timestamp = now().replace(tzinfo=utc)
                    try :
                        updated_result = get_object_or_404(Result, id=data["id"])

                        result_bk = self.handler.get_result(str(result.result_id))['data']['result']
                        result_res = self.handler.update_result(att_result_id=result_bk['result_id'],
                                                                att_middlescore=str(updated_result.middle_score),
                                                                att_finallscore=str(updated_result.final_score),
                                                                # timestampp=result_bk['timestampp'],
                                                                for_classroom_class_id=result_bk['classroom_class_id'],
                                                                for_student_student_id=result_bk['student_student_id'],
                                                                private_key = professor.user.private_key)
                        res_transaction = Transaction.objects.create(transaction_id=result_res['data']['txid'],
                                                                        transaction_type = Transaction.UPDATE,
                                                                        timestamp=timestamp)

                        ResultTransactions.objects.create(transaction=res_transaction, result=result)    
                        response_data.append({"class_id": result.class_detail.class_id, "student": result.student.student_id, "status":"update_success"})
                    except:
                        response_data.append({"class_id": result.class_detail.class_id, "student": result.student.student_id, "status":"update_fail_on_blockchain"})
                except:
                    response_data.append({"class_id": result.class_detail.class_id, "student": result.student.student_id, "status":"update_fail_on_database"})


        return Response({'data':response_data})

class ViewDetailTransaction(APIView):
    check = Handler()
    def get(self, request, format=None):
        tx_data = self.check.get_data_blockchain([request.query_params["txid"]])
        # print(tx_data)
        try: 
            user = customUser.objects.get(public_key=tx_data[0]["data"]["header"]["signer_public_key"])
            if user.is_professor:
                profess = Professor.objects.get(user=user)
                profess_data = ProfessorSerializer(profess).data
                profess_id = profess_data["professor_id"]
                profess_name = profess_data["user"]["full_name"]

                # return Response({"tx_data": tx_data, "signer": ProfessorSerializer(profess).data})
                return Response({"tx_data": tx_data[0], "signer": {"signer_id": profess_id, "name": profess_name}})
        except:
            try: 
                university = University.objects.get(public_key=tx_data[0]["data"]["header"]["signer_public_key"])
                uni_data = UniversitySerializer(university).data
                uni_id = uni_data["university_id"]
                uni_name = uni_data["university_name"]
                return Response({"tx_data": tx_data[0], "signer": {"signer_id": uni_id, "name": uni_name}})
            except:
                return Response({"tx_data": tx_data[0], "error":"Object not exist"})

        return Response({"tx_data": tx_data})

class TransactionsAPIView(APIView):
    check = Handler()
    def get(self, request, format=None):
        page = int(request.query_params["page"])
        tx = Transaction.objects.all().order_by("-timestamp")
        serializer = TransactionSerializer(tx[((page-1)*10):(page*10)], many=True)
        total_data = len(tx)
        list_tx_id = []
        for tran in serializer.data:
            list_tx_id.append(tran["transaction_id"])
        list_data_txs = self.check.get_data_blockchain(list_tx_id)
        data_response = []

        for data in list_data_txs:
            try: 
                user = customUser.objects.get(public_key=data["data"]["header"]["signer_public_key"])
                if user.is_professor:
                    profess = Professor.objects.get(user=user)
                    profess_data = ProfessorSerializer(profess).data
                    profess_id = profess_data["professor_id"]
                    profess_name = profess_data["user"]["full_name"]
                    data_response.append({"tx_data": data, "signer": {"signer_id": profess_id, "name": profess_name}})
            except:
                try: 
                    university = University.objects.get(public_key=data["data"]["header"]["signer_public_key"])
                    uni_data = UniversitySerializer(university).data
                    uni_id = uni_data["university_id"]
                    uni_name = uni_data["university_name"]
                    data_response.append({"tx_data": data, "signer": {"signer_id": uni_id, "name": uni_name}})
                except:
                    data_response.append({"tx_data": data, "error":"Object not exist"})

        return Response({"data": data_response, "total":total_data})
        