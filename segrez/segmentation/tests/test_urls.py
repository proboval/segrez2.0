# segmentation/tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from segmentation.views import *

class SegmentationURLTests(SimpleTestCase):

    def test_segmentation_index_url(self):
        url = reverse('segmentation:segmentation.index')
        self.assertEqual(resolve(url).func, index)

    def test_testDraw_url(self):
        url = reverse('segmentation:testDraw')
        self.assertEqual(resolve(url).func, test)

    def test_upload_project_url(self):
        url = reverse('segmentation:upload_project')
        self.assertEqual(resolve(url).func, upload_project)

    def test_upload_url(self):
        url = reverse('segmentation:upload')
        self.assertEqual(resolve(url).func, upload_show)

    def test_change_tag_url(self):
        url = reverse('segmentation:change_tag')
        self.assertEqual(resolve(url).func, change_tag)

    def test_delete_tag_url(self):
        url = reverse('segmentation:delete_tag')
        self.assertEqual(resolve(url).func, delete_tag)

    def test_get_tag_url(self):
        url = reverse('segmentation:get_tag')
        self.assertEqual(resolve(url).func, get_tag)

    def test_save_new_tag_url(self):
        url = reverse('segmentation:save_new_tag')
        self.assertEqual(resolve(url).func, save_new_tag)

    def test_save_polygon_url(self):
        url = reverse('segmentation:save_polygon')
        self.assertEqual(resolve(url).func, save_polygon)

    def test_del_polygon_url(self):
        url = reverse('segmentation:del_polygon')
        self.assertEqual(resolve(url).func, del_polygon)

    def test_project_show_url(self):
        url = reverse('segmentation:project_show')
        self.assertEqual(resolve(url).func, project_show)

    def test_changeProject_url(self):
        url = reverse('segmentation:changeProject')
        self.assertEqual(resolve(url).func, changeProject)

    def test_deleteImage_url(self):
        url = reverse('segmentation:deleteImage')
        self.assertEqual(resolve(url).func, deleteImage)

    def test_deleteProject_url(self):
        url = reverse('segmentation:deleteProject')
        self.assertEqual(resolve(url).func, deleteProject)

    def test_changeProjectData_url(self):
        url = reverse('segmentation:changeProjectData')
        self.assertEqual(resolve(url).func, changeProjectData)

    def test_downloadData_url(self):
        url = reverse('segmentation:downloadData')
        self.assertEqual(resolve(url).func, downloadData)
