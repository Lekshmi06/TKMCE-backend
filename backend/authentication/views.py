from django.shortcuts import render
from .serializers import LoginSerializer
from django.contrib.auth import authenticate


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class AdminLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                if not user.is_superuser:
                    return Response({'error': 'Access restricted to admin only'}, status=status.HTTP_403_FORBIDDEN)

                refresh = RefreshToken.for_user(user)
                refresh['is_superuser'] = user.is_superuser  

                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'is_superuser': user.is_superuser,
                    'message': 'Login successful'
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
