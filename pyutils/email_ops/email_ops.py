from typing import List
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from pyutils.general.data_io import get_basename_from_filepath


def send_email_with_excel_attachments(
        from_email_id: str,
        from_email_id_password: str,
        to_email_ids: List[str],
        cc_email_ids: List[str],
        subject: str,
        body: str,
        excel_filepaths_with_ext: List[str],
    ) -> None:
    r"""
    Sends an email from one Email ID to one or more Email IDs, along with the Excel attachments provided (if any).
    Accepts HTML tags for the `body` parameter.
    Note: Works only if the sender uses a Gmail ID.

    >>> send_email_with_excel_attachments(
            from_email_id='sender_email_id@gmail.com',
            from_email_id_password='some_password',
            to_email_ids=['person1@gmail.com', 'person2@gmail.com'],
            cc_email_ids=['person3@gmail.com'],
            subject="Your subject",
            body="Your message",
            excel_filepaths_with_ext=[
                r"C:\user\files\file1.xlsx",
                r"C:\user\files\file2.xlsx",
                r"C:\user\files\file3.xlsx",
            ],
        )
    """
    msg = MIMEMultipart()
    msg['From'] = from_email_id
    msg['To'] = ", ".join(to_email_ids)
    msg['Cc'] = ", ".join(cc_email_ids)
    msg['Subject'] = subject
    msg.attach(payload=MIMEText(_text=body, _subtype='html'))
    
    for excel_filepath_with_ext in excel_filepaths_with_ext:
        excel_filename_with_ext = get_basename_from_filepath(filepath=excel_filepath_with_ext)
        attachment = open(file=excel_filepath_with_ext, mode='rb')
        payload = MIMEBase(_maintype='application', _subtype='octet-stream')
        payload.set_payload(payload=attachment.read())
        encoders.encode_base64(msg=payload)
        payload.add_header(
            _name='Content-Disposition',
            _value=f"attachment; filename={excel_filename_with_ext}",
        )
        msg.attach(payload=payload)
    
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.ehlo()
    server.login(user=from_email_id, password=from_email_id_password)
    server.sendmail(
        from_addr=msg['From'],
        to_addrs=msg['To'].split(',') + msg['Cc'].split(','),
        msg=msg.as_string(),
    )
    server.quit()
    return None