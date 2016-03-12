import json

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Plop,
    Trip
    )


@view_config(route_name='trips', renderer='templates/trips.pt')
def trips(request):
    try:
        trips = DBSession.query(Trip).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'trips':trips}

@view_config(route_name='view_trip', renderer='templates/trip.pt')
def view_trip(request):
    tripid = request.matchdict['tripid']
    try:
        trip = DBSession.query(Trip).filter( Trip.id == tripid ).one()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'trip':trip}

@view_config(route_name='map_trip', renderer='templates/trip_map.pt')
def map_trip(request):
    # Lets map this muther fucker
    tripid = request.matchdict['tripid']
    # Get them plops
    plops = DBSession.query(Plop).filter( Plop.trip_id == tripid )
    # Give them plops
    return {'plops': plops}

@view_config(route_name='add_plop')
def add_plop(request):
    if request.method != 'POST':
        return Response('Failed', content_type='text/json', status_int=500)

    jsn = request.json_body
    print jsn
    trip_id = jsn.get( 'trip_id', None )
    annotation = jsn.get( 'annotation', None )
    plop = Plop( jsn['lat'], jsn['lng'], jsn['timestamp'], annotation, trip_id )
    try:
        DBSession.add(plop)
        DBSession.flush()
        DBSession.refresh(plop)
        jsn['id'] = plop.id
        jsn['datetime'] = str( plop.datetime )
        return Response( json.dumps(jsn), content_type='application/json; charset=utf-8', status_int=200 )
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

@view_config(route_name='add_trip')
def add_trip(request):
    trip = Trip('New Trip')
    DBSession.add(trip)
    DBSession.flush()
    DBSession.refresh(trip)
    trip = {'id': trip.id, 'name': trip.name, 'complete': trip.complete}
    return Response( json.dumps(trip), content_type='application/json; charset=utf-8', status_int=200 )

@view_config(route_name='edit_plop_attr')
def edit_plop_attr(request):
    if request.method != 'POST':
        return Response('Failed', content_type='text/json', status_int=500)
    id = request.POST['pk']
    plop = DBSession.query(Plop).filter( Plop.id == id ).one()
    attr = request.POST['name']
    val = request.POST['value']
    setattr( plop, attr, val )
    DBSession.flush()
    return Response(val, content_type='text/plain', status_int=200)

@view_config(route_name='complete_trip')
def complete_trip(request):
    if request.method != 'POST':
        return Response('Failed', content_type='text/json', status_int=500)
    tripid = request.matchdict['tripid']
    try:
        trip = DBSession.query(Trip).filter(Trip.id == tripid).one()
        trip.complete = True
        DBSession.flush()
    except DBAPIError as e:
        return Response(str(e), content_type='text/plain', status_int=500)
    return Response(str(trip.id), content_type='text/plain', status_int=200)
