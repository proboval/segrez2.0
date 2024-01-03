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


# class Data(models.Model):
#     """
#     Class for storage images
#
#     """
