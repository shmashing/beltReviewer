from __future__ import unicode_literals
from django.db import models
from ..users.models import *

# Create your models here.
class AuthorManager(models.Manager):
  def authorValidation(self, name):
    author_name = name
    
    try:
      author = Author.objects.get(name=author_name)
    except:
      author = Author.objects.create(name=author_name)

    return author

  def getAuthor(self, name):
    try:
      author = Author.objects.get(name=name)
      return author

    except:
      return


class BookManager(models.Manager):
  def bookKnit(self, postData, user):
    book_validation = {
      'isValid': True,
      'errors': [],
      'book': None,
    }

    if(postData['author_name'] != ''):
      author = Author.objects.authorValidation(postData['author_name'])
 
    elif(postData['author_name_list'] != ''):
      author = Author.objects.getAuthor(postData['author_name_list'])

    else:
      book_validation['isValid'] = False
      book_validation['errors'].append('Please enter an author!')
      author = None

    book_title = postData['book_title']

    if(author):
      try:
        book = Book.objects.get(title=book_title)
       
        if(book.author.id == author.id):
          book_validation['isValid']=False
          book_validation['error'] = "Book already exists bruh."
          return book_validation
    
        book_validation['book'] = Book.objects.create(title=book_title, author=author)         
        review = Review.objects.makeReview(postData['review'], postData['rating'], user, book_validation['book'])
  
      except:
        book = Book.objects.create(title=book_title, author = author)
        book_validation['book'] = book
        review = Review.objects.makeReview(postData['review'], postData['rating'], user, book_validation['book'])        

    return book_validation

class ReviewManager(models.Manager):
  def makeReview(self, content, rating, user, book):
    try:
      review=Review.objects.create(content=content, rating=rating, book=book, user=user)

    except:
      return None
    
    return review

class LikeManager(models.Manager):
  def makeLike(self, review, user):
    try:

      if(self.checkUserLike(user, review)):
        return None

      else:
        like=Like.objects.create(review=review, user=user)

    except:
      return None

    return like

  def checkUserLike(self, user, review):
    like = Like.objects.filter(user_id=user.id).filter(review_id=review.id)
    if(len(like)>0):
      return True

    else:
      return False

class Author(models.Model):
  name = models.CharField(max_length=100)
  objects = AuthorManager()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
 
class Book(models.Model):
  title = models.CharField(max_length=100)
  author = models.ForeignKey(Author, related_name='author')
  objects = BookManager()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def getAvgRating(self):
    reviews = Review.objects.filter(book_id=self.id)

    tot_rating = 0
    for i in range(len(reviews)):
      tot_rating += len(reviews[i].rating)

    count = int(tot_rating/len(reviews))
    rating = ''
    for i in range(count):
      rating += '*'

    print(rating)
    return rating

class Review(models.Model):
  content = models.TextField(max_length=255)
  rating = models.CharField(max_length=6)
  book = models.ForeignKey(Book)
  user = models.ForeignKey(User)
  objects = ReviewManager()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def getLikes(self):
    likes = Like.objects.filter(review_id=self.id)

    user_ids = []
    for like in likes:
      user_ids.append(like.user.id)

    return user_ids    

class Like(models.Model):
  review = models.ForeignKey(Review)
  user = models.ForeignKey(User)
  objects = LikeManager()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


