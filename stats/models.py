from django.db import models


class HGUser(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        app_label = "stats"


class ChangeSet(models.Model):
    revision = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(HGUser)
    files = models.IntegerField()
    lines_added = models.IntegerField()
    lines_removed = models.IntegerField()
    description = models.TextField()

    class Meta:
        app_label = "stats"
        get_latest_by = 'timestamp'

