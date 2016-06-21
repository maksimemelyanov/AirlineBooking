from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import Authenticated
class HelloFactory(object):
    def __init__(self, request):
        self.__acl__ = [
            (Allow, Authenticated, 'view')
        ]

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('main', '/')
    config.add_route('login', '/signin')
    config.add_route('logged', '/login')
    config.add_route('logouted', '/logout')
    config.add_route('cab', '/cabinet', factory=HelloFactory)
    config.add_route('search', '/search', factory=HelloFactory)
    config.add_route('buying', '/buy', factory=HelloFactory)
    config.add_route('reserve', 'reserve', factory=HelloFactory)
