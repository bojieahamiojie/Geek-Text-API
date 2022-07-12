from dataclasses import field
import imp
from pickle import FRAME
from xmlrpc.client import ResponseError
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from .models import Books, Authors, Comments, Payment, Profile, Ratings
from .serializers import BooksSerializers, AuthorsSerializers, CommentsSerializers, RatingsSerializers, ProfileSerializers, PaymentSerializers

# Create your views here.
def welcomePage(request):
    if request.method == 'GET':
        return JsonResponse('Welcome to Group 10\'s bookstore API!', safe = False)

@api_view(['GET'])
def getBooks(request):
    if request.method == 'GET':
        books = Books.objects.all()
        books_serializer = BooksSerializers(books, many = True)
        return JsonResponse(books_serializer.data, safe= False)
        
@api_view(['POST'])
def createBook(request):
    if request.method == 'POST':
        books_serializer = BooksSerializers(data = request.data)
        if books_serializer.is_valid():
            books_serializer.save()
            return Response(books_serializer.data, status = status.HTTP_201_CREATED)
        
@api_view(['GET'])     
def bookISBN(request, ISBN):
    try:
        book = Books.objects.get(pk=ISBN)
    except Books.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        books_serializer = BooksSerializers(book)
        return Response(books_serializer.data)
        
    
@api_view(['GET'])
def getAuthors(request):
    if request.method == 'GET':
        authors = Authors.objects.all()
        authors_serializer = AuthorsSerializers(authors, many = True)
        return JsonResponse(authors_serializer.data, safe= False)
    
        
@api_view(['POST'])
def createAuthor(request):
    if request.method == 'POST':
        authors_serializer = AuthorsSerializers(data = request.data)
        print(authors_serializer)
        if authors_serializer.is_valid():
            authors_serializer.save()
            return Response(authors_serializer.data, status = status.HTTP_201_CREATED)
   
@api_view(['GET'])     
def booksByAuthor(request, author):
    try:
        books = Books.objects.all()
    except Books.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    
    if request.method == 'GET':
        books_serializer = BooksSerializers(books)
        return Response(books_serializer.data)

@api_view(['GET'])
def getAverageRating(request, ISBN):

    ratings = Ratings.objects.filter(ISBN_RATINGS = ISBN)
    rating_serializer = RatingsSerializers(data=ratings, fields='rating')
    counter = 0
    ratingTotal = 0
    for rating in rating_serializer:
        counter+= 1
        ratingTotal += int(rating.get('rating'))
    return Response(ratingTotal/float(counter))

@api_view(['POST'])
def rateBook(request):

    # print(request.data)
    rating_serializer = RatingsSerializers(data=request.data)
    # print(rating_serializer)
    rating_serializer.is_valid()
    print(rating_serializer.errors)
    if rating_serializer.is_valid():
        print('Rating added')
        rating_serializer.save()
        return Response('Rating added succesfully')

@api_view(['POST'])
def commentBook(request):
    
    # print(request.data)
    comment_serializer = CommentsSerializers(data=request.data)
    # print(comment_serializer)
    comment_serializer.is_valid()
    print(comment_serializer.errors)
    if comment_serializer.is_valid():
        print('Comment added')
        comment_serializer.save()
        return Response('Comment added succesfully')

@api_view(['Get'])
def getCommentsAndRatings(request, ISBN):
    
    print(request.data)
    comments = Comments.objects.all().filter(ISBN_COMMENTS = ISBN).order_by('commentDate')
    ratings = Ratings.objects.all().filter(ISBN_RATING = ISBN).order_by('rating')
    comments_serializer = CommentsSerializers(comments)
    rating_serializer = RatingsSerializers(ratings)

    if(comments_serializer.is_valid() and rating_serializer.is_valid()):
        return Response(comments_serializer.data, rating_serializer.data)

@api_view(['POST'])
def createProfile(request):
    if request.method == 'POST':
        print(request.data)
        profile_serializer = ProfileSerializers(data=request.data)
        print(profile_serializer)
        if profile_serializer.isvalid():
            print('Profile has been made for this user')
            profile_serializer.save()
            return Response('Profile created successfully')

@api_view(['GET'])     
def getProfile(request, username):
    try:
        profile = Profile.objects.get(pk=username)
    except Profile.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        profile_serializer = ProfileSerializers(profile)
        return Response(profile_serializer.data)

@api_view(['POST'])
def createPayment(request):
    if request.method == 'POST':
        print(request.data)
        payment_serializer = PaymentSerializers(data=request.data)
        print(payment_serializer)
        if payment_serializer.isvalid():
            print('Payment method has been added to this user')
            payment_serializer.save()
            return Response('Payment created successfully')

@api_view(['GET'])
def paymentByUser(request):
    if request.method == 'GET':
        profile_username = JSONParser().parse(request)
        payment_profile = Payment.objects.filter(username_creditCard = profile_username)
        payment_serializer = PaymentSerializers(data=payment_profile)
        return JsonResponse(JSONParser().parse(payment_serializer))
