from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404

from .models import Course, Lesson, Payments, SubscriptionCourse
from .paginators import LessonPaginator
from .serializers import (CourseSerializer, LessonSerializer, PaymentsSerializer, PaymentsCreateSerializer,
                          PaymentDetailSerializer, SubscriptionCourseSerializer)
from .permissions import IsStaff, IsOwner, IsOwnerOrIsStaff

from .services import stripe_create_session, stripe_retrieve_session
from lms.tasks import send_notification_update_course


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonPaginator

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [~IsStaff]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsOwnerOrIsStaff]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        send_notification_update_course.delay(instance.pk)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsStaff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentsListView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['payment_type', 'lesson', 'course']
    ordering_fields = ['payment_date']


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentsCreateSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            course = serializer.validated_data['course']
            user = request.user

            session = stripe_create_session(course, user)
            payment = Payments.objects.create(
                course=course,
                user=user,
                session_id=session.id
            )
            payment_serializer = PaymentsCreateSerializer(payment)
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)

        except Payments.DoesNotExist:
            raise APIException(detail='Платеж не найден')


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр детальной информации о платеже"""
    serializer_class = PaymentDetailSerializer
    queryset = Payments.objects.all()

    def get_object(self):
        """Меняет статус оплаты, если оплачено"""
        payment = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if payment.session_id:
            session = stripe_retrieve_session(payment.session_id)
            if session.payment_status in ['paid', 'complete']:
                payment.is_paid = True
                payment.save()
        return payment


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """Обновление платежа"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """Удаление платежа"""
    queryset = Payments.objects.all()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionCourseSerializer
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(generics.UpdateAPIView):
    serializer_class = SubscriptionCourseSerializer
    queryset = SubscriptionCourse.objects.all()
    permission_classes = [IsAuthenticated]
