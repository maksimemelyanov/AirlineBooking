#-*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.security import Authenticated


#def sacrud_settings(config):
#    config.include('pyramid_sacrud', route_prefix='admin')
#    config.registry.settings['pyramid_sacrud.models'] = (
#        ('Справочники', [Category, City, Airport, ]),
#        ('Пользователи и клиенты', [User, Client]),
#	('Рейсы и наличие мест', [Flight, Seat]),
#	('Билеты и заказы', [Order, Ticket])
#    )

def main(global_config, **settings):
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    #config.include(sacrud_settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
