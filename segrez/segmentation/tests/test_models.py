# segmentation/tests.py
from django.test import TestCase
from users.models import Company
from segmentation.models import Project, Tags, segmentImage, Rect, Point


class SegmentationModelsTest(TestCase):

    def setUp(self):
        # Создаем тестовую компанию
        self.company = Company.objects.create(name='Test Company', email='test@company.com', password='password123')

        # Создаем тестовый проект
        self.project = Project.objects.create(Name='Test Project', company=self.company)

        # Создаем тестовый тег
        self.tag = Tags.objects.create(Name='Test Tag', Red=255, Green=0, Blue=0, project=self.project)

        # Создаем тестовое изображение
        self.segment_image = segmentImage.objects.create(Name='Test Image', Image='test_image.jpg',
                                                         project=self.project)

        # Создаем тестовый прямоугольник
        self.rect = Rect.objects.create(tag=self.tag, inImage=self.segment_image, idInImage=1)

        # Создаем тестовые точки
        self.point1 = Point.objects.create(x=1.0, y=1.0, inRect=self.rect)
        self.point2 = Point.objects.create(x=2.0, y=2.0, inRect=self.rect)

    def test_project_creation(self):
        self.assertEqual(self.project.Name, 'Test Project')
        self.assertEqual(self.project.company, self.company)
        self.assertEqual(str(self.project), 'Test Project (Test Company)')

    def test_tag_creation(self):
        self.assertEqual(self.tag.Name, 'Test Tag')
        self.assertEqual(self.tag.Red, 255)
        self.assertEqual(self.tag.Green, 0)
        self.assertEqual(self.tag.Blue, 0)
        self.assertEqual(self.tag.project, self.project)
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_segment_image_creation(self):
        self.assertEqual(self.segment_image.Name, 'Test Image')
        self.assertEqual(self.segment_image.Image, 'test_image.jpg')
        self.assertEqual(self.segment_image.project, self.project)
        self.assertEqual(str(self.segment_image), 'Test Image')

    def test_rect_creation(self):
        self.assertEqual(self.rect.tag, self.tag)
        self.assertEqual(self.rect.inImage, self.segment_image)
        self.assertEqual(self.rect.idInImage, 1)
        self.assertEqual(str(self.rect), '1) Test Tag')

    def test_point_creation(self):
        self.assertEqual(self.point1.x, 1.0)
        self.assertEqual(self.point1.y, 1.0)
        self.assertEqual(self.point1.inRect, self.rect)
        self.assertEqual(str(self.point1), '(1.0, 1.0)')

        self.assertEqual(self.point2.x, 2.0)
        self.assertEqual(self.point2.y, 2.0)
        self.assertEqual(self.point2.inRect, self.rect)
        self.assertEqual(str(self.point2), '(2.0, 2.0)')
