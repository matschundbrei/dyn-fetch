#!/usr/bin/env python3
import configparser
from datetime import date
from datetime import timedelta
from csv import reader
from dyn.tm.session import DynectSession
from dyn.tm.zones import get_all_zones
from dyn.tm.errors import DynectGetError

config = configparser.ConfigParser()
config.read('dynfetch.ini')

session = DynectSession(config['dyn']['accountname'],
                        config['dyn']['username'],
                        config['dyn']['password']
                        )

zonelist = get_all_zones()

all_recs = 0
all_reqs = 0

start = date.today() - timedelta(days=30)

def csvsum(csvvar):
    """
    cumulates the second column in the csv and returns it
    """
    sum = 0
    intread = reader(csvvar.splitlines())
    next(intread)  # to skip the first line
    for row in intread:
        effq = int(row[1]) * 3600
        sum += effq
    return sum


for zone in zonelist:
    try:
        allrecs = zone.get_all_records()
        all_recs += len(allrecs)
        qpscsv = zone.get_qps(start_ts=start)
        effqs = csvsum(qpscsv['csv'])
        all_reqs += effqs
        print("Zone \"{0}\" has {1} records and gets about {2}k queries per month".format(zone.fqdn, len(allrecs), effqs/1000))
    except DynectGetError:
        print("Zone \"{0}\" does not want to list records (secondary zone?)".format(zone.fqdn))


print("{0} records in {1} zones, approximately {2}k queries per month".format(all_recs, len(zonelist), all_reqs/1000))
