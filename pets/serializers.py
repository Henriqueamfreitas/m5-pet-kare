from rest_framework import serializers
from pets.models import SexPet
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer

class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexPet.choices,
        default=SexPet.NOT_INFORMED
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)  

