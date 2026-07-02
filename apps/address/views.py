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
        if user and user.is_authenticated:
            return Address.objects.filter(user=user).select_related('country', 'state', 'city')

        return Address.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure user can only update their own addresses"""
        address = self.get_object()
        if address.user_id == self.request.user.id:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to update this address.")

    def perform_destroy(self, instance):

        if instance.user_id == self.request.user.id:
            instance.delete()
        else:
            raise PermissionDenied("You don't have permission to delete this address.")
