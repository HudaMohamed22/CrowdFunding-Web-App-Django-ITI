from django.db import models
from django.utils import timezone
# Create your models here.


# *************************** Category ******************************
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name
    
    
# **************************** Tag **********************************
class Tag(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.name
    
    
# ************************** Project **********************************
class Project(models.Model):
    title = models.CharField(max_length=250)
    details = models.TextField()
    rate = models.FloatField()
    total_target = models.FloatField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    current_donation = models.IntegerField()
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects")
    # owner = models.ForeignKey(, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag,null=True, blank=True, related_name="projects")

    def __str__(self):
        return self.title
    
    
# ************************** Picture ***********************
class Picture(models.Model):
    image = models.ImageField(upload_to='project/images/',null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"/media/{self.image}"
    

# ************************** Donation  ***********************
class Donation(models.Model):
    donation = models.FloatField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.donation   
    
    
# ***************************** Rate **********************
class Rate(models.Model):
    rate = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rates')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.rate   
    
