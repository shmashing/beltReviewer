from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse
from ..users.models import *
# Create your views here.

def user_page(request):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']

      else:
        return redirect('users:index')

    except:
      return redirect('users:index')
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
      'user': user,
      'reviews': Review.objects.all().order_by('-created_at')[:3],
      'books': Book.objects.all().order_by('title')
    }
    return render(request, 'books/user_page.html', context)

def add_book(request):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']

      else:
        return redirect('users:index')

    except:
      return redirect('users:index')

    context = {
      'authors': Author.objects.all().order_by('name'),
    }

    return render(request, 'books/add_book.html', context)

def make_book(request):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']
      else:
        return redirect('users:index')

    except:
      return redirect('users:index')

    book_validation = Book.objects.bookKnit(dict(request.POST.items()), User.objects.get(id=user_id))

    if(book_validation['isValid']):
      return redirect('books:home')
    else:
      return redirect('books:add')

def book_page(request, id):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']

      else:
        return redirect('users:index')

    except:
      return redirect('users:index')

    book = Book.objects.get(id=id)
    context = {
      'book': book,
      'reviews': Review.objects.filter(book_id=id).order_by('-created_at'),
      'user': User.objects.get(id=user_id),
      'avg_rating': book.getAvgRating(),
    }
 
    return render(request, 'books/book_page.html', context)
  
def add_review(request, id):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']
      else:
        return redirect('users:index')

    except:
      return redirect('users:index')

    if(request.POST['review'] != ''):
      review=Review.objects.makeReview(request.POST['review'], request.POST['rating'], User.objects.get(id=user_id), Book.objects.get(id=id))
    else:
      messages.add_message(request, messages.INFO, 'Please fill in a review!')

    return redirect(reverse('books:bookPage', kwargs={'id':id}))

def add_like(request, book_id, rev_id):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']
      else:
        return redirect('users:index')

    except:
      return redirect('users:index')


    like=Like.objects.makeLike(Review.objects.get(id=rev_id), User.objects.get(id=user_id))

    return redirect(reverse('books:bookPage', kwargs={'id':book_id}))

def remove_review(request, book_id, rev_id):
    try:
      if(request.session['user_logged']):
        user_id = request.session['user_id']
      else:
        return redirect('users:index')

    except:
      return redirect('users:index')


    try:
      print('~~~~~~~~~~~~~~~~~~in try~~~~~~~~~~~~~~~~')
      Review.objects.get(id=rev_id).delete()

    except:
      print('~~~~~~~~~~~~~~~~~~in except~~~~~~~~~~~~~~~~')
      messages.add_message(request, messages.INFO, 'Could not delete review')
   
    return redirect(reverse('books:bookPage', kwargs={'id':book_id}))
