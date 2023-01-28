from django.db import models

class Transformer(models.Model):
	name = models.CharField(max_length=150, unique=True)
	alternate_mode = models.CharField(
		max_length=250,
		blank=True,
		null=True)
	description = models.CharField(
		max_length=500,
		blank=True,
		null=True)
	alive = models.BooleanField(default=False)

	
	class Meta:
		ordering = ('name',)
	def to_representation(self, instance):
			data = super(Transformer, self).to_representation(instance)
			data.update("")
			return data


	def __str__(self):
		return self.name
