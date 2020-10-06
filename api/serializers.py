from rest_framework import serializers

from .models import Category, Comments, Genre, Reviews, Title, User


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
    rating = serializers.SerializerMethodField()

    def get_rating(self, Title):
        return Title.rating

    class Meta:
        fields = ('id', 'category', 'genre', 'name',
                  'year', 'description', 'rating')
        model = Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True,
                                          slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


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
