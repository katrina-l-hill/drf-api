from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Food

# Create your tests here.


class FoodTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_food = Food.objects.create(
            name="Twix",
            purchaser=testuser1,
            description="Left or right?",
        )
        test_food.save()

    def test_food_model(self):
        food = Food.objects.get(id=1)
        actual_purchaser = str(food.purchaser)
        actual_name = str(food.name)
        actual_description = str(food.description)
        self.assertEqual(actual_purchaser, "testuser1")
        self.assertEqual(actual_name, "Twix")
        self.assertEqual(actual_description, "Left or right?")

    def test_get_food_list(self):
        url = reverse("food_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food = response.data
        self.assertEqual(len(food), 1)
        self.assertEqual(food[0]["name"], "Twix")

    def test_get_food_by_id(self):
        url = reverse("food_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food = response.data
        self.assertEqual(food["name"], "Twix")

    def test_create_food(self):
        url = reverse("food_list")
        data = {
            "purchaser": 1,
            "name": "Kit Kat",
            "description": "Gotta eat it layer by layer",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        food = Food.objects.all()
        self.assertEqual(len(food), 2)
        self.assertEqual(Food.objects.get(id=2).name, "Kit Kat")

    def test_update_food(self):
        url = reverse("food_detail", args=(1,))
        data = {
            "purchaser": 1,
            "name": "Gyoza",
            "description": "Pan fried is the best.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food = Food.objects.get(id=1)
        self.assertEqual(food.name, data["name"])
        self.assertEqual(food.purchaser.id, data["purchaser"])
        self.assertEqual(food.description, data["description"])

    def test_delete_food(self):
        url = reverse("food_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        food = Food.objects.all()
        self.assertEqual(len(food), 0)
