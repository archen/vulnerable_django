import datetime

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', editable=False)
    decoration = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.date.today()
        super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('polls:detail', args=[str(self.id)])


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text