from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from account.renderers import UserRenderer
from .models import MyUser
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer


# function to create Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'message': "Login Sucessfull", 
                                 "token": token}, status=status.HTTP_200_OK)
                    
            else:
                return Response(
                    {"message": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
        except ValidationError as ve:
            return Response(
                {"message": "Validation failed", "errors": ve.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {"message": f"Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [UserRenderer]

    # Method to Create a User
    @csrf_exempt
    def post(self, request):
        try:
            serializer = UserSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'message': "Created Sucessfully", 'Token': token}, 
                            status=status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({'message': "Validation Error", 'errors': e.detail}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': f"Internal server error"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    
    # def get(self, request, pk=None, format=None):
    #     try:
    #         if pk:
    #             userData = MyUser.objects.get(id=pk)
    #             serializer = UserSerializer(userData)
    #         else:
    #             userData = MyUser.objects.all()
    #             serializer = UserSerializer(userData, many=True)
        
    #         return Response({'message': "User Fetched Sucessfully", 
    #                          'User Data': serializer.data}, status=status.HTTP_200_OK)
        
    #     except ObjectDoesNotExist:
    #         return Response(
    #             {'message': f"User with id {pk} not found"},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
        
    #     except Exception as e:
    #         return Response({'message': f"Internal server error"},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        try:
            if isinstance(request.user, AnonymousUser):
                return Response(
                    {"message": "Authentication credentials were not provided."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            serializer = UserProfileSerializer(request.user)
            
            return Response({'user data':serializer.data, 
                             'message': "User Data Fetched Sucessfully"}, status=status.HTTP_200_OK)
        
        except AttributeError as e:
            return Response(
                {"message": "User data is not in expected format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"message": f"Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):  
        try:
            refresh_token = request.data["refresh"]
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": "Logged out successfully."})
        
        except TokenError as e:
            return Response(
                {"error": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            return Response(
                {"message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
