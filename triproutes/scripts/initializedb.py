import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Plop,
    Trip,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        example_trip = Trip('Example Trip')
        DBSession.add(example_trip)
    '''
        trip = Trip( '#2 Bus Home' ) 
        trip.complete = True
        DBSession.add(trip)
        DBSession.flush()
        DBSession.refresh(trip)
        plops = (
            Plop(39.004167,-77.05437,1401468900,'WRAIR',trip),
            Plop(38.994289,-77.033494,1401469680,'Colesville/EWHWY',trip),
            Plop(38.996024,-77.028472,1401470040,'Colesville/Georgia',trip),
            Plop(38.998158,-77.030157,1401470280,'Home',trip),
        )
        for plop in plops:
            DBSession.add(plop)
    '''
