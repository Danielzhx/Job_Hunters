from django.shortcuts import render, get_object_or_404
from jobs.models import Job
from django.http import HttpResponse

from .models import Category, Company, Job, JobType

# Create your views here.
def index(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/index.html',{"jobs":jobs})

def detail(request, job_id):
    job = get_object_or_404(Job, pk = job_id)
    context = {
        'job': job
    }
    return render(request, 'jobs/profile.html', context)

def apply(request, job_id):
    pass



def filter_jobs(request):
    jobs = Job.objects
    if 'category_select' in request.POST:
        jobs.filter(category = request.POST['category_select'])
    if 'company_select' in request.POST:
        jobs.filter(company = request.POST['company_select'])
    if 'full_time' in request.POST:
        jobs.filter(job_type = 0)
    if 'part_time' in request.POST:
        jobs.filter(job_type = 1)
    if 'internship' in request.POST:
        jobs.filter(job_type = 2)

def index2(request):
    context = {
        "categories": Category.objects,
        "companies": Company.objects
               }
    jobs = Job.objects
    if 'category_select' in request.POST:
        jobs.filter(category = request.POST['category_select'])
    if 'company_select' in request.POST:
        jobs.filter(company = request.POST['company_select'])
    if 'full_time' in request.POST:
        jobs.filter(job_type = 0)
    if 'part_time' in request.POST:
        jobs.filter(job_type = 1)
    if 'internship' in request.POST:
        jobs.filter(job_type = 2)

    return render(request, 'jobs/index.html', context)
