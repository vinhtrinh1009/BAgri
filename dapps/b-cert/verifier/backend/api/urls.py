from django.urls import include, path
from .views import *
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'check_certificate/<string:token>', TockenSharedAPIView)

urlpatterns = [
    # path("", include(router.urls))
    path("decrypt-token/", DecryptTokenAPIView.as_view()),
    path('get-certificate-data/<str:pk>/', GetCertificateDataAPIView.as_view()),
    path('get-result-data/<str:pk>/', GetResultDataBlockchain.as_view()),
    path('get-student-data/<str:pk>/', GetStudentDataBlockchain.as_view()),
    path('get-university-data/<str:pk>/', GetUniversityDataBlockchain.as_view()),
    path('get-classroom-data/<str:pk>/', GetClassesDataBlockchain.as_view()),
    path('get-subject-data/<str:pk>/', GetSubjectDataBlockchain.as_view()),
]
