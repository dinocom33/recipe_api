"""
Views for the recipe API.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


@extend_schema(tags=['Recipe'])
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""

        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class."""

        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""

        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""

        return self.queryset.filter(user=self.request.user).order_by('-name')


@extend_schema(tags=['Tag'])
class TagViewSet(BaseRecipeAttrViewSet):
    """View for manage tag APIs."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


@extend_schema(tags=['Ingredient'])
class IngredientViewSet(BaseRecipeAttrViewSet):
    """View for manage ingredient APIs."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
