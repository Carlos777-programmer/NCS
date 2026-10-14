from rest_framework import serializers
from .models import ProdutoLoja

class ProdutoLojaSerializer(serializers.ModelSerializer):
    specs = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProdutoLoja
        fields = [
            'id', 'name', 'ritual', 'icon', 'tag', 'rank', 
            'description', 'price', 'specs', 'affiliate_url', 'verified_partner', 'image'
        ]

    def get_specs(self, obj):
        return {
            'volume': obj.volume,
            'rendimento': obj.rendimento,
            'ph': obj.ph,
            'durabilidade': obj.durabilidade
        }

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None