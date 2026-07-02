from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.address.models import Address
from apps.city.models import City
from apps.country.models import Country
from apps.state.models import State


User = get_user_model()


class AddressViewSetTests(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Pakistan", description="Country")
        self.state = State.objects.create(
            country=self.country,
            name="Punjab",
            description="State",
        )
        self.city = City.objects.create(
            state=self.state,
            name="Lahore",
            description="City",
        )
        self.user = User.objects.create_user(
            username="demo",
            email="demo@example.com",
            password="StrongPass123!",
            is_email_verified=True,
        )
        self.address = Address.objects.create(
            permanent_address="123 Main St",
            residential_address="Apartment 4",
            country=self.country,
            state=self.state,
            city=self.city,
            postal_code="54000",
            user=self.user,
        )

    def test_owner_can_patch_their_own_address(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            f"/address/{self.address.id}/",
            {
                "permanent_address": "456 New Street",
                "postal_code": "54001",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.address.refresh_from_db()
        self.assertEqual(self.address.permanent_address, "456 New Street")
        self.assertEqual(self.address.postal_code, "54001")
