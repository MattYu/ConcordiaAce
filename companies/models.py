from django.db import models

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length = 100, default= "")

    def __str__(self):
        return self.company_name