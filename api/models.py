from django.db import models

# Create your models here.
class Personal(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Profesional(models.Model):
        Personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
        
        
        def __str__(self):
            return self.name