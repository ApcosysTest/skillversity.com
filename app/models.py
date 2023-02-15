from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    forgot_password_token = models.CharField(max_length=100, null=True)
    phone = models.CharField(unique=True, max_length=10)
    def __str__(self):
        return self.name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_username(self):
        return self.user.username

class Contact(models.Model):  
    name = models.CharField(max_length=20)  
    email = models.EmailField(unique=True)  
    contact = models.CharField(max_length=15, unique=True)  
    textarea = models.CharField(max_length=500)   
        
    def __str__(self):
        return self.name

class Investor(models.Model):  
    name = models.CharField(max_length=20)  
    email = models.EmailField()  
    contact = models.CharField(max_length=10)
    textarea = models.CharField(max_length=500)
        
    def __str__(self):
        return self.name

class Instructor(models.Model):  
    name = models.CharField(max_length=20)  
    email = models.EmailField()  
    contact = models.CharField(max_length=15) 
    textarea = models.CharField(max_length=500)  
        
    def __str__(self):
        return self.name

class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Bundle(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    silver_price = models.IntegerField()
    gold_price = models.IntegerField()
    image = models.ImageField(upload_to='bundle_img')

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

CHOICES=(
    ('No','No'),
    ('Yes', 'Yes')
)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    price = models.IntegerField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    medium = models.CharField(max_length=50)
    image = models.ImageField(upload_to='course_img')
    standalone = models.CharField(choices = CHOICES, max_length=20)
    free = models.CharField(choices = CHOICES, max_length=20)
    bundle = models.ManyToManyField(Bundle, default='Null', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Currency(models.Model):
    currency = models.CharField(max_length=50)
    equivalent_rupee = models.FloatField()

    def __str__(self):
        return self.name
