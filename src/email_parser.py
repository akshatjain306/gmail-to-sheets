import base64
from bs4 import BeautifulSoup

def parse_email(message):
    payload = message['payload']
    headers = payload['headers']

    email_data = {
        'from': '',
        'subject': '',
        'date': '',
        'content': ''
    }

    for header in headers:
        name = header['name']
        value = header['value']

        if name == 'From':
            email_data['from'] = value
        elif name == 'Subject':
            email_data['subject'] = value
        elif name == 'Date':
            email_data['date'] = value

    def extract_body(parts):
        for part in parts:
            if part.get('parts'):
                return extract_body(part['parts'])
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
            if part['mimeType'] == 'text/html':
                data = part['body'].get('data')
                if data:
                    html = base64.urlsafe_b64decode(data).decode('utf-8')
                    return BeautifulSoup(html, 'html.parser').get_text()
        return ''

    if payload.get('parts'):
        email_data['content'] = extract_body(payload['parts'])
    else:
        body = payload['body'].get('data')
        if body:
            email_data['content'] = base64.urlsafe_b64decode(body).decode('utf-8')

    return email_data
