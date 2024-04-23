from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from users.models import *


def index(request):
    tags = Tags.objects.all()
    return render(request, 'segmentation/index.html', {'tags': tags, 'title': 'Список тегов'})

@csrf_exempt
def project_show(request):
    try:
        company = request.user.company
        user_type = 'Эксперт'
    except AttributeError:
        user_type = 'Компания'
        company = request.user

    projects = Project.objects.filter(company=company)
    context = {'user': request.user, 'projects': projects, 'user_type': user_type}

    return render(request, 'segmentation/projects.html', context=context)


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
    name = request.GET.get('name')

    tag = Tags.objects.get(Name=name)

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


@csrf_exempt
def save_polygon(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        polygon = data.get('polygon')
        numPolygon = data.get('numPolygon')
        numImg = data.get('numImg')
        tag = data.get('tag')

        idTag = Tags.objects.get(Name=tag)
        image = segmentImage.objects.get(pk=numImg)

        newPol = Rect(tag=idTag, inImage=image, idInImage=numPolygon)
        newPol.save()

        for i in range(len(polygon)):
            newPoint = Point(x=polygon[i][0], y=polygon[i][1], inRect=newPol)
            newPoint.save()

        return JsonResponse({'message': 'Данные успешно сохранены'})
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


@csrf_exempt
def save_new_tag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        newName = data.get('name')
        newColor = data.get('color')

        c = color(newColor)

        with transaction.atomic():
            tag = Tags(Name=newName, Red=c.red, Green=c.green, Blue=c.blue)
            tag.save()

        pk_tag = tag.pk

        return JsonResponse({'message': 'Данные успешно сохранены', 'id': pk_tag,
                             'name': newName, 'color': newColor})
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


@csrf_exempt
def del_polygon(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        numPolygon = data.get('numPolygon')
        numImg = data.get('numImg')

        with transaction.atomic():
            image = segmentImage.objects.get(pk=numImg)
            rect = Rect.objects.filter(inImage=image, idInImage=numPolygon).delete()

            Rect.objects.filter(inImage=image, idInImage__gt=numPolygon).update(idInImage=models.F('idInImage') - 1)

        return JsonResponse({'message': 'Данные успешно сохранены'})
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


@csrf_exempt
def delete_tag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        idTag = data.get('id')

        with transaction.atomic():
            tag = Tags.objects.get(pk=idTag).delete()

        return JsonResponse({'message': 'Данные успешно сохранены'})
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


@csrf_exempt
def change_tag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        idTag = data.get('id')
        newName = data.get('newName')
        newColor = data.get('newColor')
        newColor = newColor.replace('#', '')

        c = color(newColor)

        with transaction.atomic():
            tag = Tags.objects.get(pk=idTag)
            tag.Name = newName
            tag.Red = c.red
            tag.Green = c.green
            tag.Blue = c.blue

            tag.save()

        return JsonResponse({'message': 'Данные успешно сохранены'})
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


class color:
    red = int()
    green = int()
    blue = int()

    def __init__(self, hexColor):
        hexColor = hexColor.replace('#', '')
        self.red = int(hexColor[:2], 16)
        self.green = int(hexColor[2:4], 16)
        self.blue = int(hexColor[4:], 16)


def upload_show(request):
    return render(request, 'segmentation/upload.html')

@csrf_exempt
def upload_project(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        name_project = request.POST.get('nameProject')

        tags = request.POST.get('tags')
        tags = json.loads(tags)

        newProject = Project(Name=name_project, company=request.user)
        newProject.save()

        for image in images:
            newImage = segmentImage(Name=image.name, Image=image, project=newProject)
            newImage.save()

        for tag in tags:
            _color = color(tag['color'])
            newTag = Tags(Name=tag['name'], Red=_color.red, Green=_color.green, Blue=_color.blue, project=newProject)
            newTag.save()

    print(reverse('segmentation:project_show'))
    return redirect(reverse('segmentation:project_show'))

