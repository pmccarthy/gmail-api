from __future__ import print_function

import httplib2
import os
import datetime
import oauth2client

from termcolor import colored
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--sender', '-s', '-S',  help="User or email address that you want to search for, e.g. nagios", required=True)
    parser.add_argument('--year',   '-y', '-Y',  help="Specify a Year e.g. 2015", required=True)
    parser.add_argument('--month',  '-m', '-M',  help="Specify a Month e.g. 12", required=True)
    parser.add_argument('--day',    '-d', '-D',  help="Specify a Day e.g. 1", required=True)
    parser.add_argument('--user_id','-u', '-U',  help="User ID. Default is set to me (Optional)")
    flags = parser.parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print (colored('Storing credentials to ' + credential_path, 'red'))
    return credentials

def ListMessagesMatchingQuery(service, user_id, query=''):
    response = service.users().messages().list(userId=user_id,q=query).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id, q=query,pageToken=page_token).execute()
        messages.extend(response['messages'])
    return messages

def return_tomorrows_date(date):
    date += datetime.timedelta(days=1)
    return date

def generate_results(date,sender, message_count):
    print (colored('Results', 'yellow'))
    print ('=======================================')
    print ('Date:  %s' % date)
    print ('From:  %s' % sender)
    print ('Mail:  %s' % message_count)
    print ('=======================================')

def main():
    if flags.user_id:
        user_id = flags.user_id
    else:
        user_id='me'
    req_date = ("%s-%s-%s" % (flags.year,flags.month,flags.day))
    date = datetime.datetime.strptime(req_date , '%Y-%m-%d').date()
    before_date = return_tomorrows_date(date)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    query = ('from:%s after:%s before:%s' % (flags.sender, date, before_date))
    messages = ListMessagesMatchingQuery(service,user_id,query)
    generate_results(req_date,flags.sender,len(messages))

if __name__ == '__main__':
    main()