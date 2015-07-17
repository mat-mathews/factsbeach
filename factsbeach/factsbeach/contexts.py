from pyramid.security import (
    Everyone,
    Authenticated,
    Allow,
)

from pyaella.server.api import WebRoot

__all__ = [
    'AppRoot',
    'Admin',
    'Unsafe',
    'Users'
]

class AppRoot(WebRoot):
    __name__ = None
    __parent__ = None
    __acl__ =         [   
            (Allow, Authenticated, 'view'),

            (Allow, 'group:su', 'su'),
            (Allow, 'group:su', 'add'),
            (Allow, 'group:su', 'edit'),
            (Allow, 'group:su', 'delete'),
            (Allow, 'group:su', 'view'),

            (Allow, 'group:admin', 'add'),
            (Allow, 'group:admin', 'edit'),
            (Allow, 'group:admin', 'delete'),
            (Allow, 'group:admin', 'view'),

            (Allow, 'group:editor', 'add'),
            (Allow, 'group:editor', 'edit'),
            (Allow, 'group:editor', 'view')
        ]

    def __init__(self, request):
        WebRoot.__init__(self, request)
        WebRoot.__parent__ = self
        self.__setitem__('a', Admin(request))
        self.__setitem__('u', Users(request))
        self.__setitem__('r', Reports(request))


class Admin(dict):
    __name__ = 'Admin'
    __parent__ = AppRoot
    def __init__(self, request):
        self.request = request
        self.__setitem__('unsafe', Unsafe(request))


class Unsafe(dict):
    __name__ = 'Unsafe'
    __parent__ = Admin
    def __init__(self, request):
        self.request = request


class Users(dict):
    __name__ = 'Users'
    __parent__ = AppRoot
    def __init__(self, request):
        self.request = request


class Reports(dict):
    __name__ = 'Reports'
    __parent__ = AppRoot
    def __init__(self, request):
        self.request = request


