import base64
import binascii
from cmath import exp

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from jwt.exceptions import DecodeError
from jwt.exceptions import InvalidSignatureError


class VChainUser():
    def __init__(self, user_id, username, full_name, role, exp):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.role = role
        self.exp = exp    
        self.is_authenticated = True
    
    def to_dict(self):
        return {
            'username': self.username,
            # 'email': self.email,
            'full_name': self.full_name,
            # 'first_name': self.first_name,
            # 'last_name': self.last_name,
            # 'folder_id': self.folder_id,
            'role': self.role,
            # 'active': self.active,
            # 'balance': self.balance,
            # 'referral_code': self.referral_code,
            # 'plan': self.plan,
            # 'phone': self.phone,
            # 'birthday': self.birthday,
            'user_id': self.user_id,
            'exp': self.exp,
        }


class CustomAuthentication(BaseAuthentication):
    """
    Custom authentication class.
    It will authenticate any incoming request
    as the user given by the username in a
    custom request header.
    """

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """

        # Gets authorization from request header and query params
        # and checks different possibility of
        # invalid header.
        # ======================================

        auth = request.headers.get("AUTHORIZATION", "")

        if not auth:
            auth = 'Bearer ' + request.query_params.get('token', '')

        splitted_auth = auth.split(' ')

        if not auth or len(splitted_auth) != 2 or splitted_auth[0] not in ('Token', 'Bearer') or not splitted_auth[1]:
            raise AuthenticationFailed("Invalid authorization header. No credentials provided.")

        prefix, token = splitted_auth

        try:
            user_info = jwt.decode(token, settings.JWT_KEY, algorithms=['HS256'])
        except (InvalidSignatureError, DecodeError):
            raise AuthenticationFailed("Signature verification failed.")
        # print(user_info)
        user = VChainUser(user_info['user_id'], user_info['username'], user_info['full_name'], user_info['role'], user_info['exp'])

        return (user, None)
