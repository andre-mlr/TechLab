import datetime
import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = Credentials.from_authorized_user_file('token.pickle', SCOPES)

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
            token.write(creds.to_json().encode())

    service = build('calendar', 'v3', credentials=creds)
    return service

def check_event_conflicts(start_time, end_time):
    """Verifica se há conflitos de eventos no Google Calendar."""
    service = authenticate_google()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if events:
        print("Conflito de horário encontrado. Não é possível agendar a reunião neste horário.")
        return True
    else:
        return False

def schedule_meeting(summary, description, start_time, end_time, attendees):
    service = authenticate_google()

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Sao_Paulo',
        },
        'attendees': [{'email': attendee} for attendee in attendees],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    if not check_event_conflicts(start_time, end_time):
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

def convert_to_utc(dt, tz):
    """Converte um datetime para UTC baseado no fuso horário especificado."""
    tz = datetime.timezone(datetime.timedelta(hours=tz))
    return dt.astimezone(tz).isoformat()

def redirect_to_agenda_link(email):
    """Redirects to the agenda link for scheduling a meeting."""
    summary = "Reunião de boas vindas"
    description = "reunião dedicada a retirar dúvidas gerais sobre a empresa"
    
    # Solicita a data e hora de início da reunião
    start_time_str = input("Informe a data e hora de início (formato YYYY-MM-DD HH:MM): ")
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
    start_time_utc = convert_to_utc(start_time, -3)  # -3 para o fuso horário de São Paulo

    # Solicita a data e hora de término da reunião com fuso horário de São Paulo
    end_time_str = input("Informe a data e hora de término (formato YYYY-MM-DD HH:MM): ")
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')
    end_time_utc = convert_to_utc(end_time, -3)  # -3 para o fuso horário de São Paulo
    
    
    # Lista de participantes da reunião
    attendees = [email, "d2021007221@unifei.edu.br.com"]

    if not check_event_conflicts(start_time_utc, end_time_utc):
        # Chama a função para agendar a reunião com as informações fornecidas
        schedule_meeting(summary, description, start_time_utc, end_time_utc, attendees)



