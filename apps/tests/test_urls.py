from django.test import SimpleTestCase
from django.urls import reverse, resolve

from apps.ecr.views import ActionOptionsView, EventosView, InitialConfView


class TestUrls(SimpleTestCase):

    def test_ECR_action_url_is_resolved(self):
        url = reverse('ecr_action_option')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ActionOptionsView)

    def test_init_conf_url_is_resolved(self):
        url = reverse('ecr_initial_conf')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, InitialConfView)

    def test_eventos_url_is_resolved(self):
        url = reverse('ecr_eventos')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, EventosView)
