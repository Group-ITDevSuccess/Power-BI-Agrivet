import uuid

from django.db import models


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Family(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Saison(BaseModel):
    number = models.IntegerField(auto_created=True)
    archived = models.BooleanField(default=False)
    qte_pta = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pmp_pta = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pdv_pta = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    qte_realisation = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pmp_realisation = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    pdv_realisation = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    stock_realisation = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    stock_prevision = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.number


class Hebdo(BaseModel):
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, blank=True)
    family = models.ForeignKey('Family', on_delete=models.CASCADE, null=True, blank=True)
    article = models.CharField(max_length=150)
    designation = models.TextField()
    type = models.CharField(max_length=50, choices=(
        (1, 'Import'),
        (2, 'Local'),
    ))
    category = models.CharField(max_length=50, choices=(
        ('2080', '2080'),
        ('8020', '8020'),
    ), null=True)
    saison = models.ManyToManyField('Saison', blank=True)

    def __str__(self):
        return self.article

    def has_active_saison(self):
        return self.saison.filter(archived=False).exists()
