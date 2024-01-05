from django.db import models


class Tags(models.Model):
    """
    Class for changing selection color
    id - tag's id
    Name - tag's name
    Red - count red in RGB
    Green - count green in RGB
    Blue - count blue in RGB
    """
    Name = models.CharField(max_length=25)
    Red = models.IntegerField()
    Green = models.IntegerField()
    Blue = models.IntegerField()

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['Red', 'Green', 'Blue']

class segmentImage(models.Model):
    """
    Class for sigmentation images
    id - image's id
    Name - image's name
    Image - image
    """
    Name = models.CharField(max_length=25)
    Image = models.ImageField(upload_to='images/%data')
