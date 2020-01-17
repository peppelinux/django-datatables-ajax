from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class Ticket(models.Model):
    """
    Simple ticket model
    """
    code = models.CharField(max_length=255, unique=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    edited = models.DateField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   null=True)
    priority = models.IntegerField(default=0)

    def get_priority_verbose(self):
        """
        Pure example method
        """
        if self.priority == 1:
            return "High"
        return "Normal"

    class Meta:
        ordering = ["priority",
                    "-created",
                    "code"]
        verbose_name = _("Ticket")
        verbose_name_plural = _("Ticket")
