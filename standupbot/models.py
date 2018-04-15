import uuid

from django.db import models
from django.utils import timezone


class AbstractModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(null=True, default=timezone.now)
    updated_at = models.DateTimeField(null=True, default=timezone.now)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at'])
        ]


class Question(AbstractModel):
    text = models.TextField()
    order_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'questions'
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at'])
        ]


class User(AbstractModel):
    slack_id = models.TextField(unique=True)
    channel_id = models.TextField(unique=True, null=True, blank=True)
    is_active = models.BooleanField()
    name = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.slack_id

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['slack_id']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]


class Answer(AbstractModel):
    text = models.TextField()
    date = models.DateField()
    question = models.ForeignKey(to=Question, on_delete=models.PROTECT)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'answers'
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at'])
        ]
