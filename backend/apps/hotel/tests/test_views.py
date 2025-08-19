import pytest
from django.urls import reverse
from apps.hotel.models import Hotel
from .conftest import api_client

from .factories import HotelFactory, AmenityFactory
from apps.accounts.tests.factories import UserFactory, HotelOwnerProfileFactory


@pytest.mark.django_db
class TestHotelListCreateView:
    url = reverse('hotel:api_v1:hotel-list-create')

    def test_get_hotels_list_anonymous(self, api_client):
        """Anonymous user can view the list of hotels."""
        HotelFactory(name="Test Hotel")
        response = api_client.get(self.url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Hotel'

    def test_create_hotel_by_anonymous_user_fails(self, api_client):
        """ Anonymous user cannot create a hotel."""
        amenity = AmenityFactory()
        payload = {
            "name": "New Hotel",
            "phone_number": "1234567890",
            "email": "new@hotel.com",
            "amenities": [amenity.id]
        }
        response = api_client.post(self.url, payload, format='json')
        assert response.status_code == 401

    def test_create_hotel_by_authenticated_user_fails(self, api_client):
        """Authenticated regular user cannot create a hotel (due to permissions)."""
        user = UserFactory(role='customer')
        api_client.force_authenticate(user=user)
        amenity = AmenityFactory()
        payload = {
            "name": "New Hotel",
            "phone_number": "1234567890",
            "email": "new@hotel.com",
            "amenities": [amenity.id]
        }
        response = api_client.post(self.url, payload, format='json')
        assert response.status_code == 403

    def test_create_hotel_by_unverified_hotel_owner_fails(self, api_client):
        """Unverified hotel owner cannot create a hotel."""
        unverified_profile = HotelOwnerProfileFactory(is_verified=False)
        api_client.force_authenticate(user=unverified_profile.user)
        amenity = AmenityFactory()
        payload = {
            "name": "Unverified Owner's Hotel",
            "phone_number": "1234567890",
            "email": "ownerunverified@hotel.com",
            "amenities": [amenity.id]
        }
        response = api_client.post(self.url, payload, format='json')
        assert response.status_code == 403

    def test_create_hotel_by_hotel_owner_succeeds(self, api_client):
        """Verified hotel owner can create a new hotel."""
        verified_profile = HotelOwnerProfileFactory(is_verified=True)
        amenity = AmenityFactory()
        api_client.force_authenticate(user=verified_profile.user)
        payload = {
            "name": "Owner's Hotel",
            "phone_number": "0987654321",
            "policy": "No pets allowed",
            "email": "owner@hotel.com",
            ""
            "amenities": [amenity.id]
        }
        response = api_client.post(self.url, payload, format='json')
        assert response.status_code == 201
        assert Hotel.objects.filter(name="Owner's Hotel").exists()


@pytest.mark.django_db
class TestHotelDetailView:
    """
    Tests for hotel detail view:
    - Anonymous user can view hotel details.
    - Authenticated user can view hotel details.
    - Hotel owner can delete their own hotel.
    - Non-owner cannot delete hotel.
    - Hotel owner can update their own hotel.
    - Non-owner cannot update hotel.
    """

    def test_get_hotel_detail_anonymous(self, api_client):
        """Anonymous user can view hotel details."""
        hotel = HotelFactory()
        url = reverse('hotel:api_v1:hotel-detail', kwargs={'pk': hotel.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == hotel.name

    def test_get_hotel_detail_authenticated_user(self, api_client):
        """Authenticated user can view hotel details."""
        hotel = HotelFactory()
        api_client.force_authenticate(user=UserFactory())
        url = reverse('hotel:api_v1:hotel-detail', kwargs={'pk': hotel.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['name'] == hotel.name
    def test_delete_hotel_by_owner(self, api_client):
        """Hotel owner can delete their own hotel."""
        hotel = HotelFactory()
        owner = hotel.owner
        print(f"Hotel Owner: {owner}, Authenticated User: {owner}")
        api_client.force_authenticate(user=owner)
        url = reverse('hotel:api_v1:hotel-detail', kwargs={'pk': hotel.pk})
        response = api_client.delete(url)
        print(f"Response: {response.status_code}, Data: {response.data}")
        assert response.status_code == 204
        assert not Hotel.objects.filter(pk=hotel.pk).exists()

    # def test_delete_hotel_by_another_owner(self, api_client):
    #     """Hotel owner cann't delete threir own hotel."""
    #     hotel = HotelFactory()
    #     owner = HotelOwnerProfileFactory(is_verified=True).user
    #     api_client.force_authenticate(user=owner)
    #     url = reverse('hotel:api_v1:hotel-detail', kwargs={'pk': hotel.pk})
    #     response = api_client.delete(url)
    #     assert response.status_code == 403
    #     # Ensure hotel still exists
    #     assert Hotel.objects.filter(pk=hotel.pk).exists()

    def test_delete_hotel_by_non_owner_fails(self, api_client):
        """Non-owner cannot delete hotel."""
        hotel = HotelFactory()
        api_client.force_authenticate(user=UserFactory())
        url = reverse('hotel:api_v1:hotel-detail', kwargs={'pk': hotel.pk})
        response = api_client.delete(url)
        assert response.status_code == 403
        assert Hotel.objects.filter(pk=hotel.pk).exists()
