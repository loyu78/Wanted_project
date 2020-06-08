from django.urls import path

from .views import CompanyRegister, CompanyPosition, PositionList, DetailView, \
         PositionBookmarkView, PositionApplyView, CompanyLikedResume, \
         JobAd, ThemeList, HomeView, MatchupList, \
         PositionAdvertisement, PositionMain, MainFilter, TagView, TagSearch

urlpatterns = [
    path('/register', CompanyRegister.as_view()),
    path('/positions/create', CompanyPosition.as_view()),
    path('/positions', PositionList.as_view()),
    path('/position/<int:position_id>', DetailView.as_view()),
    path('/like/resume', CompanyLikedResume.as_view()),
    # path('/request/matchup', RequestResume.as_view()),
    # path('/requests/matchup', RequestMatchupList.as_view()),
    path('/position/<int:position_id>/bookmark', PositionBookmarkView.as_view()),
    path('/position/<int:position_id>/apply', PositionApplyView.as_view()),
    path('/matchup/list', MatchupList.as_view()),
    path('/themelist/<int:theme_id>', ThemeList.as_view()),
    path('/home', HomeView.as_view()),
    path('/job-ad', JobAd.as_view()),
    # path('/read/matchup', ReadingMatchup.as_view()),
    # path('/reading', ReadingMatchupList.as_view()),
    # path('/proposal', ProposalView.as_view()),
    path('/position/main', PositionMain.as_view()),
    path('/position/advertisement', PositionAdvertisement.as_view()),
    path('/position/main/filter', MainFilter.as_view()),
    path('/position/tag', TagView.as_view()),
    path('/position/tag/search', TagSearch.as_view())
]
