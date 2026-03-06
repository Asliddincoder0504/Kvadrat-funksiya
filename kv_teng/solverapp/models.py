from django.db import models
from django.utils import timezone


class EquationSolution(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan vaqt")

    a = models.FloatField(verbose_name="a koeffitsienti")
    b = models.FloatField(verbose_name="b koeffitsienti")
    c = models.FloatField(verbose_name="c koeffitsienti")

    discriminant = models.FloatField(verbose_name="Diskriminant (D)")
    roots = models.TextField(verbose_name="Ildizlar", blank=True)
    steps = models.TextField(verbose_name="Bosqichlar")

    class Meta:
        verbose_name = "Yechim"
        verbose_name_plural = "Yechimlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.a}x² {self.b:+}x {self.c:+}   ({self.created_at.strftime('%Y-%m-%d %H:%M')})"