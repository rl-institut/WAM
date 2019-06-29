import logging
from requests.exceptions import ConnectionError

from exchangelib import Credentials, Account, Message, Mailbox
from exchangelib.errors import AutoDiscoverFailed
from wam.settings import WAM_EXCHANGE_ACCOUNT, WAM_EXCHANGE_EMAIL, WAM_EXCHANGE_PW


def send_email(to_email, subject, message):
    """Send E-mail via MS Exchange Server using credentials from env vars"""

    credentials = Credentials(WAM_EXCHANGE_ACCOUNT,
                              WAM_EXCHANGE_PW)
    try:
        account = Account(WAM_EXCHANGE_EMAIL,
                          credentials=credentials,
                          autodiscover=True)
    except ConnectionError:
        err_msg = 'Feedback-Form - Verbindungsfehler!'
        logging.error(err_msg)
        return False
    except AutoDiscoverFailed:
        err_msg = 'Feedback-Form - Konto- oder Authentifizierungsfehler!'
        logging.error(err_msg)
        return False
    except Exception as err:
        err_msg = f'Feedback-Form - Sonstiger Fehler: {err}'
        logging.error(err_msg)
        return False

    recipients = [Mailbox(email_address=to_email)]

    m = Message(account=account,
                folder=account.sent,
                subject=subject,
                body=message,
                to_recipients=recipients)

    try:
        m.send_and_save()
    except Exception as err:
        err_msg = f'Feedback-Form - Fehler beim Mailversand: {err}'
        logging.error(err_msg)
        return False

    return True
