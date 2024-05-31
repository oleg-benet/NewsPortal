from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostEdit, PostDelete, PostCreate, CategoryList, subscribe

urlpatterns = [
    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:id>', PostDetail.as_view(), name='post_detail'),
    path('news/create', PostCreate.as_view(), name='news_create'),
    path('news/search', PostSearch.as_view(), name='post_search'),
    path('news/<int:id>/edit', PostEdit.as_view(), name='news_edit'),
    path('news/<int:id>/delete', PostDelete.as_view(), name='news_delete'),
    path('articles/create', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:id>/delete', PostDelete.as_view(), name='articles_delete'),
    path('news/<int:id>/edit', PostEdit.as_view(), name='articles_edit'),
    path('news/category/<int:pk>', CategoryList.as_view(), name='category'),
    path('news/category/<int:pk>/subscribe', subscribe, name='subscribe')
]
