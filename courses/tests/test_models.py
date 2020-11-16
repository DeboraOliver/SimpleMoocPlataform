from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from model_bakery import baker #testa models e automatiza

from courses.models import Course

class CourseManagerTestCase(TestCase):

    def setUp(self):
        #vms criar 5 cursos (quantity=5) tds com msm nome
        self.courses_django = baker.make(
            'courses.Course', name='Python na Web com Django', _quantity=5
        ) #o mommy evita que eu crie dezenas de linhas criando cursos
        self.courses_dev = baker.make(
            'courses.Course', name='Python para Devs', _quantity=10
        ) #não me retorna ummodel, mas sim uma lista
        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()
        #for course in self.courses_dev:
         #   course.delete()

    def test_course_search(self):
        search = Course.objects.search('django')#testar o search p a palavra 'django'
        self.assertEqual(len(search), 5)
        search = Course.objects.search('devs')
        self.assertEqual(len(search), 10) #pq criamos 10 cursos  com este nome
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)
