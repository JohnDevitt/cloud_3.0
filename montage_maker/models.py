from django.db import models
from django.utils.translation import ugettext_lazy as _

class MontageElementContainer(models.Model):
	auto_increment_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=3000)

class MontageElement(models.Model):
	video_file = models.FileField(_('Attachment'), upload_to='montage_elements/%Y/%m/%d')
	container = models.ForeignKey(MontageElementContainer)

class Montage(models.Model):
	video_file = models.FileField(upload_to='montages/%Y/%m/%d')