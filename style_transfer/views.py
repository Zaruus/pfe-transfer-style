import re
import subprocess
import sys

from django.shortcuts import render, redirect
from .forms import ContentImagesForm
from .models import ContentImagesModel, OutputImagesModel, StyleImagesModel
from fast_neural_style.neural_style import *

def index(request):
    """View function for home page of site."""
    StyleImages = StyleImagesModel.objects.all()

    if request.method == "POST":
        form = ContentImagesForm(request.POST, request.FILES)
        if form.is_valid():
            imgObj = form.save(commit=False)
            imgObj.save()
            name = re.search(r'(?<=/)(.*)(?=\.)', str(imgObj)).group(0)
            inputImgURL = "media/" + str(imgObj)
            modelURL = "fast_neural_style/saved_models/" + form.cleaned_data['style_image'] + ".pth"
            outputImgURL = "media/output-images/" + name + "-" + form.cleaned_data['style_image'] + ".jpg"
            subprocess.run(
                [sys.executable, "fast_neural_style/neural_style/neural_style.py", "eval", \
                    "--content-image", inputImgURL, \
                    "--model", modelURL, \
                    "--output-image", outputImgURL, \
                    "--cuda", "0"])
            outputImage = OutputImagesModel()
            outputImage.img = "output-images/" + name + "-" + form.cleaned_data['style_image'] + ".jpg"
            outputImage.save()
            return redirect('images')
    else:
        form = ContentImagesForm()

        context = {
        'form' : form,
        'style_images': StyleImages,
    }

    return render(request, 'index_style_transfer.html', context=context)

def display_images(request):

    if request.method == 'GET':

        # getting all the objects.
        ContentImages = ContentImagesModel.objects.all()
        OutputImages = OutputImagesModel.objects.all()

        context = {
            'content_images': ContentImages,
            'output_images': OutputImages,
        }
        
        return render(request, 'style_transfer/display_images.html', context=context)