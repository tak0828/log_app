from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """カスタムユーザーモデル"""
    email = models.EmailField('メールアドレス', unique=True, blank=False, null=False)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    is_active = models.BooleanField('有効', default=True)
    
    class Meta:
        db_table = 'custom_user'
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'
    
    def __str__(self):
        return self.username


class Log(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='logs',
        null=True,
        blank=True,
    )
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"{self.date}: {self.text[:20]}"
