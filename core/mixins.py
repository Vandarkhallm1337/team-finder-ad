from django.core.exceptions import PermissionDenied


class OwnerOrAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj.owner != request.user and not request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class SelfOrAdminRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if obj != request.user and not request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
