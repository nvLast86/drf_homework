from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from lms.models import Course, Lesson, SubscriptionCourse
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test1', owner=self.user)

    def test_create_course(self):
        """Тестирование создание курса"""
        data = {'title': 'Test2', 'owner': self.user}
        response = self.client.post(path='/courses/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.all().exists())

    def test_list_course(self):
        """Тестирование вывода списка курса"""
        response = self.client.get(path='/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual( Course.objects.all().count(), 1)

    def test_retrieve_course(self):
        """Тестирования детальной информации по курсу"""
        response = self.client.get(path=f'/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),{ 'id': self.course.id, 'title': self.course.title, 'count_lessons': 0,
                                           'lessons': [], 'description': None, 'preview': None, 'subscription': False,
                                           'owner': self.user.email})

    def test_update_course(self):
        """Тестирование обновления курса"""
        data = {"title": 'test_update'}
        response = self.client.patch(path=f'/courses/{self.course.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], data['title'] )

    def test_destroy_course(self):
        """Тестирование удаления курса"""
        response = self.client.delete(path=f'/courses/{self.course.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test', owner=self.user)
        self.lesson = Lesson.objects.create(title='Test', course=self.course, owner=self.user)

    def test_create_lesson(self):
        """Тестирование создание урока"""
        data = {'title': 'Test', 'course': self.course.id, 'owner': self.user.id}
        response = self.client.post(reverse('lms:create_lesson'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(),2)

    def test_create_lesson_validation_error(self):
        data = {'title': 'TestError', 'course': self.course.id, 'owner': self.user.id, 'video_link': 'https://my.sky.pro/'}
        response = self.client.post(reverse('lms:create_lesson'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors':
                                               ['Cсылки на сторонние образовательные платформы или личные сайты прикреплять нельзя']} )

    def test_list_lesson(self):
            """Тестирование вывода списка уроков"""
            response = self.client.get(reverse('lms:all_lessons'),)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()['count'], 1)

    def test_retrieve_lesson(self):
            """Тестирования детальной информации по уроку"""
            response = self.client.get(reverse('lms:view_lesson', kwargs={'pk': self.lesson.pk}))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), {'id': self.lesson.pk, 'course': self.course.title,
                                               'owner': self.user.email, 'title': self.lesson.title, 'preview': None,
                                               'description': None, 'video_link': None})

    def test_update_lesson(self):
                """Тестирование обновления урока"""
                data = {'title': 'test_update'}
                response = self.client.patch(reverse('lms:update_lesson', kwargs={'pk': self.lesson.pk}),
                                             data=data)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.json()['title'], data['title'])

    def test_destroy_lesson(self):
                """Тестирование удаления урока"""
                response = self.client.delete(reverse('lms:delete_lesson', kwargs={'pk': self.lesson.pk}),)
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionCourseTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='test@example.com', password='test')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test', owner=self.user)

    def test_create_subscription(self):
            data = {'user': self.user.id, 'course': self.course.id, 'status': True}
            response = self.client.post(reverse('lms:create_subscription'), data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(SubscriptionCourse.objects.all().exists())

    def test_delete_subscription(self):
        data = {'user': self.user, 'course': self.course, 'status': True}
        subscription = SubscriptionCourse.objects.create(**data)
        response = self.client.delete(reverse('lms:delete_subscriptione', kwargs={'pk': subscription.pk}), )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

