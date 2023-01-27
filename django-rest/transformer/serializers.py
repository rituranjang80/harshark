from rest_framework import serializers
from .models import Transformer

class TransformerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transformer
		fields = "__all__"
