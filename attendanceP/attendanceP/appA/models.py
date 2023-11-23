from django.db import models


# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=10)
    branch = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    parent_mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.roll_no


class data(models.Model):
    batch = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    total_classes = models.IntegerField(default=0)

    def __str__(self):
        return self.batch


class attend(models.Model):
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100, default="student")
    batch = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    total_classes = models.IntegerField(default=0)
    present_classes = models.IntegerField(default=0)
    date = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return self.roll_no
