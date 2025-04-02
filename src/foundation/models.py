from django.db import models
from django.contrib.auth.models import User

class Audit(models.Model):
    deleted = models.BooleanField(default=False, db_index=True)
    createdAt = models.DateTimeField(auto_now_add=True, db_column="created_at")
    createdBy = models.ForeignKey(User, null=True, db_column="created_by", on_delete=models.SET_NULL) 

    class Meta:
        abstract = True
        ordering = ['-createdAt']

class StateAudit(Audit):
    active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
        indexes = [ models.Index(fields=["active"]) ]

class Client(StateAudit):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "client"
        
class Project(StateAudit):
    name = models.CharField(max_length=100, unique=True)
    amount = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "project"

class PayDay(models.Model):
    day = models.SmallIntegerField()
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='pay_days')
    active = models.BooleanField(default=True, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        db_table = "pay_day"
        
class Payment(models.Model):
    amount = models.FloatField()
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, related_name='payments')
    payed = models.BooleanField(default=False, db_index=True)
    payed_at = models.DateTimeField(null=True)
    active = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        db_table = "payment"
