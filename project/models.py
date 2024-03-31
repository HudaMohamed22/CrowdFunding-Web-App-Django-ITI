from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from users.models import CustomUser
from django.shortcuts import reverse,get_object_or_404
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
    featured_at = models.DateTimeField(default=None, null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_DEFAULT, default=None, related_name="projects")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    tag = models.ManyToManyField(Tag ,blank=True, related_name="projects")

    def __str__(self):
        return self.title
    
    def get_image_urls(self):
        return [image.image.url for image in self.images.all()]
    
    @classmethod
    def get_project_by_id(cls, id):
        return get_object_or_404(cls, id=id)
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
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.donation   
    
    
# ***************************** Rate **********************
class Rate(models.Model):
    rate = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.rate  
    @classmethod
    def create_rate(cls, rate_value, project_instance, user_instance=None):
        try:
            rate = cls(rate=rate_value, project=project_instance, user=user_instance)
            rate.save()
        except Exception as e:
            print(e)
            return False
        else:
            return rate
    

# ***************************** Comment **********************
class Comment(models.Model):
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return str(f'comment by {self.user.first_name} {self.user.last_name}  on {self.project.title} project.')
    @property
    def show_url(self):
        url = reverse('project_details', args=[self.id])
        return url    
    
# ***************************** Project_Report **********************
class Project_Report(models.Model):
    reason = models.TextField(default="No Reason Provided")
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='Project_Reports')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Project_Reports')

# ***************************** Comment_Report **********************
class Comment_Report(models.Model):
    reason = models.TextField(default="Abused Comment",null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='Comment_Reports')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Comment_Reports')    