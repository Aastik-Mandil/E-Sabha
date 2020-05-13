from django.urls import path
from social import views
from django.views.generic.base import RedirectView
from django.urls import include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'myprofile', views.MyProfileViewSet)
router.register(r'mypost', views.MyPostViewSet)
router.register(r'postcomment', views.PostCommentViewSet)
router.register(r'postlike', views.PostLikeViewSet)
router.register(r'followuser', views.FollowUserViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('home/', views.HomeView.as_view()),
    path('about/', views.AboutView.as_view()),
    path('contact/', views.ContactView.as_view()),

    path('mypost/create/', views.MyPostCreate.as_view(success_url="/social/home")),
    path('mypost/delete/<int:pk>', views.MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('mypost/', views.MyPostListView.as_view()),
    path('mypost/<int:pk>', views.MyPostDetailView.as_view()),
    path('mypost/like/<int:pk>', views.like),
    path('mypost/unlike/<int:pk>', views.unlike),

    path('myprofile/', views.MyProfileListView.as_view()),
    path('myprofile/<int:pk>', views.MyProfileDetailView.as_view()),
    path('profile/edit/<int:pk>', views.MyProfileUpdateView.as_view(success_url="/social/mypost")),
    path('myprofile/follow/<int:pk>', views.follow),
    path('myprofile/unfollow/<int:pk>', views.unfollow),

    path('postcomment/create/', views.PostCommentCreate.as_view(success_url="/social/home")),
    path('postcomment/<int:pk>/', views.PostCommenteListView.as_view()),
    # path('postcomment/<int:pk>/', views.postCommentDetailView),

    path('', RedirectView.as_view(url="home/")),

    path(r'api/', include(router.urls)),
    path(r'api-token-auth', obtain_jwt_token),
]
