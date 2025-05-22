from django.urls import path
from .views import PostList, PostDetail, NewsCreate, ArticleCreate, NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete, search_news, subscribe


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
   path('search/', search_news, name='news_search'),
   path('news/category/<int:subscribed_categories>/subscribe/', subscribe, name='subscribe'),
]
