from django.db import models

class Fact(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    value = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Rule(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    conditions = models.ManyToManyField(Fact, related_name='rules_conditions')
    conclusion = models.ForeignKey(Fact, related_name='rules_conclusion', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
