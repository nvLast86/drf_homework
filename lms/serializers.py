from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from .models import Course, Lesson, Payments, SubscriptionCourse
from .validators import UrlValidator
from .services import stripe_retrieve_session
from users.models import User


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


class PaymentsCreateSerializer(serializers.ModelSerializer):
    payment_link = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = '__all__'

    def get_payment_link(self, payment: Payments):
        session = stripe_retrieve_session(payment.session_id)
        return session.url


class PaymentDetailSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для просмотра детальной информации по объекту Payment"""
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    payment_link = serializers.SerializerMethodField()
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payments
        fields = '__all__'

    def get_payment_link(self, payment: Payments):
        """Получает ссылку на оплату"""
        session = stripe_retrieve_session(payment.session_id)
        return session.url

class SubscriptionCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionCourse
        fields = "__all__"



