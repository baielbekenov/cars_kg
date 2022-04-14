from rest_framework import generics, response
from rest_framework.viewsets import ModelViewSet
from .permissions import IsAuthorOrReadOnly
from .serializers import CarSerializer
from rest_framework.decorators import action
from .models import Car

#
# class CreateCarAPIView(generics.CreateAPIView):
#     serializer_class = CarSerializer
#     queryset = Car.objects.all()
#
#
#     def perform_create(self, serializer):
#         return serializer.save(author=self.request.user)
#
#
# class UpdateCarAPIView(generics.UpdateAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#     permission_classes = [IsAuthorOrReadOnly, ]
#
#
# class DeleteDetailCarAPIView(generics.RetrieveDestroyAPIView):
#     queryset = Car.objects.all()
#     serializer_class = CarSerializer
#     permission_classes = [IsAuthorOrReadOnly, ]


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        queryset = self.queryset
        name = request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        serializer = self.serializer_class(queryset, many=True)
        return response.Response(serializer.data)

