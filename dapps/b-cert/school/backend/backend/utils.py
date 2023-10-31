'''
Utility functions
'''
from api.serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None):
    '''Return token with user data'''
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
