from rest_framework.decorators import api_view
from .models import Room
from .serializers import RoomSerializer

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsOwner

# @api_view(["GET", "POST"])
# def rooms_view(request):
#     if request.method == "GET":
#         rooms = Room.objects.all()[:5]
#         serializer = ReadRoomSerializer(rooms, many=True).data
#         return Response(serializer)
#     elif request.method == "POST":
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = WriteRoomSerializer(data=request.data)
#         if serializer.is_valid():
#             room = serializer.save(user=request.user)
#             room_serializer = ReadRoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)




class RoomViewSet(ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]



    @action(detail=False)
    def room_search(self, request):
        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("beds", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        filter_kwargs = {}
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms
        paginator = self.paginator
        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()    
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)



# class OwnPagination(PageNumberPagination):
#     page_size = 20

# class RoomsView(APIView):

#     def get(self, request):
#         paginator = OwnPagination()
#         rooms = Room.objects.all()
#         results = paginator.paginate_queryset(rooms, request)
#         serializer = RoomSerializer(results, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = RoomSerializer(data=request.data)
#         if serializer.is_valid():
#             room = serializer.save(user=request.user)
#             room_serializer = RoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)




# class RoomView(APIView):

#     def get_room(self, pk):
#         try:
#             room = Room.objects.get(pk=pk)
#             return room
#         except Room.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             serializer = RoomSerializer(room).data
#             return Response(serializer)

#     def put(self, request, pk):

#         print("put")
#         room = self.get_room(pk)
#         if room.user != request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         if room is not None:
#             serializer = RoomSerializer(room, data=request.data, partial=True)
#             if serializer.is_valid():
#                 room = serializer.save()
#                 return Response(RoomSerializer(room).data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)


#     def delete(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             if room.user != request.user:
#                 return Response(status=status.HTTP_403_FORBIDDEN)
#             room.delete()
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)





# class SeeRoomView(RetrieveAPIView):
#     queryset = Room.objects.all()
#     serializer_class = ReadRoomSerializer

# @api_view(["GET","DELETE"])
# def list_rooms(request):
#     rooms = Room.objects.all()
#     serialized_rooms = RoomSerializer(rooms, many=True)
#     return Response(data=serialized_rooms.data)

