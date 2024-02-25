from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import *
from django.http import JsonResponse


def index(request):
    tags = Tags.objects.all()
    return render(request, 'segmentation/index.html', {'tags': tags, 'title': 'Список тегов'})


def test(request):
    tags = Tags.objects.all()
    images = segmentImage.objects.all()

    return render(request,
                  'segmentation/testDraw.html',
                  {'tags': tags, 'images': images, 'title': 'Test Draw'})


def get_image_name(request):
    num_img = request.GET.get('numImg')  # Получаем значение numImg из GET-параметров
    image = segmentImage.objects.get(pk=num_img)

    if image:
        return JsonResponse({'image_name': image.Name, 'image_url': image.Image.url})
    else:
        return JsonResponse({'error': 'Image not found'})


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "segmentation/upload.html"  # Replace with your template.
    success_url = "segmentation/testDraw.html"  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]

        for uploaded_file in files:
            segment_image = segmentImage(Image=uploaded_file, Name=uploaded_file.name)
            segment_image.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('test')
