#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 2020/09/13

from __future__ import print_function
import datetime
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    startDate = input('Enter start date in YYYY-MM-DD format ')
    finDate = input('Enter finish date in YYYY-MM-DD format ')

    yearStart, monthStart, dayStart = map(int,startDate.split('-'))
    yearFin, monthFin, dayFin = map(int,finDate.split('-'))

    now = datetime.datetime(yearStart, monthStart, dayStart).isoformat() + 'Z' # 'Z' indicates UTC time
    fin = datetime.datetime(yearFin, monthFin, dayFin).isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting the upcoming the events')
    #now = datetime.datetime(2020, 7, 1).isoformat() + 'Z'
    #print('Getting the upcoming 10 events')
    #events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                    maxResults=50, singleEvents=True,
    #                                    orderBy='startTime').execute()

    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=fin, singleEvents=True,
                                        orderBy='startTime').execute()
   
    events = events_result.get('items', [])

    sys.stdout = open('apointments', 'w')

    #with open('apointments.pdf', mode='w') as pdf_file:

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        
    #sys.stdout.buffer.write(pdf_file.write())
    sys.stdout.close()

if __name__ == '__main__':
    main()
