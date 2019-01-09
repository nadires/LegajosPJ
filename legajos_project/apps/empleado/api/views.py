from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from rest_framework.response import Response
from django.http import Http404

from .serializers import EmpleadoSerializer
from ..models import Empleado
from rest_framework import filters


class EmpleadoModelViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer


class EmpleadoApiView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request, format=None):        
		elements = Empleado.objects.all()
		serializer = EmpleadoSerializer(elements, many=True)
		response_dict = {
            'code': status.HTTP_200_OK,
            'data': serializer.data,
            'message': 'Success'
        }
		return JsonResponse(response_dict)



class EmpleadoViewSet(viewsets.ViewSet):
	# permission_classes = (AllowAny,)

	def get_object(self, pk):
		try:
			return Empleado.objects.get(pk=pk)
		except Empleado.DoesNotExist:
			raise Http404

	def list(self, request):
		queryset = Empleado.objects.all()
		serializer = EmpleadoSerializer(queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		instance = self.get_object(pk)
		serializer = EmpleadoSerializer(instance)
		return Response(serializer.data)


class EmpleadoViewSetReadOnly(viewsets.ReadOnlyModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('apellido', 'nombre', 'legajo')