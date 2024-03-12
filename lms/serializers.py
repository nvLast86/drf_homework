from rest_framework import serializers
from .models import Course, Lesson, Payments, SubscriptionCourse
from .validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(field='video_link')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    all_lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCourse
        fields = "__all__"
