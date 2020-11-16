from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

#use python manage.py test
#para  testar a aplicação o django cria um bd temporário nome_do_banco_atual_test

#vms criar uma classe que seria um teste unitário:
class HomeViewTest(TestCase): #testar a core/views/home.
    ## A teste case precisa de métodos chamados TEST_ALGUMACOISA:
    #cada teste é uma função
    def test_home_status_code(self):
        client = Client()
        response = client.get(reverse('core:home'))#o nome da url a ser testada
        self.assertEqual(response.status_code, 200)#podemos criar varios asserts dentro de uma msm função

    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')#testa templates que são usados
        self.assertTemplateUsed(response, 'base.html')
        #testamos ambos pq um é herdado do outro