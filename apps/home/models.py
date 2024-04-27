from django.db import models


# Create your models here.
class Hebdo(models.Model):
    department = models.CharField(max_length=150)
    family = models.CharField(max_length=150)
    article = models.CharField(max_length=150)
    designation = models.TextField()
    type = models.CharField(max_length=50, choices=(
        ('Import', 'Import'),
        ('Local', 'Local'),
    ))
    qte_pta = models.DecimalField(max_digits=20, decimal_places=2)
    pmp_pta = models.DecimalField(max_digits=20, decimal_places=2)
    pdv_pta = models.DecimalField(max_digits=20, decimal_places=2)
    qte_realisation = models.DecimalField(max_digits=20, decimal_places=2)
    pmp_realisation = models.DecimalField(max_digits=20, decimal_places=2)
    pdv_realisation = models.DecimalField(max_digits=20, decimal_places=2)
    ecart_qte = models.DecimalField(max_digits=20, decimal_places=2)
    ecart_ca_ht = models.DecimalField(max_digits=20, decimal_places=2)
    stock_prevision = models.DecimalField(max_digits=20, decimal_places=2)

