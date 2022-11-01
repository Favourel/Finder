import json

from django.test import TestCase, Client
from .models import User, Product
from django.shortcuts import reverse

# Create your tests here.

"""
Need the test? Send me a mail on favourelodimuor16@gmail.com. I will be glad to help.

Thanks
"""


class CreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="james", email="james@gmail.com", password="top_secret"
        )
        self.client = Client()
        self.credentials = {
            "username": "favour",
            "password": "top_secret"

        }
        User.objects.create_user(**self.credentials)

    def test_create(self):
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

        response_ = self.client.post(reverse("create_store"),
                                    {
                                        "user": response.context["user"].username,
                                        "full_name": "James earl jones",
                                        "location": "London",
                                        "phone_number": 313,
                                        "about": "I am whioe",
                                        "instagram_rul": "https://instagfe.com",
                                        "twiiter_rul": "https://instagfe.com",
                                        "skills": "singinf",
                                        "education": "M.A."
                                    }, follow=True)
        # data = json.loads(response.content)
        print(response_.context.get("name"))
        self.assertEquals(response_.context["full_name"]["full_name"], "Loren ipsum text 14")
        # print(response.content.get("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/create_store.html")