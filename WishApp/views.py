import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register_user(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
            password.encode(),  # pw to hash
            bcrypt.gensalt()  # generated salt bae
        ).decode()  # create the hash
        print(hash_browns)
        created_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            hashed_password=hash_browns
        )
        request.session['uuid'] = created_user.id

        return redirect('/wishes')


def show_wishes(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'all_wishes_granted': Wish.objects.filter(granted=True),
        'all_wishes_not_granted': Wish.objects.filter(granted=False),
    }
    return render(request, 'wishes.html', context)


def logout_user(request):
    del request.session['uuid']
    # request.session.flush()
    return redirect('/')


def login_user(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['uuid'] = user.id
        return redirect('/wishes')    


def Make_a_wish(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
    }
    return render(request, 'Make_a_wish.html',context)




def create_wish(request):
    # TODO add validation
    errors = Wish.objects.add_wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/Make_a_wish')
    else:
        logged_in_user = User.objects.get(id=request.session['uuid'])
        Wish.objects.create(
            name=request.POST['name'],
            desc=request.POST['desc'],
            uploaded_by=logged_in_user
        )
        print('Created a wish!')
        return redirect('/wishes')


def mark_wish_granted(request, wish_id):
    # update
    wish = Wish.objects.get(id=wish_id)
    wish.granted = True
    wish.save()
    return redirect('/wishes')


def mark_wish_as_favorite(request, wish_id):
    # get wish
    wish = Wish.objects.get(id=wish_id)
    # get user
    user = User.objects.get(id=request.session['uuid'])
    # add
    user.favorites.add(wish)
    return redirect('/wishes')


def mark_wish_as_unfavorite(request, wish_id):
    # get wish
    wish = Wish.objects.get(id=wish_id)
    # get user
    user = User.objects.get(id=request.session['uuid'])
    # add
    user.favorites.remove(wish)
    return redirect('/wishes')        


def wish_edit(request, wish_id):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'wish': Wish.objects.get(id=wish_id)
    }
    return render(request, 'wish_edit.html', context)


def wish_update(request, wish_id):
    print(request.POST)
    # run the validator
    errors = Wish.objects.add_wish_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            print(key, value)
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(f'/wishes/{wish_id}/edit')
    else:
        wish_to_update = Wish.objects.get(id=wish_id)
        wish_to_update.name = request.POST['name']
        wish_to_update.desc = request.POST['desc']
        wish_to_update.save()
        return redirect('/wishes')


def wish_remove(request, wish_id):
    Wish.objects.get(id=wish_id).delete()
    return redirect('/wishes')


def view_stats(request):
    if 'uuid' not in request.session:
            return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['uuid']),
        'all_wishes_granted': Wish.objects.filter(granted=True),
        'user_wishes_granted': Wish.objects.filter(granted=True, uploaded_by=request.session['uuid'] ),
        'user_wishes_not_granted': Wish.objects.filter(granted=False, uploaded_by=request.session['uuid']),
    }
    return render(request, 'view_stats.html', context)
