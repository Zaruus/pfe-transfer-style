from django.db import models
import re

class ContentImagesModel(models.Model):
    img = models.ImageField(upload_to = "content-images/")

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.img}'

class OutputImagesModel(models.Model):
    img = models.ImageField(upload_to = "output-images/")

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.img}'

class StyleImagesModel(models.Model):
    name = models.CharField(max_length=50, default ="style_image")
    img = models.ImageField(upload_to = "style-images/")

    def __str__(self):
        """String for representing the Model object."""
        str_to_return = re.search(r'(?<=/)(.*)(?=.jpg)', str(self.img)).group(0)
        return str_to_return