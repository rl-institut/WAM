import logging
from requests.exceptions import ConnectionError  # pylint: disable=import-error

from exchangelib import (
    Credentials,
    Account,
    Message,
    Mailbox,
)  # pylint: disable=import-error
from exchangelib.errors import AutoDiscoverFailed  # pylint: disable=import-error
from wam.settings import WAM_EXCHANGE_ACCOUNT, WAM_EXCHANGE_EMAIL, WAM_EXCHANGE_PW


def send_email(to_email, subject, message):
    """Send E-mail via MS Exchange Server using credentials from env vars

    Parameters
    ----------
    to_email : :obj:`str`
        Target mail address
    subject : :obj:`str`
        Subject of mail
    message : :obj:`str`
        Message body of mail

    Returns
    -------
    :obj:`bool`
        Success status (True: successful)
    """

    credentials = Credentials(WAM_EXCHANGE_ACCOUNT, WAM_EXCHANGE_PW)
    try:
        account = Account(
            WAM_EXCHANGE_EMAIL, credentials=credentials, autodiscover=True
        )
    except ConnectionError:
        err_msg = "Feedback-Form - Verbindungsfehler!"
        logging.error(err_msg)
        return False
    except AutoDiscoverFailed:
        err_msg = "Feedback-Form - Konto- oder Authentifizierungsfehler!"
        logging.error(err_msg)
        return False
    except Exception as err:  # pylint: disable=broad-except
        err_msg = f"Feedback-Form - Sonstiger Fehler: {err}"
        logging.error(err_msg)
        return False

    recipients = [Mailbox(email_address=to_email)]

    m = Message(
        account=account,
        folder=account.sent,
        subject=subject,
        body=message,
        to_recipients=recipients,
    )

    try:
        m.send_and_save()
    except Exception as err:  # pylint: disable=broad-except
        err_msg = f"Feedback-Form - Fehler beim Mailversand: {err}"
        logging.error(err_msg)
        return False

    return True
