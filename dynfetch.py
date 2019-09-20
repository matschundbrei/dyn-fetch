#!/usr/bin/env python3
import configparser
import csv
from datetime import date
from datetime import timedelta
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

sum_records = 0
sum_requests = 0

start = date.today() - timedelta(days=30)

zones = dict()

def csvsum(csvvar):
    """
    cumulates the second column in the csv and returns it
    """
    sum = 0
    intread = csv.reader(csvvar.splitlines())
    next(intread)  # to skip the first line
    for row in intread:
        sum += int(row[1])
    return sum


for zone in zonelist:
    try:
        allrecs = zone.get_all_records()
        sum_records += len(allrecs)
        qpscsv = zone.get_qps(start_ts=start)
        effqs = csvsum(qpscsv['csv'])
        sum_requests += effqs
        print("Zone \"{0}\" has {1} records and gets about {2}k queries per month".format(zone.fqdn, len(allrecs), effqs/1000))
        zones[zone.fqdn] = dict({
                                'requests': effqs,
                                'records': len(allrecs)
                                })
    except DynectGetError:
        print("Zone \"{0}\" does not want to list records (secondary zone?)".format(zone.fqdn))


print("{0} records in {1} zones, approximately {2}k queries per month".format(sum_records, len(zonelist), sum_requests/1000))

with open('dynfetch-out.csv', 'w', newline='') as outcsv:
    csvw = csv.writer(outcsv, dialect='excel')
    csvw.writerow(['Zone FQDN', 'Number of Records', 'Number of Requests(Month)'])
    for fqdn in zones.keys():
        csvw.writerow([fqdn, zones[fqdn]['records'], zones[fqdn]['requests']])
    csvw.writerow(['TOTALS', sum_records, sum_requests])
