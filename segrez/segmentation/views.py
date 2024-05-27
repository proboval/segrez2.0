from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from users.models import *
from django.contrib import messages
import io
import zipfile
from PIL import Image, ImageDraw
import os


def index(request):
    tags = Tags.objects.all()
    return render(request, 'segmentation/index.html', {'tags': tags, 'title': 'Список тегов'})


@csrf_exempt
def project_show(request):
    try:
        first_name = request.user.first_name
        projects = request.user.projects.all()
        user_type = 'Эксперт'
    except AttributeError:
        user_type = 'Компания'
        company = request.user
        projects = Project.objects.filter(company=company)

    context = {'user': request.user, 'projects': projects, 'user_type': user_type}

    return render(request, 'segmentation/projects.html', context=context)


def test(request):
    projectId = request.GET.get('projectId')
    print(projectId)
    if projectId:
        project = Project.objects.get(pk=projectId)
        _tags = project.tags.all()
        _images = project.images.all()
        polygons = []
        colorPol = []
        for i in range(len(_images)):
            polygons.append([])
            colorPol.append([])

        i = 0
        for image in _images:
            print(image)
            for rect in Rect.objects.all().filter(inImage=image):
                print(rect)
                tempArr = []
                colorPol[i].append(rect.tag.Name)
                for p in rect.points.all():
                    tempArr.append([p.x, p.y])
                polygons[i].append(tempArr)
            i += 1

        _images = list(_images.values())
        context = {'tags': _tags, 'images': _images, 'title': 'Test Draw', 'rectForImage': polygons,
                   'colorPolArr': colorPol, 'projectId': projectId}
        return render(request, 'segmentation/testDraw.html', context=context)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


def renderDraw(request, data):
    return render(request, 'segmentation/testDraw.html', context=data)


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
        projectId = data.get('projectId')

        project = Project.objects.get(pk=projectId)

        idTag = Tags.objects.get(Name=tag, project=project)
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
            print(image.pk)
            print(Rect.objects.filter(inImage=image, idInImage=numPolygon))
            rect = Rect.objects.filter(inImage=image, idInImage=numPolygon).delete()

            Rect.objects.filter(inImage=image, idInImage__gt=numPolygon).update(idInImage=models.F('idInImage') - 1)

        return JsonResponse({'message': 'Данные успешно удалены'})
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'})


@csrf_exempt
def delete_tag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        idTag = data.get('tagId')

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
    experts = request.user.experts.all()
    print(experts)
    return render(request, 'segmentation/upload.html', {'experts': experts, 'change': False})


@csrf_exempt
def upload_project(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        name_project = request.POST.get('nameProject')
        projectExperts = request.POST.get('projectExperts')
        projectExperts = list(projectExperts.split(','))

        tags = request.POST.get('tags')
        tags = json.loads(tags)

        newProject = Project(Name=name_project, company=request.user)
        newProject.save()

        for expertPk in projectExperts:
            expert = Expert.objects.get(pk=expertPk)
            expert.projects.add(newProject)
            expert.save()

        for image in images:
            newImage = segmentImage(Name=image.name, Image=image, project=newProject)
            newImage.save()

        for tag in tags:
            _color = color(tag['color'])
            newTag = Tags(Name=tag['name'], Red=_color.red, Green=_color.green, Blue=_color.blue, project=newProject)
            newTag.save()

        messages.success(request, f'Проект {newProject.Name} успешно добавлен!')

    print(reverse('segmentation:project_show'))
    return redirect(reverse('segmentation:project_show'))


@csrf_exempt
def changeProject(request):
    projectIdGET = request.GET.get('projectId')
    project = Project.objects.get(pk=projectIdGET)
    companyExp = request.user.experts
    experts = []
    for expert in companyExp.all():
        if not (project.expert_set.filter(pk=expert.pk).exists()):
            experts.append(expert)

    context = {'project': project, 'experts': experts}
    return render(request, 'segmentation/changeProject.html', context=context)


@csrf_exempt
def deleteImage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        imagePk = data.get('imagePk')
        image = segmentImage.objects.get(pk=imagePk)
        image.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def deleteProject(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        projectPk = data.get('projectPk')
        project = Project.objects.get(pk=projectPk)
        project.delete()
        print(projectPk)

    return redirect(reverse('segmentation:project_show'))


@csrf_exempt
def changeProjectData(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        name_project = request.POST.get('nameProject')
        projectExperts = request.POST.get('projectExperts')
        projectPk = request.POST.get('projectPk')
        projectExperts = list(projectExperts.split(','))

        tags = request.POST.get('tags')
        tags = json.loads(tags)

        project = Project.objects.get(pk=projectPk)

        project.Name = name_project
        project.save_base()

        projectTags = project.tags.all()

        for tag in projectTags:
            tag.delete()

        for tag in tags:
            _color = color(tag['color'])
            newTag = Tags(Name=tag['name'], Red=_color.red, Green=_color.green, Blue=_color.blue, project=project)
            newTag.save()

        for image in images:
            newImage = segmentImage(Name=image.name, Image=image, project=project)
            newImage.save()

        for expert in project.expert_set.all():
            if expert.pk not in projectExperts:
                expert.projects.remove(project)
            else:
                projectExperts.remove(expert.pk)

        for expertPk in projectExperts:
            expert = Expert.objects.get(pk=expertPk)
            expert.projects.add(project)

        return redirect(reverse('segmentation:project_show'))


# добавить масшт и фикс размер
# добавить сохранение тегов в json
@csrf_exempt
def downloadData(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            projectPk = data.get('projectPk')
            project = Project.objects.get(pk=projectPk)

            images = project.images.all()
            rects = []
            points = []
            for image in images:
                rects.append(list(image.rects.all()))

                tempPoints = []
                for rect in rects[-1]:
                    tempPoints.append(list(rect.points.all()))
                points.append(tempPoints)

            data = {}

            i = 0
            for image in images:
                data[image.Name] = {}
                for j in range(len(rects[i])):
                    rect_key = f'{rects[i][j].idInImage}'
                    data[image.Name][rect_key] = {}
                    data[image.Name][rect_key][rects[i][j].tag.Name] = {'Red': rects[i][j].tag.Red,
                                                                        'Green': rects[i][j].tag.Green,
                                                                        'Blue': rects[i][j].tag.Blue}
                    for k in range(len(points[i][j])):
                        point = points[i][j][k]
                        data[image.Name][rect_key][k + 1] = {'x': point.x, 'y': point.y}
                i += 1

            json_data = json.dumps(data, indent=4, ensure_ascii=False).encode('utf8')

            buffer = io.BytesIO()

            print(rects)

            for i in range(len(rects)):
                rects[i].sort(key=lambda rect: sqGause(rect) * (-1))

            print(rects)
            for i in range(len(rects)):
                for j in range(len(rects[i])):
                    print(f'{rects[i][j]}, {sqGause(rects[i][j])}', end='; ')
                print()

            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(f'{project}.json', json_data)

                i = 0
                for image in images:
                    img = Image.new("RGB", (image.Image.width, image.Image.height), color=(0, 0, 0))
                    draw = ImageDraw.Draw(img)
                    for j in range(len(rects[i])):
                        xy = list()
                        for point in rects[i][j].points.all():
                            xy.append((point.x, point.y))
                        draw.polygon(xy, fill=(rects[i][j].tag.Red, rects[i][j].tag.Green, rects[i][j].tag.Blue),
                                     outline=(rects[i][j].tag.Red, rects[i][j].tag.Green, rects[i][j].tag.Blue))

                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    zip_file.writestr(f'masks/{image.Name}.png', img_buffer.read())
                    i += 1

            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=data.zip'

            messages.success(request, 'Маски успешно сгенерированы, ожидайте загрузку')

            return response
        except Exception as e:
            print(str(e))
            return HttpResponse(f"Ошибка: {str(e)}", status=500)

    return HttpResponse("Метод не поддерживается", status=405)


def sqGause(rect: Rect):
    points = []
    for point in rect.points.all():
        points.append(point)

    sq = 0
    for i in range(1, len(points) - 1):
        sq += points[i].x * points[i + 1].y
        sq -= points[i + 1].x * points[i].y

    sq += points[0].x * points[1].y + points[-1].x * points[0].y
    sq -= points[1].x * points[0].y + points[0].x * points[-1].y

    return abs(sq / 2)

