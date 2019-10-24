from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse


class TimeStampedModel(models.Model):
    """ TimeStamped Model """
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    class Meta:
        abstract    = True




class Todo(TimeStampedModel):
    """ Todo Model """
    owner    = models.ForeignKey(to = get_user_model(),on_delete=models.CASCADE)
    name     = models.CharField(max_length=60)
    is_done  = models.BooleanField(default=False)


    class Meta:
        ordering            = ('-created',) 
        verbose_name        = 'Todo'
        verbose_name_plural = 'Todo\'s'

    def __str__(self):
        return self.name

    def get_api_url(self,request=None):
        return api_reverse('todo_api:todo-detail',kwargs={'pk':self.pk},request=request)

