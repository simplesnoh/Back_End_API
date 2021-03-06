"""View module for handling requests about daddy_os"""

import json
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Daddy_O

class daddy_o_serializer(serializers.HyperlinkedModelSerializer):
    """ JSON Serializer for Daddy-Os(aka users)"""

    class Meta:
        model = Daddy_O
        url = serializers.HyperlinkedIdentityField(
            view_name='daddy_o',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user_id')
        depth = 2

class Daddy_Os(ViewSet):
    """Daddy-Os for the DadMoves app"""

    """Creating a Daddy-O is accomplished in register view"""

    def create(self, request):
        """Handles Post Operations"""

        new_daddy_o = Daddy_O()
        new_daddy_o.save()

        serializer = daddy_o_serializer(new_daddy_o, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handles the delete request request for the Daddy-os, effectively deleting their whole account"""
        try:
            daddy_o = Daddy_O.objects.get(pk)
            daddy_o.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Daddy_O.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """ Handles get request for a single Daddy-o for the profile page """

        daddy_os = Daddy_O.objects.all()

        serializer = daddy_o_serializer(
            daddy_os, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def currentUser(self, request):

        try:
            daddy_o = Daddy_O.objects.get(user=request.auth.user)
        except Daddy_O.DoesNotExist as ex:
            return Response({'message': ex.args[0]},status=status.HTTP_404_NOT_FOUND)

        serializer = daddy_o_serializer(
            daddy_o, context={'request': request})
        return Response(serializer.data)