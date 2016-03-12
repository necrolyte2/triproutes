import os
from pyramid.config import Configurator
from sqlalchemy import engine_from_config, create_engine

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Try to pull database url from environment(for Heroku, or whatever)
    db_url = os.environ.get('DATABASE_URL', None)
    if db_url is not None:
        try:
            engine = create_engine(os.environ['DATABASE_URL'])
        except Exception as e:
            print "Unable to connect with DATABASE_URL {0}".format(db_url)
            raise e
    else:
        engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('add_trip', '/trips/add')
    config.add_route('trips', '/trips')
    config.add_route('view_trip', '/trips/{tripid}')
    config.add_route('add_plop', '/plops/add')
    config.add_route('edit_plop_attr', '/plops/edit')
    config.add_route('map_trip', '/trips/map/{tripid}')
    config.add_route('complete_trip', '/trips/{tripid}/complete')
    config.scan()
    return config.make_wsgi_app()
