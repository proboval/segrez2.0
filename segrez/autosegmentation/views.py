import json

import torch
from django.shortcuts import render, get_object_or_404
import cv2
import numpy as np
from segment_anything import SamPredictor, sam_model_registry
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from segmentation.models import segmentImage
import supervision as sv
import requests


@csrf_exempt
def autoSegmentation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        points = data.get('points')
        imagePk = data.get('imagePk')

        if 'image' not in request.session or request.session['image'] != imagePk:
            request.session['image'] = imagePk

            # Получаем URL изображения из модели
            image = get_object_or_404(segmentImage, pk=imagePk)
            image_url = request.build_absolute_uri(image.Image.url)

            # Загружаем изображение по URL
            response = requests.get(image_url)
            image_bytes = np.frombuffer(response.content, np.uint8)

            # Декодируем изображение
            imagecv = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(imagecv, cv2.COLOR_BGR2RGB)

            settings.MASK_PREDICTOR.set_image(image_rgb)
        if len(points) == 1:
            input_point = np.array([[points[0][0], points[0][0]]])
            input_label = np.array([1])

            masks, scores, logits = settings.MASK_PREDICTOR.predict(
                point_coords=input_point,
                point_labels=input_label,
                multimask_output=True,
            )
        else:
            box = np.array(points)
            input_label = np.array([1])
            masks, scores, logits = settings.MASK_PREDICTOR.predict(
                box=box,
                point_labels=input_label,
                multimask_output=True,
            )

        detections = sv.Detections(
            xyxy=sv.mask_to_xyxy(masks=masks),
            mask=masks
        )

        detections = detections[detections.area == np.max(detections.area)]
        bbox_coordinates = detections.xyxy[0]
        bbox_coordinates.tolist()

        bbox_coordinates = list(map(int, bbox_coordinates))

        mask = masks[0]
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Предполагаем, что интересует самый большой контур
        largest_contour = max(contours, key=cv2.contourArea)
        contour_coordinates = largest_contour.squeeze().tolist()
        print(contour_coordinates)

        return JsonResponse({'x_min': bbox_coordinates[0],
                             'y_min': bbox_coordinates[1],
                             'x_max': bbox_coordinates[2],
                             'y_max': bbox_coordinates[3],
                             'contour': contour_coordinates})

    return JsonResponse({'message': 'Данные успешно передались'})
