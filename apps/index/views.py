from django.shortcuts import render, HttpResponse, redirect
from .models import User, Author, Book, Review
from django.contrib import messages
from django.conf.urls.static import static


def index(request):
  return render(request, "index/index.html")

def login(request):
  if request.method == "POST":
    try:
      result = User.objects.login_validator(request.POST)
      if "success" in result:
        request.session["user_id"] = result["success"].id
        request.session["user_first_name"] = result["success"].first_name
        messages.add_message(request, messages.SUCCESS, 'Log in successful', extra_tags="log_in")
        return redirect("/books/view/")
      else:
        messages.add_message(request, messages.ERROR, 'Invalid login credentials', extra_tags="invalid_login")
        return redirect("/")
    except:
      messages.add_message(request, messages.ERROR, 'Invalid login credentials', extra_tags="invalid_login")
      return redirect("/")
  else:
    return redirect("/")

def register(request):
  if request.method == "POST":
    try:    
      result = User.objects.registration_validator(request.POST)
      if "success" in result:
        request.session["user_id"] = result["success"].id
        request.session["user_first_name"] = result["success"].first_name
        messages.add_message(request, messages.SUCCESS, 'Registration successful', extra_tags="registration")
        return redirect('/books/view/')
      else:
        for key, value in result.items():
          messages.error(request, value, extra_tags=key)
        return redirect('/')
    except:
      pass

  return redirect("/")

def logout(request):
  request.session.clear()
  messages.add_message(request, messages.SUCCESS, 'Logout successful', extra_tags="log_out")
  return redirect("/")

def view_books(request):
  context = {
    # "all_books":Book.objects.values_list("title", flat=True).distinct(),
    "all_books":Book.objects.all(),
    "first_three_reviews":Review.objects.all().order_by('-created_at')[:3],
  }
  return render(request, "index/books.html", context)

def add_book(request):
  return render(request, "index/add_book.html")

def book_details(request,id):
  context = {
    "book": Book.objects.get(id=id),
    "reviews": Review.objects.filter(book=Book.objects.get(id=id))
  }
  request.session["book_id"] = id
  return render(request, "index/book_details.html", context)

def user_details(request, id):
  request.session["reviewer_id"] = id
  context = {
    "reviewer": User.objects.get(id=id),
    "all_user_reviews": Review.objects.filter(reviewer=User.objects.get(id=request.session["user_id"]))
  }
  return render(request, "index/user_details.html", context)

def add_book_process(request):
  if len(Author.objects.filter(first_name=request.POST["first_name"],last_name=request.POST["last_name"])) == 0:
    author = Author.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"])
  else:
    author = Author.objects.filter(first_name=request.POST["first_name"],last_name=request.POST["last_name"])[0]
  if len(Book.objects.filter(title=request.POST["title"],author=author)) == 0:
    book = Book.objects.create(title=request.POST["title"],author=author)
  else:
    book = Book.objects.filter(title=request.POST["title"],author=author)[0]
  Review.objects.create(book=book,rating=request.POST["rating"],text=request.POST["review"],reviewer=User.objects.get(id=request.session["user_id"]))
  request.session["book_id"] = book.id
  return redirect("/book/details/" + str(request.session["book_id"]) + "/")

def add_book_review(request):
  if not request.POST["review"]:
    return redirect("/book/details/" + str(request.session["book_id"]) + "/")
  Review.objects.create(book=Book.objects.get(id=request.session["book_id"]), rating=request.POST["rating"], text=request.POST["review"], reviewer=User.objects.get(id=request.session["user_id"]))

  return redirect("/book/details/" + str(request.session["book_id"]) + "/")

def delete_book_review(request,id):
  Review.objects.get(id=id).delete()
  return redirect("/book/details/" + str(request.session["book_id"]) + "/")
