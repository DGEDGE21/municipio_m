from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return False

        # Verifica se o usuário pertence ao grupo "admin"
        return request.user.groups.filter(name='Admin').exists()

