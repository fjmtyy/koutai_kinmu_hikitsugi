from django.urls import path
from . import views

app_name ="handover"

urlpatterns = [
    path('top/', views.HandoverListView.as_view(), name='top'),
    path('post/', views.HandoverPostView.as_view(), name='post'),
    path('top/handover_detail/<int:pk>/', views.HandoverDetailView.as_view(), name='handover_detail'),
    path('search/', views.HandoverSearchView.as_view(), name='search'),
]
