#-*- coding: utf-8 -*-

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from pyramid.security import Allow, forget, remember
from ..models.mymodel import *
from datetime import *

# главная страница
@view_config(route_name='main', renderer='../templates/signin.jinja2')
def signin(request):
	if request.authenticated_userid == None:
		headers = forget(request)
	else: return HTTPFound(location='../cabinet', headers = None)
	return {'project': 'kek', 'users' :['1', '2', '3']}

# обработка логина
@view_config(route_name='logged', renderer='../templates/logged.jinja2', request_method='POST')
def login(request):
	DBSession = Session(bind=engine)
	result = DBSession.query(User).filter(User.email == request.params['username'], User.password == request.params['password']).first()
	if result != None:
		headers = remember(request, request.params['username'])
		return HTTPFound(location='../cabinet', headers = headers)
	return HTTPFound(location='../')

# личный кабинет
@view_config(route_name='cab', renderer='../templates/cabinet.jinja2', permission='view')
def my_page(request):
	DBSession = Session(bind=engine)
	user = DBSession.query(User).filter(User.email == request.authenticated_userid).first()
	client = DBSession.query(Client).filter(Client.user_id == user.id).first()
	orders = DBSession.query(Order).filter(Order.user == user.id).all()
	for order in orders:
		tickets = DBSession.query(Ticket).filter(Ticket.order_id == order.id).all()
		if len(tickets)==0:
			DBSession.delete(order)
			DBSession.commit()
	orders = DBSession.query(Order).filter(Order.user == user.id).all()	
	ords = []
	for order in orders:
		totalsum = 0;
		tickets = DBSession.query(Ticket).filter(Ticket.order_id == order.id).all()
		ticks = []
		for ticket in tickets:
			passenger = DBSession.query(Client).filter(Client.id == ticket.client_id).first()
			tick = {'tick_number':ticket.code, 'tick_name':passenger.name, 'tick_birth': passenger.birth, 'tick_document': passenger.document, 'tick_price': ticket.totalprice, 'ticket_seat': ticket.seat_id}
			totalsum = totalsum + ticket.totalprice
			ticks.append(tick)
			if (len(ticks) >0):
				seat = DBSession.query(Seat).filter(Seat.id == ticks[0]['ticket_seat']).first()
				flight = DBSession.query(Flight).filter(Flight.id == seat.flight_id).first()
				fromair = DBSession.query(Airport).filter(Airport.id == flight.airport_id).first()
				fromcity = DBSession.query(City).filter(City.id == fromair.city_id).first()
				toair = DBSession.query(Airport).filter(Airport.id == flight.toairport_id).first()
				tocity = DBSession.query(City).filter(City.id == toair.city_id).first()
				orderinfo = {'or_number': order.id, 'or_date': order.date, 'or_flightnumber': flight.number, 'or_fromcity': fromcity.name, 'or_fromport':fromair.name, 'or_tocity':tocity.name, 'or_toport':toair.name, 'or_fromdate':flight.date_dep, 'or_fromtime':flight.time_dep, 'or_todate':flight.date_arr, 'or_totime':flight.time_arr, 'tickets': ticks, 'total':totalsum}
		ords.append(orderinfo)
	return {'client': client, 'orders': ords}

# поиск билета (без ввода)
@view_config(route_name='search', renderer='../templates/flightsearch.jinja2', permission='view', request_method='GET')
def flight_search(request):
	DBSession = Session(bind=engine)
	cities = DBSession.query(City).all()
	categories = DBSession.query(Category).all()
	return {'cities' : cities, 'categories':categories, 'query':''}

# поиск билета (после запроса)
@view_config(route_name='search', renderer='../templates/flightsearch.jinja2', permission='view', request_method='POST')	
def flight_searching(request):
	DBSession = Session(bind=engine)
	cities = DBSession.query(City).all()
	categories = DBSession.query(Category).all()
	category = DBSession.query(Category).filter(Category.id == request.params['category']).first()
	try:
		fromcities = DBSession.query(City).filter(City.name == request.params['fromcity']).all()
		results = []
		query = u'рейсы из ' + request.params['fromcity'] + u' в ' + request.params['tocity'] + u' на ' + request.params['date'] + u': ' + category.name + u', ' + request.params['count'] + u' билет(-а)'
		for fcity in fromcities:
			fair = DBSession.query(Airport).filter(Airport.city_id == fcity.id).first()
			tocities = DBSession.query(City).filter(City.name == request.params['tocity']).all()
			for tocity in tocities:
				toair = DBSession.query(Airport).filter(Airport.city_id == tocity.id).first()
				flights = DBSession.query(Flight).filter(Flight.airport_id == fair.id, Flight.toairport_id == toair.id, Flight.date_dep == request.params['date']).all()
				avalflights = []
				for flight in flights:
					seat = DBSession.query(Seat).filter(Seat.flight_id == flight.id, Seat.category_id == category.id, Seat.count>=request.params['count']).first()
					if seat != None:				
						result = {'number': flight.number, 'fromcity': fcity.name, 'fromport': fair.name, 'tocity':tocity.name,'toport':toair.name, 'fromdate': flight.date_dep, 'fromtime': flight.time_dep, 'todate': flight.date_arr, 'totime': flight.time_arr, 'tarif': seat.price, 'tax': seat.tax, 'total': (seat.price+seat.tax)*float(request.params['count']), 'baggage': seat.baggage, 'r_id':seat.id, 'p_count': request.params['count']}
						results.append(result)
		return {'cities': cities, 'categories': categories, 'flights': results, 'query': query}
	except: return {'cities': cities, 'categories': categories, 'flights': results, 'query': query}

# логаут
@view_config(route_name='logouted', renderer='../templates/logouted.jinja2')
def logout(request):
	headers = forget(request)
	return HTTPFound(location=request.route_url('main', name='log out!!!'), headers=headers)

# ввод данных о пассажирах
@view_config(route_name='buying', renderer='../templates/buy.jinja2')
def buy(request):
	DBSession = Session(bind=engine)
	cuser = DBSession.query(User).filter(User.email == request.authenticated_userid).first()
	now = datetime.now()
	#stringdate = str(now.year)+'-'+ str(now.month)+'-'+ str(now.day)+' '+ str(now.hour)+':'+ str(now.minute)+':'+ str(now.second)
	new_order = Order(date = now, user = cuser.id)
	DBSession.add(new_order)
	DBSession.commit()
	orders = DBSession.query(Order).all()
	order = orders[-1]
	items = []
	for i in range(1, int(request.params['count'])+1):
		items.append(i)
	seat = DBSession.query(Seat).filter(Seat.id == request.params['seat']).first()
	category = DBSession.query(Category).filter(Category.id == seat.category_id).first()
	flight = DBSession.query(Flight).filter(Flight.id == seat.flight_id).first()
	fair = DBSession.query(Airport).filter(Airport.id == flight.airport_id).first()
	toair = DBSession.query(Airport).filter(Airport.id == flight.toairport_id).first()
	fcity = DBSession.query(City).filter(City.id == fair.city_id).first()
	tocity = DBSession.query(City).filter(City.id == toair.city_id).first()
	total = float(request.params['count'])*(seat.price+seat.tax)
	info = {'number': flight.number, 'fair':fair.name, 'toair':toair.name, 'fcity':fcity.name, 'tocity':tocity.name, 'depdate':flight.date_dep, 'deptime':flight.time_dep, 'arrdate':flight.date_arr, 'arrtime':flight.time_arr, 'total':total, 'ind': request.params['count'], 'category': category.name, 'order': order}
	return {'counting' : items, 'info': info}






db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_bookingsystem_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
