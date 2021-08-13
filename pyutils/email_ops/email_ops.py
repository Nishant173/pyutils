from typing import List, Optional
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from pyutils.general.data_io import (
    get_basename_from_filepath,
    get_extension,
)


def add_attachments_to_multipart_obj(
        multipart_obj: MIMEMultipart,
        filepaths_to_attachments: List[str],
    ) -> MIMEMultipart:
    """
    Adds attachments from the given filepaths to the given `MIMEMultipart` object.
    Returns `MIMEMultipart` object containing the attachments.
    """
    extension_to_mime_subtype_mapper = {
        'csv': 'octet-stream',
        'docx': 'octet-stream',
        'pdf': 'pdf',
        'xls': 'octet-stream',
        'xlsx': 'octet-stream',
    }
    for filepath in filepaths_to_attachments:
        extension = get_extension(filepath=filepath)
        mime_subtype = extension_to_mime_subtype_mapper.get(extension.lower(), None)
        if mime_subtype is None:
            raise Exception(
                f"Cannot attach '{filepath}', as this file extension is not supported.",
                f" Supported extensions are: {list(extension_to_mime_subtype_mapper.keys())}"
            )
        attachment = open(file=filepath, mode='rb')
        payload = MIMEBase(_maintype='application', _subtype=mime_subtype)
        payload.set_payload(payload=attachment.read())
        encoders.encode_base64(msg=payload)
        payload.add_header(
            _name='Content-Disposition',
            _value=f"attachment; filename={get_basename_from_filepath(filepath=filepath)}",
        )
        multipart_obj.attach(payload=payload)
    return multipart_obj


def send_email(
        from_email_id: str,
        from_email_id_password: str,
        to_email_ids: List[str],
        cc_email_ids: List[str],
        subject: str,
        body: str,
        filepaths_to_attachments: Optional[List[str]] = None,
    ) -> None:
    r"""
    Sends an email from one Email ID to one or more Email IDs, along with the attachments provided (if any).
    Accepts HTML tags for the `body` parameter.
    Note: Works only if the sender uses a Gmail ID.

    >>> send_email(
            from_email_id='sender_email_id@gmail.com',
            from_email_id_password='some_password',
            to_email_ids=['person1@gmail.com', 'person2@gmail.com'],
            cc_email_ids=['person3@gmail.com'],
            subject="Your subject",
            body="Your message",
            filepaths_to_attachments=[
                r"C:\user\files\file1.csv",
                r"C:\user\files\file2.docx",
                r"C:\user\files\file3.pdf",
                r"C:\user\files\file4.xls",
                r"C:\user\files\file5.xlsx",
            ],
        )
    """
    msg = MIMEMultipart()
    msg['From'] = from_email_id
    msg['To'] = ", ".join(to_email_ids)
    msg['Cc'] = ", ".join(cc_email_ids)
    msg['Subject'] = subject
    msg.attach(payload=MIMEText(_text=body, _subtype='html'))
    if filepaths_to_attachments is not None:
        msg = add_attachments_to_multipart_obj(
            multipart_obj=msg,
            filepaths_to_attachments=filepaths_to_attachments,
        )
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