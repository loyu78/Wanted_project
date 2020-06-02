from django.urls import path
from .views import *

urlpatterns = [
	path('/register', CompanyRegister.as_view()),
	path('/positions/create', CompanyPosition.as_view()),
  path('/positions', PositionList.as_view()),
  path('/themetop/<int:theme_id>',ThemeTop.as_view()),
  path('/themelist/<int:theme_id>',ThemeList.as_view()),
]
