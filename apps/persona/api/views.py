from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from rest_framework.response import Response
from django.http import Http404

from .serializers import PersonaSerializer
from ..models import Persona
from rest_framework import filters


class PersonaModelViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaApiView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):        
		elements = Persona.objects.all()
		serializer = PersonaSerializer(elements, many=True)
		response_dict = {
            'code': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Success'
        }
		return JsonResponse(response_dict)



class PersonaViewSet(viewsets.ViewSet):
	# permission_classes = (AllowAny,)

	def get_object(self, pk):
		try:
			return Persona.objects.get(pk=pk)
		except Persona.DoesNotExist:
			raise Http404

	def list(self, request):
		queryset = Persona.objects.all()
		serializer = PersonaSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		instance = self.get_object(pk)
		serializer = PersonaSerializer(instance)
		return Response(serializer.data)


class PersonaViewSetReadOnly(viewsets.ReadOnlyModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('apellido', 'nombre', 'legajo')