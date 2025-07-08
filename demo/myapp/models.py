from django.db import models

class Book(models.Model):
    bookid = models.AutoField(db_column='BookID', primary_key=True)
    isbn = models.CharField(db_column='ISBN', max_length=20, unique=True)
    title = models.CharField(db_column='Title', max_length=255)
    genre = models.CharField(db_column='Genre', max_length=100, null=True, blank=True)
    description = models.TextField(db_column='Description', null=True, blank=True)
    author = models.CharField(db_column='Author', max_length=150)
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)
    stoc = models.IntegerField(db_column='Stoc')

    class Meta:
        managed = False
        db_table = 'Books'

class User(models.Model):
    userid = models.AutoField(db_column = "UserID",primary_key = True)
    firstname = models.CharField(db_column = "FirstName",max_length = 100)
    lastname = models.CharField(db_column = "LastName", max_length = 100)
    email = models.CharField(db_column = "Email", max_length = 150, unique = True)
    phone = models.CharField(db_column = "Phone", max_length = 20)
    passwordhash = models.CharField(db_column = "PasswordHash", max_length = 256)
    balance = models.DecimalField(db_column="Balance",decimal_places=2,max_digits=10)
    
    class Meta:
        managed = False
        db_table = 'Users'
    
