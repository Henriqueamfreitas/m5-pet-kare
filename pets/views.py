from rest_framework.views import APIView, status, Request, Response
from pets.models import Pet
from django.forms import model_to_dict
from groups.models import Group
from traits.models import Trait
from pets.serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class PetView(APIView, PageNumberPagination):	
	def post(self, request: Request) -> Response:
		serializer = PetSerializer(data=request.data)
		if not serializer.is_valid():
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
		group_data = serializer.validated_data.pop('group')		
		trait_data = serializer.validated_data.pop('traits')
		
		try:
			group = Group.objects.get(scientific_name=group_data['scientific_name'])
		except Group.DoesNotExist:
			group = Group.objects.create(**group_data)
		
		pet = Pet.objects.create(**serializer.validated_data, group=group)
		for data in trait_data:
			data['name'] = data['name'].lower()
			try:
				trait = Trait.objects.get(name=data['name'])
			except Trait.DoesNotExist:
				trait = Trait.objects.create(**data)
				trait.pets.add(pet)		

		serializer = PetSerializer(pet)
		return Response(serializer.data, status.HTTP_201_CREATED)

	def get(self, request: Request) -> Response:
		by_trait = request.query_params.get('trait', None)
		if by_trait:
			pets = Pet.objects.filter(traits=by_trait)
		else:
			pets = Pet.objects.all()
		result = self.paginate_queryset(pets, request)
		serializer = PetSerializer(result, many=True)
		return self.get_paginated_response(serializer.data)


class PetDetailView(APIView):	
	def get(self, request: Request, pet_id: int) -> Response:
		try:
			found_pet = Pet.objects.get(pk=pet_id)
		except Pet.DoesNotExist:
			return Response({'detail': 'Not found.'}, status.HTTP_404_NOT_FOUND)
		
		serializer = PetSerializer(found_pet)

		return Response(serializer.data)
	
	def delete(self, request: Request, pet_id: int) -> Response:
		try:
			found_pet = Pet.objects.get(pk=pet_id)
		except Pet.DoesNotExist:
			return Response({'detail': 'Not found.'}, status.HTTP_404_NOT_FOUND)
		
		found_pet.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)
	
	def patch(self, request: Request, pet_id: int) -> Response:
		try:
			found_pet = Pet.objects.get(pk=pet_id)
		except Pet.DoesNotExist:
			return Response({'detail': 'Not found.'}, status.HTTP_404_NOT_FOUND)
		
		serializer = PetSerializer(data=request.data, partial=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

		for key, value in serializer.validated_data.items():
			if key == 'traits':
				found_pet.traits.clear()
				found_pet.traits.add(*value)  
			elif key == 'group':
				found_pet.group = value
			else:
				setattr(found_pet, key, value)
			
		found_pet.save()

		serializer = PetSerializer(found_pet)

		return Response(serializer.data)
