from django.urls import path

from .views import (UserEmailExists, UserRegisterView, AdminRegisterView, ResumeView, LogInView,
                    UserResumeWriteView, ResumeDetailWriteView, ResumeDetailView, CareerResultView,
                    ResumeMainView, LikedCompanies, UserMatchUpView, UserMatchUpResumeView,
                    MatchupJobTextView, UserUpdateView, UserGlobalView, UserBookmark,
                    UserMatchUpDetailView, CompanyInterviewResume, CompanyRequestsResume,
                    MatchUpDetailGetView, IsAdminToken, MatchUpRegistrationView,
                    UserImageUploadView, UserApplyView, ApplicantResumeView)

urlpatterns = [
    path('/is/admin', IsAdminToken.as_view()),
    path('/exists', UserEmailExists.as_view()),
    path('/register', UserRegisterView.as_view()),
    path('/adminregister', AdminRegisterView.as_view()),
    path('/login', LogInView.as_view()),
    path('/likes', LikedCompanies.as_view()),
    path('/resume', ResumeView.as_view()),
    path('/resume/<str:main_resume_id>', UserResumeWriteView.as_view()),
    path('/resumeDetailWrite/<str:main_resume_id>', ResumeDetailWriteView.as_view()),
    path('/resumeDetail/<str:main_resume_id>', ResumeDetailView.as_view()),
    path('/resumeResult/<str:main_career_id>', CareerResultView.as_view()),
    path('/resumeMain', ResumeMainView.as_view()),
    path('/specList', UserMatchUpView.as_view()),
    path('/requests', CompanyRequestsResume.as_view()),
    path('/proposals', CompanyInterviewResume.as_view()),
    path('/userResume/<str:main_resume_id>', UserMatchUpResumeView.as_view()),
    path('/jobtext', MatchupJobTextView.as_view()),
    path('/userUpdate', UserUpdateView.as_view()),
    path('/global', UserGlobalView.as_view()),
    path('/bookmark', UserBookmark.as_view()),
    path('/matchupDetail', UserMatchUpDetailView.as_view()),
    path('/resumeRole/<str:main_resume_id>', MatchUpDetailGetView.as_view()),
    path('/matchupRegistration', MatchUpRegistrationView.as_view()),
    path('/userImage', UserImageUploadView.as_view()),
    path('/applicantResume/<str:main_resume_id>', ApplicantResumeView.as_view()),
    path('/apply', UserApplyView.as_view())
]
