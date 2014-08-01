# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import zope.component
import zope.sendmail
import email.MIMEText
import email.Header

from email.MIMEBase import MIMEBase
from email import Encoders
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE

from .. import log


def start_processor_thread(mailer_object, queue_path):
    thread = zope.sendmail.queue.QueueProcessorThread()
    thread.setMailer(mailer_object)
    thread.setQueuePath(queue_path)
    thread.start()


def send_mail(sender, recipient, subject, body, file=None, filename=None):
    '''
    Funktion zum versenden von Emails
    recipient muss als Liste übergeben werden
    body sollte einen formatierter String sein
    '''

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = COMMASPACE.join(recipient)  # List to String
    msg["Subject"] = email.Header.Header(subject, 'UTF-8')
    msg.attach(MIMEText(body.encode('utf-8'),'plain','utf-8'))

    # Attachment von Dateien
    if file != None:
        fn = file.split("/")
        fn = fn[-1]
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename=%s' % filename or fn
            )
        msg.attach(part)
    mailer = zope.component.getUtility(
        zope.sendmail.interfaces.IMailDelivery,
        name=u'uvcsite.maildelivery'
        )
    mailer.send(sender, recipient, msg.as_string())


def configure_mail(config, app):
    queue_path = config.get('queue-path')
    hostname = config.get('hostname', 'localhost')
    port = int(config.get('port', 25))
    # treat username and password as non-existent if they're empty strings
    username = config.get('username', None) or None
    password = config.get('password', None) or None

    mailer_object = zope.sendmail.mailer.SMTPMailer(
        hostname, port, username, password, force_tls=False)

    uvclight.global_utility(
        mailer_object,
        provides=zope.sendmail.interfaces.IMailer,
        name='uvcsite.smtpmailer',
        direct=True)

    uvclight.global_utility(
        zope.sendmail.delivery.QueuedMailDelivery(queue_path),
        zope.sendmail.interfaces.IMailDelivery,
        name='uvcsite.maildelivery',
        direct=True)

    start_processor_thread(mailer_object, queue_path)
    log('Emailer thread started.')
