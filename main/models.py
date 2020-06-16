from django.db import models
from datetime import datetime
# Create your models here.

#Tutorial is inheriting attributes from Model in models library, have to pass this
#Tutorial is table with these as columns 
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length= 200) #short blurbs
    tutorial_content = models.TextField() #Blog, long stuff
    tutorial_published = models.DateTimeField('date published', default = datetime.now())

    def __str__(self):
        return self.tutorial_title