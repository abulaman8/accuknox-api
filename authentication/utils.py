import re
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt import authentication
from functools import wraps


def authed():
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            jwt_auth = authentication.JWTAuthentication()
            auth_tuple = jwt_auth.authenticate(request)

            if not auth_tuple:
                return Response(
                    {'message': 'User is not authenticated'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            user = auth_tuple[0]
            print(f"user: {user}")
            if not user.is_authenticated:
                return Response(
                    {'message': 'User is not authenticated'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            request.user = user
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def is_valid_email(email):
    # Define a regular expression for validating an email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Use the re.match() method to check if the email matches the regex
    if re.match(email_regex, email):
        return True
    else:
        return False
