from rest_framework import serializers
from .models import Book, Favorite, Review, ReadingListItem

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'book', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'book', 'rating', 'comment', 'created_at', 'updated_at']

class ReadingListItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = ReadingListItem
        fields = ['id', 'user', 'book', 'status', 'added_at', 'updated_at']