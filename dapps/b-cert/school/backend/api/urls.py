from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('users/', UsersAPIView.as_view()),
    path('users/<int:pk>/', UserAPIView.as_view()),
    path('current-user/', CurrentUser.as_view()),

    path('update/avatar/<int:pk>/', UpdateAvatarUser.as_view()),

    path('university/', UniversityAPIView.as_view()),
    path('university/<int:pk>/', UniversityDetailsAPIView.as_view()),
    path('register-university/', RegisterUniversityAPIView.as_view()),
    path('update-university-info/<int:pk>/', UpdateUniversityAPIView.as_view()),

    path('student/', StudentAPIView.as_view()),
    path('student/<int:pk>/', StudentDetailAPIView.as_view()),

    path('professor/', ProfessorAPIView.as_view()),
    path('professor/<int:pk>/', ProfessorDetailAPIView.as_view()),

    path('subject/', SubjectAPIView.as_view()),
    path('create-subject/', CreateSubjectAPIView.as_view()),
    
    path('classes/<int:pk>/', ClassDetailAPIView.as_view()),
    path('classes/', ClassesAPIView.as_view()),
    path('create-class/', CreateClassAPIView.as_view()),

    path('results/', ResultsAPIView.as_view()),
    path('results/<int:pk>/', ResultDetailAPIView.as_view()),
    path('update-results/', UpdateResultInClassAPIView.as_view()),

    path('certificates/', CertificatesAPIView.as_view()),
    path('search-certificate/', SearchCertificateAPIView.as_view()),
    path('create-certificate', CreateCertificateAPIView.as_view()),
    path('update-certificate/<str:pk>/', UpdateCertificateAPIView.as_view()),

    path('create-student/', CreateStudentAPIView.as_view()),
    path('create-professor/', CreateProfessorAPIView.as_view()),

    path('auth/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('auth/register', UserRegister.as_view(), name='register'),
    path('auth/forgot-password', ForgotPasswordView.as_view()),
    
    path('student/tokenize-data/', TokenizeDataView.as_view()),
    path('student/tokenize-certificate/', TokenizeCertificateView.as_view()),
    path('student/decode-token/', DecodeTokenAPIView.as_view()),

    path('fix-uni-studentlist/', FixUniversityBKStudentAPIView.as_view()),
    path('fix-uni-professorlist/', FixUniversityBKProfessorAPIView.as_view()),
    path('fix-uni-classlist/', FixClassDataBkAPIView.as_view()),
    path('get-class-bk/', GetBkDataClassAPIView.as_view()),
    path('get-student-bk/', GetBkDataStudentAPIView.as_view()),
    path('add-class-bk/', AddClassBkAPIView.as_view()),
    path('get-uni-bk/', GetUniversityBkAPIView.as_view()),
    path('fix-uni-subjectlist/', FixSubjectOnBKAPIView.as_view()),
    path('view-detail-tx/', ViewDetailTransaction.as_view()),
    path('get_all_transaction/', TransactionsAPIView.as_view()),
    # path('add-subj-bkkey/', SubjectAddBkKeyAPIView.as_view()),
    # path('add-stud-bkkey/', StudentAddBkKeyAPIView.as_view())
    
]
