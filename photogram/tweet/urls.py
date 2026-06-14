from . import views
from django.urls import path , include
from .views import CustomLoginView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.tweet_list , name = "tweet_list"),
    path("__reload__/", include("django_browser_reload.urls")),
    path('create/', views.tweet_create , name = "tweet_create"),
    path('edit/<int:tweet_id>/', views.tweet_edit , name = "tweet_edit"),
    path('delete/<int:tweet_id>/', views.tweet_delete , name = "tweet_delete"),   
    path('form/', views.tweet_create , name = "form"),
    path('register/' , views.register , name="register"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('search/', views.search, name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('profile/<str:username>/', views.profile, name='profile'),

] 