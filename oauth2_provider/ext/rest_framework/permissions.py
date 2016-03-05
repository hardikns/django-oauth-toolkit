import logging

from django.core.exceptions import ImproperlyConfigured

from rest_framework.permissions import BasePermission

from ...settings import oauth2_settings


log = logging.getLogger('oauth2_provider')

SAFE_HTTP_METHODS = ['GET', 'HEAD', 'OPTIONS']

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print ip
    return ip

def format_ip(value):
    try: 
        return '.'.join(map(lambda x: str(int(x)), value.split('.')))
    except:
        return '' 

class TokenHasScope(BasePermission):
    """
    The request is authenticated as a user and the token used has the right scope
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, 'scope'):  # OAuth 2
            required_scopes = self.get_scopes(request, view)
            log.debug("Required scopes to access resource: {0}".format(required_scopes))

            if not token.is_valid(required_scopes):
                return False

            if token.application.authorization_grant_type in ['password','client-credentials'] and \
               get_client_ip(request) not in map(format_ip, token.application.server_ips.split('\n')):
                print "missing not matched {0} - {1}".format(get_client_ip(request),token.application.server_ips)
                return False

            return True

        assert False, ('TokenHasScope requires either the'
                       '`oauth2_provider.rest_framework.OAuth2Authentication` authentication '
                       'class to be used.')

    def get_scopes(self, request, view):
        try:
            return getattr(view, 'required_scopes')
        except AttributeError:
            raise ImproperlyConfigured(
                'TokenHasScope requires the view to define the required_scopes attribute')


class TokenHasReadWriteScope(TokenHasScope):
    """
    The request is authenticated as a user and the token used has the right scope
    """

    def get_scopes(self, request, view):
        try:
            required_scopes = super(TokenHasReadWriteScope, self).get_scopes(request, view)
        except ImproperlyConfigured:
            required_scopes = []

        # TODO: code duplication!! see dispatch in ReadWriteScopedResourceMixin
        if request.method.upper() in SAFE_HTTP_METHODS:
            read_write_scope = oauth2_settings.READ_SCOPE
        else:
            read_write_scope = oauth2_settings.WRITE_SCOPE

        return required_scopes + [read_write_scope]


class TokenHasResourceScope(TokenHasScope):
    """
    The request is authenticated as a user and the token used has the right scope
    """

    def get_scopes(self, request, view):
        try:
            view_scopes = (
                super(TokenHasResourceScope, self).get_scopes(request, view)
            )
        except ImproperlyConfigured:
            view_scopes = []

        if request.method.upper() in SAFE_HTTP_METHODS:
            scope_type = oauth2_settings.READ_SCOPE
        else:
            scope_type = oauth2_settings.WRITE_SCOPE

        required_scopes = [
            '{0}:{1}'.format(scope, scope_type) for scope in view_scopes
        ]

        return required_scopes
