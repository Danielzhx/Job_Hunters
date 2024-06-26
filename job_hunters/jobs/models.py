from django.db import models
from companies.models import Company
from signup.models import Individual
from django_countries.fields import CountryField


# Create your models here.
class JobType(models.Model):
    job_type = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.job_type)


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.category)


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=200)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    due_date = models.DateField("Due date")
    start_date = models.DateField("Start date")

    def __str__(self) -> str:
        return f"{self.title}, {self.company}"


class Application(models.Model):
    user = models.ForeignKey(Individual, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)
    house_number = models.IntegerField()
    city = models.CharField(max_length=200)
    country = CountryField(blank_label="Country")
    postal = models.IntegerField()
    cover_letter = models.TextField(max_length=1000)
    status = models.TextField(default="Pending",max_length=200)

    class Meta:
        unique_together = ("user", "job")


class References(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    contact_bool = models.BooleanField()


class Experiences(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    workplace = models.CharField(max_length=200)
    role = models.CharField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField()
