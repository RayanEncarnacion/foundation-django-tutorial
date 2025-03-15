from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Audit(models.Model):
    deleted = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, db_column="created_at")
    createdBy = models.ForeignKey(User, null=True, db_column="created_by", on_delete=models.SET_NULL) 

    class Meta:
        abstract = True

class StateAudit(Audit):
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Client(StateAudit):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = "client"