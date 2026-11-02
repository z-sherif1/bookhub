import requests
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Favorite,ReadingListItem,Review


# Api link
API_URL = "https://openlibrary.org/search.json"

HEADERS = { "User-Agent": "BookHub/1.0 (zeyadaboali1138@gmial.com)" }

def books(request):
    query = request.GET.get('q', "").strip()
    if query:
        search_query = query
    else:
        search_query = "the hobbit"

    books = []

    try:
        response = requests.get(
            API_URL,
            params={
                "q" : search_query,
                'limit' : 10,
                'fields' : "key,title,author_name,cover_i,first_publish_year"
            },
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        books = data.get('docs',[])
    except (requests.RequestException, ValueError):
        books =[]

    context = {
        'books':books,
        'query': query,
        'api_error' : not books
    }
    return render(request, 'bookhub/home.html', context)
        


def book_detail(request, book_id):
    url = f"https://openlibrary.org/works/{book_id}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        book = response.json()
        book["key"] = f"/works/{book_id}"

    except (requests.RequestException, ValueError) as e:
        print("Book detail API error:", e)
        book = None

    return render(
        request,
        "bookhub/book_detail.html",
        {"book": book}
    )


@login_required
def add_favorite(request, book_id):
    url = f"https://openlibrary.org/works/{book_id}.json"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as e:
        print("Add favorite API error:", e)
        return redirect("book_detail", book_id=book_id)

    description = data.get("description", "")
    if isinstance(description, dict):
        description = description.get("value", "")

    cover_image_url = ""
    if data.get("covers"):
        cover_image_url = (
            f"https://covers.openlibrary.org/b/id/"
            f"{data['covers'][0]}-L.jpg"
        )

    book, created = Book.objects.get_or_create(
        open_library_id=f"/works/{book_id}",
        defaults={
            "title": data.get("title", "Unknown title"),
            "authors": "",
            "description": description,
            "published_date": data.get("first_publish_date", ""),
            "cover_image_url": cover_image_url,
        }
    )

    Favorite.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect("book_detail", book_id=book_id)

@login_required
def favorites(request):
    favorite_books = Favorite.objects.filter(user=request.user)
    context = {'favorite_books':favorite_books}
    return render(request , 'bookhub/favorites.html', context)

@login_required
def remove_favorite(request, book_id):
    book_key = f"/works/{book_id}"
    book = get_object_or_404(Book, open_library_id=book_key)
    Favorite.objects.filter(user=request.user, book=book).delete()
    return redirect("favorites")


@login_required
def reading_list_view(request):
    user_items = ReadingListItem.objects.filter(user=request.user)
    context = {'reading_items': user_items}
    return render(request, 'bookhub/reading_list.html', context)

@login_required
def update_reading_list(request, book_id):
    if request.method == "POST":
        status = request.POST.get("status")
        url = f"https://openlibrary.org/works/{book_id}.json"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return redirect("book_detail", book_id=book_id)

        description = data.get("description", "")
        if isinstance(description, dict):
            description = description.get("value", "")

        cover_image_url = ""
        if data.get("covers"):
            cover_image_url = f"https://covers.openlibrary.org/b/id/{data['covers'][0]}-L.jpg"

        book, created = Book.objects.get_or_create(
            open_library_id=f"/works/{book_id}",
            defaults={
                "title": data.get("title", "Unknown title"),
                "authors": "",
                "description": description,
                "published_date": data.get("first_publish_date", ""),
                "cover_image_url": cover_image_url,
            }
        )

        ReadingListItem.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={"status": status}
        )
    return redirect("book_detail", book_id=book_id)


@login_required
def add_review(request, book_id):
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")
        
        url = f"https://openlibrary.org/works/{book_id}.json"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return redirect("book_detail", book_id=book_id)

        description = data.get("description", "")
        if isinstance(description, dict):
            description = description.get("value", "")

        cover_image_url = ""
        if data.get("covers"):
            cover_image_url = f"https://covers.openlibrary.org/b/id/{data['covers'][0]}-L.jpg"

        book, created = Book.objects.get_or_create(
            open_library_id=f"/works/{book_id}",
            defaults={
                "title": data.get("title", "Unknown title"),
                "authors": "",
                "description": description,
                "published_date": data.get("first_publish_date", ""),
                "cover_image_url": cover_image_url,
            }
        )
        
        Review.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={"rating": rating, "comment": comment}
        )
    return redirect("book_detail", book_id=book_id)


def book_reviews(request, book_id):
    book_key = f"/works/{book_id}"
    book = get_object_or_404(Book, open_library_id=book_key)
    reviews = Review.objects.filter(book=book).order_by('-created_at')
    
    context = {
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'bookhub/book_reviews.html', context)