from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    tags = Tags.objects.all()
    return render(request, 'segmentation/index.html', {'tags': tags, 'title': 'Список тегов'})


def test(request):
    tags = Tags.objects.all()
    images = segmentImage.objects.all()
    rects = Rect.objects.all()
    polygons = []
    colorPol = []
    for i in range(len(images)):
        polygons.append([])
        colorPol.append([])

    for i in range(len(images)):
        for rect in Rect.objects.all().filter(inImage=i+1):
            tempArr = []
            colorPol[i].append(rect.tag.Name)
            for p in rect.points.all():
                tempArr.append([p.x, p.y])
            polygons[i].append(tempArr)

    return render(request,
                  'segmentation/testDraw.html',
                  {'tags': tags, 'images': images, 'title': 'Test Draw', 'rectForImage': polygons,
                   'colorPolArr': colorPol})


def get_image_name(request):
    num_img = request.GET.get('numImg')  # Получаем значение numImg из GET-параметров
    image = segmentImage.objects.get(pk=num_img)

    if image:
        return JsonResponse({'image_name': image.Name, 'image_url': image.Image.url})
    else:
        return JsonResponse({'error': 'Image not found'})


def get_tag(request):
    optionName = request.GET.get('optionName')

    tag = Tags.objects.get(Name=optionName)

    if tag:
        return JsonResponse({'Name': tag.Name, 'Red': tag.Red, 'Green': tag.Green, 'Blue': tag.Blue, 'ID': tag.pk})
    else:
        return JsonResponse({'error': 'Image not found'})


@csrf_exempt
def save_data(request):
    Rect.objects.all().delete()
    Point.objects.all().delete()
    if request.method == 'POST':
        data = json.loads(request.body)
        polygons = data.get('polygons')
        colorPolygons = data.get('PolsColor')
        for i in range(len(polygons)):
            for j in range(len(polygons[i])):
                tag = Tags.objects.get(Name=colorPolygons[i][j])
                image = segmentImage.objects.get(pk=i+1)
                newPol = Rect(tag=tag, inImage=image)
                newPol.save()
                for k in range(len(polygons[i][j])):
                    newPoint = Point(x=polygons[i][j][k][0], y=polygons[i][j][k][1], inRect=newPol)
                    newPoint.save()

        return JsonResponse({'message': 'Данные успешно сохранены'})  # Возвращаем ответ клиенту
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "segmentation/upload.html"
    success_url = "segmentation/testDraw.html"

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
