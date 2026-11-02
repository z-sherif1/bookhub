from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Favorite, ReadingListItem, Review
from .serializers import FavoriteSerializer, ReadingListItemSerializer, ReviewSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_favorite(request):
    open_library_id = request.data.get('open_library_id')
    if not open_library_id:
        return Response({'error': 'open_library_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    book, created = Book.objects.get_or_create(
        open_library_id=open_library_id,
        defaults={
            'title': request.data.get('title', 'Unknown Title'),
            'authors': request.data.get('authors', ''),
            'description': request.data.get('description', ''),
            'published_date': request.data.get('published_date', ''),
            'cover_image_url': request.data.get('cover_image_url', '')
        }
    )

    favorite, created_fav = Favorite.objects.get_or_create(user=request.user, book=book)
    if created_fav:
        return Response({'message': 'Added to favorites successfully'}, status=status.HTTP_201_CREATED)
    return Response({'message': 'Already in favorites'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_remove_favorite(request, book_id):
    book_key = f"/works/{book_id}"
    try:
        book = Book.objects.get(open_library_id=book_key)
        Favorite.objects.filter(user=request.user, book=book).delete()
        return Response({'message': 'Removed from favorites successfully'}, status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_reading_list(request):
    items = ReadingListItem.objects.filter(user=request.user)
    serializer = ReadingListItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_update_reading_list(request):
    open_library_id = request.data.get('open_library_id')
    status_val = request.data.get('status', 'WANT_TO_READ')
    
    if not open_library_id:
        return Response({'error': 'open_library_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    book, created = Book.objects.get_or_create(
        open_library_id=open_library_id,
        defaults={
            'title': request.data.get('title', 'Unknown Title'),
            'authors': request.data.get('authors', ''),
            'description': request.data.get('description', ''),
            'published_date': request.data.get('published_date', ''),
            'cover_image_url': request.data.get('cover_image_url', '')
        }
    )

    item, created = ReadingListItem.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={'status': status_val}
    )
    return Response({'message': 'Reading list updated successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def api_book_reviews(request, book_id):
    book_key = f"/works/{book_id}"
    try:
        book = Book.objects.get(open_library_id=book_key)
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response([], status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_review(request, book_id):
    book_key = f"/works/{book_id}"
    book, created = Book.objects.get_or_create(
        open_library_id=book_key,
        defaults={
            'title': request.data.get('title', 'Unknown Title'),
            'authors': '',
            'description': '',
            'published_date': '',
            'cover_image_url': ''
        }
    )
    
    rating = request.data.get('rating')
    comment = request.data.get('comment', '')

    if not rating:
        return Response({'error': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)

    review, created = Review.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={'rating': rating, 'comment': comment}
    )
    return Response({'message': 'Review added successfully'}, status=status.HTTP_201_CREATED)