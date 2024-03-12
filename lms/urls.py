from django.urls import path
from rest_framework import routers

from lms import views, apps

app_name = apps.LmsConfig.name

router = routers.DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/', views.LessonListAPIView.as_view(), name='all_lessons'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='view_lesson'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='update_lesson'),
    path('lesson/destroy/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='delete_lesson'),
    path('payments/', views.PaymentsListView.as_view(), name='payments_list'),
    path('subscription/create', views.SubscriptionCreateAPIView.as_view(), name='create_subscription'),
    path('subscription/delete/<int:pk>', views.SubscriptionDestroyAPIView.as_view(), name='delete_subscription'),
    ] + router.urls
