from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from school.models import ShareCertificateToken, University, Staff, Student, Professor, Subject, Class, Result, Certificate, Transaction, UniversityTransactions, SubjectTransactions, StaffTransactions, ProfessorTransactions, StudentTransactions, ClassTransactions, ResultTransactions, CertificateTransactions
from django.contrib.auth import get_user_model
from .utils import generate_key_pair
from bcertsdk.handler import Handler
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = '__all__'

    # def get_avatar(self, obj):
    #     request = self.context.get('request')

    #     if not request:
    #         return obj.avatar.url

    #     if obj.avatar:
    #         if obj.avatar.url:
    #             avatar_url = obj.avatar.url
    #             return request.build_absolute_uri(avatar_url)

    #     return


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'


class SubjectDetailSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()

    class Meta:
        model = Subject
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    university = UniversitySerializer()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'avatar', 'private_key', 'public_key', 'university', "address", "phone")

    def get_full_name(self, obj):
        return obj.full_name()

    def get_avatar(self, obj):
        request = self.context.get('request')

        if not request:
            return obj.avatar.url
        if obj.avatar:
            avatar_url = obj.avatar.url
            return request.build_absolute_uri(avatar_url)

        return


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = ('token', 'username', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        public_key, private_key = Handler().gen_key_pair()
        user = get_user_model().objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'],
                                                    first_name=validated_data['first_name'], last_name=validated_data['last_name'], is_staff=True, private_key=private_key, public_key=public_key)
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Professor
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    student_list = serializers.SerializerMethodField()
    subject_id = serializers.SerializerMethodField()
    subject_name = serializers.SerializerMethodField()
    professor_id = serializers.SerializerMethodField()
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = '__all__'
    
    def get_student_list(self, obj):
        student_list = ''
        for student in obj.students.all():
            student_list = student_list+student.student_id+", "
        return student_list
    
    def get_subject_id(self, obj):
        return obj.subject.subject_id

    def get_subject_name(self, obj):
        return obj.subject.name
    
    def get_professor_id(self, obj):
        return obj.professor.professor_id
    
    def get_professor_name(self, obj):
        return obj.professor.user.get_full_name()

class ResultListSerializer(serializers.ListSerializer):
    def update(self, validated_data):

        pass


class ResultSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Result
        fields = '__all__'


class AllResultsOfStudentSerializer(serializers.ModelSerializer):
    class_detail = ClassSerializer()

    class Meta:
        model = Result
        fields = ("class_detail", "middle_score", "final_score", "status")


class ResultDetailSerializer(serializers.ModelSerializer):

    class_detail = ClassSerializer()
    student = StudentSerializer()

    class Meta:
        model = Result
        fields = '__all__'


class ClassDetailSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    subject = SubjectSerializer()
    professor = ProfessorSerializer()

    class Meta:
        model = Class
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    student_id = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()
    university_name = serializers.SerializerMethodField()
    student_major = serializers.SerializerMethodField()
    education_form = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = '__all__'
    
    def get_student_id(self, obj):
        return obj.student.student_id

    def get_university_name(self, obj):
        return obj.university.university_name
    
    def get_student_major(self, obj):
        return obj.student.major
    
    def get_education_form(self, obj):
        return obj.student.education_form
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name()


class CertificateDetailSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    student = UserSerializer()

    class Meta:
        model = Certificate
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class UniversityTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    university = UniversitySerializer()

    class Meta:
        model = UniversityTransactions
        fields = '__all__'        

class StaffTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    staff = StaffSerializer()

    class Meta:
        model = StaffTransactions
        fields = '__all__'   

class ProfessorTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    professor = ProfessorSerializer()

    class Meta:
        model = ProfessorTransactions
        fields = '__all__'   

class StudentTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    student = StudentSerializer()

    class Meta:
        model = StudentTransactions
        fields = '__all__'   

class SubjectTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = SubjectTransactions
        fields = '__all__'   

class ClassTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    class_detail = ClassDetailSerializer()

    class Meta:
        model = ClassTransactions
        fields = '__all__'   

class ResultTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    result = ResultSerializer()

    class Meta:
        model = ResultTransactions
        fields = '__all__'  

class CertificateTransactionSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer()
    certificate = CertificateSerializer()

    class Meta:
        model = CertificateTransactions
        fields = '__all__'    

class ShareCertificateTokenSerializer(serializers.ModelSerializer):
    # student = StudentSerializer()
    class Meta:
        model = ShareCertificateToken
        fields = '__all__'
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = user.id
        if user.is_staff:
            token['role'] = 'staff'
        elif user.is_professor:
            token['role'] = 'professor'
        elif user.is_student:
            token['role'] = 'student'
        else:
            token['role'] = ''
        if user.university:
            token['university'] = user.university.id
        else:
            token['university'] = ""
        # ...
        return token
    # @classmethod

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user': self.user.id})
        if self.user.is_staff:
            data.update({'role': 'staff'})
        elif self.user.is_professor:
            data.update({'role': 'professor'})
        elif self.user.is_student:
            data.update({'role': 'student'})
        # and everything else you want to send in the response
        else:
            data.update({'role': ''})
        if self.user.university:
            data.update({'university': self.user.university.id})
        else:
            data.update({'university': ""})

        return data
