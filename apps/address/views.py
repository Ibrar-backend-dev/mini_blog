from rest_framework import permissions,status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Address.objects.select_related('country', 'state', 'city')

    serializer_class = AddressSerializer

# If listing, return only the current user's address (or none)
    def get_queryset(self):

        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and user.address_id:
            return Address.objects.filter(id=user.address_id).select_related('country', 'state', 'city')
        
        return Address.objects.none()
# link to user (user has FK to Address)
    def perform_create(self, serializer):

        address = serializer.save()
        user = self.request.user
        user.address = address
        user.save(update_fields=["address"])

    def perform_update(self, serializer):
        """Ensure user can only update their own addresses"""
        address = self.get_object()
        if address.id == self.request.user.address_id:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update this address.")

    def perform_destroy(self, instance):

        if instance.id == self.request.user.address_id:
            user = self.request.user
            user.address = None
            user.save(update_fields=["address"])
            instance.delete()
        else:
            raise PermissionDenied("You don't have permission to delete this address.")
