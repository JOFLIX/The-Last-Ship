from django.db import models
from accounts.models import Courses

# Create your models here.
class IndexPage(models.Model):
    slider_one_text=models.TextField(max_length=400)
    slider_one_image=models.ImageField(upload_to='files',blank=True, null=True)
    slider_two_text=models.TextField(max_length=400)
    slider_two_image=models.ImageField(upload_to='files',blank=True, null=True)
    slider_three_text=models.TextField(max_length=400)
    slider_three_image=models.ImageField(upload_to='files',blank=True, null=True)
    welcome_message=models.TextField(max_length=200)
    director_image=models.ImageField(upload_to='files',blank=True, null=True)
    director_message=models.TextField(max_length=1500)
    video=models.FileField(upload_to="video", max_length=100,blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'CUSTOMIZE INDEX PAGE'
    class Meta:
            verbose_name = ('Index Page')
            verbose_name_plural = ('Index Pages' )


class AboutPage(models.Model):
    about_us_full_description=models.TextField(max_length=1500)
    about_us_img=models.ImageField(upload_to='files')
    gallery1=models.ImageField(upload_to='files',blank=True, null=True)
    gallery2=models.ImageField(upload_to='files',blank=True, null=True)
    gallery3=models.ImageField(upload_to='files',blank=True, null=True)
    gallery4=models.ImageField(upload_to='files',blank=True, null=True)
    gallery5=models.ImageField(upload_to='files',blank=True, null=True)
    gallery6=models.ImageField(upload_to='files',blank=True, null=True)
    gallery7=models.ImageField(upload_to='files',blank=True, null=True)
    gallery8=models.ImageField(upload_to='files',blank=True, null=True)
    gallery9=models.ImageField(upload_to='files',blank=True, null=True)
    gallery10=models.ImageField(upload_to='files',blank=True, null=True)
    gallery11=models.ImageField(upload_to='files',blank=True, null=True)
    gallery12=models.ImageField(upload_to='files',blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'CUSTOMIZE ABOUT PAGE'
    class Meta:
            verbose_name = ('About Page')
            verbose_name_plural = ('About Pages' )



class NewsEvents(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=1500)
    image=models.ImageField(upload_to='files',blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'CUSTOMIZE NEWS & EVENTS PAGE'
    class Meta:
            verbose_name = ('News & Events')
            verbose_name_plural = ('News & Events')


class MessagesFromVisitors(models.Model):
    first_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    phone=models.IntegerField()
    subject=models.CharField(max_length=50)
    message=models.TextField(max_length=100)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'MessagesFromVisitors'
    class Meta:
            verbose_name = ('Messages From Visitor')
            verbose_name_plural = ('Messages From Visitors')




class Contacts(models.Model):
    email1=models.EmailField(max_length=254)
    email2=models.EmailField(max_length=254)
    phone1=models.IntegerField(blank=True, null=True)
    phone2=models.IntegerField(blank=True, null=True)
    phone3=models.IntegerField(blank=True, null=True)
    box=models.CharField(max_length=50)
    location=models.TextField(max_length=100)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'CUSTOMIZE CONTACT PAGE'
    class Meta:
            verbose_name = ('Contact')
            verbose_name_plural = ('Contacts')


class Accreditation(models.Model):
    brief_introduction=models.TextField(max_length=1000,blank=True, null=True)
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=1000)
    image=models.ImageField(upload_to='files')
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'Customize Accreditation Page'
    class Meta:
            verbose_name = ('Accreditation')
            verbose_name_plural = ('Accreditation')


class Admission(models.Model):
    brief_introduction=models.TextField(max_length=1000,blank=True, null=True)
    title=models.CharField(max_length=50)
    description=models.TextField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'Customize Admission Page'
    class Meta:
            verbose_name = ('Admission')
            verbose_name_plural = ('Admission')



class Alumni(models.Model):
    name=models.CharField(max_length=50)
    dob=models.DateField( auto_now_add=False)
    email=models.EmailField(max_length=254,unique=True)
    phone=models.IntegerField()
    course=models.ForeignKey(Courses, on_delete=models.CASCADE)
    graduation_year=models.IntegerField()
    current_occupation=models.CharField(max_length=1000)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  'Customize Admission Page'
    class Meta:
            verbose_name = ('Alumni')
            verbose_name_plural = ('Alumni')