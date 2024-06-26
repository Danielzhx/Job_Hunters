from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Category, Company, Job, Application, Experiences, References
from signup.models import Individual
from Forms.filter_form import FilterForm, ORDERS
from Forms.application_form import ApplicationForm, ExperienceForm, ReferencesForm
from Forms.creation_forms import JobCreationForm
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.
def index(request):
    try:
        company = Company.objects.get(user_id = request.user.id)
        is_company = True
    except:
        is_company = False

    form = FilterForm(request.GET)
    context = {
        'form': form,
        "categories": Category.objects.all(),
        "companies": Company.objects.all(),
        "is_company":is_company
    }
    context['jobs'] = filter_jobs(request)
    if is_company:
        context['jobs'] = context['jobs'].filter(company = company)

    else:
        context['jobs'] = context['jobs'].filter(due_date__gte=datetime.now())

    return render(request, 'jobs/index.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = JobCreationForm(request.POST)
        try:
            company  = Company.objects.get(user_id = request.user.id)
        except:
            return redirect('/jobs/')

        try:
            category = Category.objects.get(category = request.POST["category"])
        except:
            category = Category(category = request.POST['category'])
            category.save()

        if form.is_valid():
            job = form.save(commit = False)
            job.category = category
            job.company = company
            job.save()
            
            return redirect("/jobs")

    else:
        form = JobCreationForm() 

    content = {
        "form":form
    }
    return render(request, "jobs/create.html", content) 

@login_required
def company_applications(request, job_id, company_id):
    applications = Application.objects.all()
    company = Company.objects.get(pk = company_id)
    job = Job.objects.get(pk = job_id)
    applications = applications.filter(job = job)
    applications = applications.filter(job__company = company)
    applications = applications.filter(status="Pending")
    content = {
        'applications':applications
    }
    return render(request,"applications/index.html", content)

@login_required
def company_application_details(request, job_id, company_id, application_id):
    application = Application.objects.get(pk = application_id)
    experiences = Experiences.objects.all().filter(application_id = application_id)
    references = References.objects.all().filter(application_id = application_id)
    content = {
        'application':application,
        'references':references,
        'experiences':experiences,
        'is_company': True
    }
    return render(request, "applications/details.html", content)

@login_required
def company_accept_application(request,job_id, company_id, application_id):
    try:
        company = Company.objects.get(user_id = request.user.id)
    except:
        return redirect('/jobs/')

    application = Application.objects.get(pk=application_id)
    application.status = "Accepted"
    application.save()
    return redirect("/jobs/%d/companies/%d/applications/%d"%(job_id,company_id,application_id))

@login_required
def company_deny_application(request,job_id, company_id, application_id):
    try:
        company = Company.objects.get(user_id = request.user.id)
    except:
        return redirect('/jobs/')

    application = Application.objects.get(pk=application_id)
    application.status = "Denied"
    application.save()
    return redirect("/jobs/%d/companies/%d/applications/%d"%(job_id,company_id,application_id))


def detail(request, job_id):
    """Detail view for individual job posting.
    """
    job = get_object_or_404(Job, pk=job_id)
    try:
        application = get_object_or_404(Application, user_id=request.user.id, job_id=job_id)
        applied = True
    except Http404:
        application = None
        applied = False

    try:
        company = get_object_or_404(Company, user_id=request.user.id)
        is_company = True
    except Http404:
        company = None 
        is_company = False

    context = {
        'job': job,
        'applied': applied,
        'application':application,
        'is_company':is_company,
        'company':company
    }
    return render(request, 'jobs/profile.html', context)

@login_required
def apply(request, job_id):
    """
        Application view for job posting.
    """
    try:
        individual = Individual.objects.get(parent_user_id=request.user.id)
    except:
        return redirect('/jobs')

    application = Application.objects.all()\
                .filter(job = Job.objects.get(pk = job_id))\
                .filter(user = individual)
    if application:
        application.delete()
    
    # Autofill form based on user info
    autofill = {"country":"Country"}
    if request.user.first_name or request.user.last_name:
        autofill["name"] = f"{request.user.first_name} {request.user.last_name}"
    if individual and individual.address:
        autofill["street_name"] = individual.address

    job = Job.objects.get(pk=job_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit = False)
            application.job = job
            application.user = individual
            application.save()
            return redirect('/jobs/%d/applications/%d/experiences'%(job.id,application.id))

    else:
        form = ApplicationForm(initial=autofill)

    content = {
        'form':form,
        'job':job
    }

    return render(request, 'applications/apply.html', content)

@login_required
def experience(request, job_id, application_id):
    experience_form_set = formset_factory(ExperienceForm, extra = 3)
    post_data = request.POST.copy()
    post_data['form-TOTAL_FORMS'] = 3
    post_data['form-INITIAL_FORMS'] = 3
    post_data['form-MAX_NUM_FORMS'] = 3

    content = {
        "forms":experience_form_set(post_data or None),
        "action":"experiences"
    }
    if request.method != "POST":
        return render(request, 'applications/experiences.html', content)
    
    application = Application.objects.get(pk=application_id)
    for form in content["forms"].forms:
        if form.is_valid():
            experience = form.save(commit = False)
            experience.application = application
            experience.save()

    return redirect("/jobs/%d/applications/%d/references"%(job_id, application_id))
            
@login_required
def reference(request,job_id, application_id):
    reference_form_set = formset_factory(ReferencesForm, extra = 3)
    post_data = request.POST.copy()
    post_data['form-TOTAL_FORMS'] = 3
    post_data['form-INITIAL_FORMS'] = 3
    post_data['form-MAX_NUM_FORMS'] = 3

    content = {
        "forms":reference_form_set(post_data or None),
        "action":"references"
    }
    if request.method != "POST":
        return render(request, 'applications/references.html', content)

    application = Application.objects.get(pk=application_id)
    for form in content["forms"]:
        if form.is_valid():
            reference = form.save(commit = False)
            reference.application = application
            reference.save()
    return redirect('/profiles/applications/%d'%(application_id))

def filter_jobs(request):
    jobs = Job.objects.all()
    if not request.GET:
        return jobs

    type_selection = request.GET.getlist("job_type")
    if len(type_selection) > 0:
        jobs = jobs.filter(job_type__in=type_selection)

    if request.GET['title']:
        jobs = jobs.filter(title__icontains=request.GET['title'])

    if request.GET['company']:
        jobs = jobs.filter(company=request.GET['company'])

    if request.GET['category']:
        jobs = jobs.filter(category=request.GET['category'])

    if request.GET['order_by']:
        order = ORDERS[int(request.GET['order_by'])][1]
        if not order:
            return jobs

        jobs = jobs.order_by(order)

    return jobs

