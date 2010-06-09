import grok
import zope.app.appsetup.product
import zope.component
import zope.sendmail.delivery
import zope.sendmail.interfaces
import zope.sendmail.mailer
import zope.sendmail.queue


config = zope.app.appsetup.product.getProductConfiguration('mailer')
queue_path = config['queue-path']
hostname = config.get('hostname', 'localhost')
port = int(config.get('port', 25))
# treat username and password as non-existent if they're empty strings
username = config.get('username', None) or None
password = config.get('password', None) or None


mailer_object = zope.sendmail.mailer.SMTPMailer(
        hostname, port, username, password)


def mailer():
    return mailer_object


def delivery():
    return zope.sendmail.delivery.QueuedMailDelivery(queue_path)


def start_processor_thread():
    thread = zope.sendmail.queue.QueueProcessorThread()
    thread.setMailer(mailer_object)
    thread.setQueuePath(queue_path)
    thread.start()


grok.global_utility(
    mailer,
    provides=zope.sendmail.interfaces.IMailer,
    name='uvcsite.smtpmailer')
grok.global_utility(
    delivery,
    zope.sendmail.interfaces.IMailDelivery,
    name='uvcsite.maildelivery')
start_processor_thread()
