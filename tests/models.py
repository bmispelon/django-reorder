from django.db import models


SIZES = [
    ('XXS', 'XX-Small'),
    ('XS', 'X-Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'X-Large'),
    ('XXL', 'XX-Large'),
]


class Tshirt(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=5, choices=SIZES)

    def __str__(self):
        return self.name
