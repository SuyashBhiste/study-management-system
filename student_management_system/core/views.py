from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponse
from django.db import IntegrityError
from .models import Study
from .forms import StudyForm
import logging

logger = logging.getLogger('django')

def study_list(request):
    studies = Study.objects.all()
    return render(request, 'study_list.html', { 'studies': studies }, status=200)

def add_study(request):
    if request.method == "GET":
        return render(request, 'add_study.html', { 'form': StudyForm() }, status=201)

    if request.method == 'POST':
        form = StudyForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid input. Please correct the form fields.")

        try:
            if Study.objects.filter(study_name=form.cleaned_data['study_name']).exists():
                logger.info("Duplicate name detected")
                return HttpResponse("Study with this name already exists.", status=409)
            
            form.save()
            return redirect('study_list')
        except IntegrityError as e:
            logger.info("Database connection issue")
            return HttpResponse("Error: Could not save the study. Please try again.")

def edit_study(request, id):
    study = get_object_or_404(Study, pk=id)

    if request.method == "GET":
        return render(request, 'edit_study.html', { 'form': StudyForm(instance=study) }, status=200)

    if request.method == 'POST':
        form = StudyForm(request.POST, instance=study)
        if not form.is_valid():
            return HttpResponseBadRequest("Invalid input. Please correct the form fields.")
        try:
            if Study.objects.filter(study_name=form.cleaned_data['study_name']).exclude(pk=id).exists():
                logger.info("Duplicate name detected")
                return HttpResponse("Study with this name already exists.", status=409)
            
            form.save()
            return redirect('study_list')
        except IntegrityError:
            logger.info("Database connection issue")
            return HttpResponse("Error: Could not update the study. Please try again.")

def view_study(request, id):
    study = get_object_or_404(Study, pk=id)
    return render(request, 'view_study.html', { 'study': study }, status=200)

def delete_study(request, id):
    study = get_object_or_404(Study, pk=id)
    study.delete()
    return redirect('study_list')
