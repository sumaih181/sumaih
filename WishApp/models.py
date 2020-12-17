from datetime import datetime, timedelta
import re
import bcrypt
from django.db import models

# import datetime
# datetime.datetime

class UserManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        # check email in db
        user_list = User.objects.filter(email=post_data['email'])
        if len(user_list) == 0:
            # errors['username'] = 'email not found'
            errors['email'] = 'There was a problem'

        # check password

        elif not bcrypt.checkpw(
            post_data['password'].encode(),  # from the form
            user_list[0].hashed_password.encode()  # from the db
        ):
            # errors['password'] = 'Password did not match'
            errors['password'] = 'There was a problem'
        return errors

    def register_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # check first_name
        if len(post_data['first_name']) < 5:
            errors['first_name'] = 'first_name must be longer than 8 characters'
        
        if len(post_data['last_name']) < 5:
            errors['last_name'] = 'last_name must be longer than 8 characters'
        # check password
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid Email'
        
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be longer than 8 characters'

        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Password does not match'

        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = 'email taken'


        return errors

class WishManager(models.Manager):

    def add_wish_validator(self,post_data):
        errors={}
        if len(post_data['name']) < 3:
            errors['name'] = 'Wish must be at least 3 characters!'
        if len(post_data['desc']) < 3:
            errors['desc'] = 'Description must be at least 3 characters!'

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=255)
    # games_uploaded  = wishes_uploaded
    # favorites
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Wish(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        User, related_name='wishes_uploaded', on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name='favorites')
    granted = models.BooleanField(default=False)
    desc = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()