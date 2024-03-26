from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.shortcuts import get_object_or_404
# Create your models here.

def get_current_date():
    return timezone.now().date()




# *************************** Category ******************************
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def get_all_categories(cls):
        return cls.objects.all()
    
    @classmethod
    def get_category_by_id(cls, id):
        return get_object_or_404(cls, id=id)
    
# **************************** Tag **********************************
class Tag(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name
    
    
# ************************** Project **********************************
class Project(models.Model):
    title = models.CharField(max_length=250,unique=True)
    details = models.TextField(default="No Details Provided")
    total_target = models.FloatField()
    start_date = models.DateField(default=get_current_date)
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField(default=0,null=True)
    current_donation = models.FloatField(default=0,null=True)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    tag = models.ManyToManyField(Tag ,blank=True, related_name="projects")

    def __str__(self):
        return self.title
    
    @property
    def image_url(self):
        picture = self.images.first()
        if picture:
            return picture.image.url
    
# ************************** Picture ***********************
class Picture(models.Model):
    image = models.ImageField(upload_to='project/images/',null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"/media/{self.image}"
    

        
# **************************  Donation  ***********************
class Donation(models.Model):
    donation = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.donation   
    
    
# ***************************** Rate **********************
class Rate(models.Model):
    rate = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.rate   
    