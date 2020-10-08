from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerRating(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')
    title = TitleSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Review
        validators = []

    def validate(self, data):
        if self.context['view'].action == 'create':
            title = get_object_or_404(Title, pk=self.context['view'].kwargs[
                'title_id'])
            user = self.context['request'].user

            if Review.objects.filter(author=user).filter(title=title).exists():
                raise serializers.ValidationError("Uniq error")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("first_name", "last_name",
                  "username", "bio", "email", "role")
        model = User


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)
