from django.db import models
from users.models import Company


class Project(models.Model):
    """
    Class for save img for company
    id - project's id
    CompanyId - company's id
    Name - project's name
    """
    Name = models.CharField(
        max_length=25
    )
    company = models.ForeignKey(
        'users.Company',
        on_delete=models.CASCADE,
        related_name='projects'
    )

    def __str__(self):
        return f'{self.Name} ({self.company.companyName})'


class Tags(models.Model):
    """
    Class for changing selection color
    id - tag's id
    Name - tag's name
    Red - count red in RGB
    Green - count green in RGB
    Blue - count blue in RGB
    """
    Name = models.CharField(
        max_length=25
    )
    Red = models.IntegerField()
    Green = models.IntegerField()
    Blue = models.IntegerField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='tags'
    )

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
    ProjectId - project's id
    """
    Name = models.CharField(
        max_length=25
    )
    Image = models.ImageField(
        upload_to='images/'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return self.Name


class Rect(models.Model):
    tag = models.ForeignKey('Tags',
                            on_delete=models.CASCADE
                            )
    inImage = models.ForeignKey('segmentImage',
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='rects'
                                )
    idInImage = models.IntegerField()


class Point(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    inRect = models.ForeignKey(
        'Rect',
        on_delete=models.CASCADE,
        related_name='points'
    )

    def __str__(self):
        return f'({self.x}, {self.y})'