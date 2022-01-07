from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Todo(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Название"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    important = models.BooleanField(default=False, verbose_name=_("Важно"))
    completed = models.BooleanField(default=False, verbose_name=_("Выполнено"))
    created_at = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
