import csv
import requests
from requests.exceptions import RequestException
import sys
import urllib
from datetime import datetime, date
import json
from tqdm import tqdm

MISSING_VINTAGE = 1990

# see: https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module
# see: https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions
# requests will not return a response if either Timout, ConnectionError,
# HTTPError, or TooManyRedirects is raised - RequestException

def push_records_to_api(csv_file_path, api_url, model, user, headers, session,
                        sam_version):
    failures = []
    results = []
    ncount = 0
    created = 0
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # skip units header and the sandia header
        next(reader)
        next(reader)
        for row in tqdm(reader):
            if model == 'cecmodule':
                row = cecmodule_handler(row)
            elif model == 'pvinverter':
                if sam_version is None:
                    raise ValueError(
                        'SAM version cannot be None for PV Inverter.')
                row = pvinverter_handler(row, sam_version)
            else:
                break
            if 'error' in row:
                failures.append(row)
                continue
            row['created_by'] = user
            row['modified_by'] = user
            try:
                response = session.post(api_url, json=row, headers=headers)
            except RequestException as exc_info:
                failures.append({
                    'error': 'requests error',
                    'exc_info': str(exc_info),  # make exc_info serializable
                    'data': row})
                continue
            name = row['Name']
            status_code, reason = response.status_code, response.reason
            location = None
            if status_code == 401:
                response.raise_for_status()
            elif status_code == 201:
                location = response.headers.get('Location', location)
                created += 1
            else:
                failures.append({
                    'error': 'not created',
                    'exc_info': response.text,  # might have exception info
                    'data': row})
            results.append({
                'name': name,
                'status': status_code,
                'reason': reason,
                'location': location})
            ncount += 1
    return failures, results, ncount, created


def cecmodule_handler(kwargs):
    # handle BIPV
    bipv = kwargs['BIPV'] == 'Y'
    kwargs['BIPV'] = bipv
    # handle date
    timestamp = kwargs['Date']
    try:
        timestamp = datetime.strptime(timestamp, '%m/%d/%Y')
    except (ValueError, TypeError) as exc_info:
        return {
            'error': 'date error',
            'exc_info': str(exc_info),  # make exc_info serializable
            'data': kwargs}
    kwargs['Date'] = datetime.strftime(timestamp, '%Y-%m-%d')
    # handle Length and Width
    if not kwargs['Length']:
        kwargs['Length'] = None
    if not kwargs['Width']:
        kwargs['Width'] = None
    return kwargs


def pvinverter_handler(kwargs, sam_version):
    cec_date = kwargs.get('CEC_Date')
    if cec_date is not None:
        try:
            cec_date = datetime.strptime(cec_date, '%m/%d/%Y')
        except ValueError as exc_info:
            if cec_date != 'n/a':
                return {
                    'error': 'date error',
                    'exc_info': str(exc_info),  # make exc_info serializable
                    'data': kwargs}
            cec_date = date(MISSING_VINTAGE, 1, 1)
        kwargs['CEC_Date'] = datetime.strftime(cec_date, '%Y-%m-%d')
    kwargs['SAM_Version'] = sam_version
    return kwargs


if __name__ == "__main__":
    # TODO: use optparse or click
    username = sys.argv[1]  # mikofski
    api_key = sys.argv[2]
    api_base = sys.argv[3]  # "http://127.0.0.1:8000"
    model = sys.argv[4]  # cecmodule --> /api/v1/cecmodule/
    csv_file_path = sys.argv[5]  # "deploy/libraries/CEC Modules.csv"
    try:
        sam_version = sys.argv[6]  # "2020.2.29.r2.ssc.240"
    except IndexError:
        sam_version = None
    schema = requests.get(urllib.parse.urljoin(api_base, '/api/v1'))
    schema = schema.json()
    model_schema = schema[model]
    api_url = urllib.parse.urljoin(api_base, model_schema['list_endpoint'])
    # /api/v1/user always responds, but objects could be empty
    users = requests.get(
        urllib.parse.urljoin(api_base, '/api/v1/user'),
        params={'username': username})
    users = users.json()
    user = users['objects'][-1]['resource_uri']
    headers = {
        "Authorization": f"ApiKey {username}:{api_key}",
        "Content-Type": "application/json"
    }
    with requests.Session() as session:
        failures, results, ncount, created = push_records_to_api(
            csv_file_path, api_url, model, user, headers, session, sam_version)
    # TODO: use logging
    with open('pvfree_cli.log', mode='w', encoding='utf-8') as f:
        f.write(f'Created count: {created}\n')
        f.write(f'count of failures {len(failures)}\n')
        f.write(f'total count of records {ncount}\n')
        f.write('Results\n')
        json.dump(results, f)
        f.write('Failures\n')
        json.dump(failures, f)
