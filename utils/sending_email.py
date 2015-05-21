#-*- coding: utf8 -*-
import HR_project.settings as settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender():

    def __create_message(self, title, sender, recipients, html, plain):
        """ Create the email message container from the input args."""
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender
        #msg['To'] = ','.join(recipients)

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(plain, 'plain')
        part2 = MIMEText(html.encode('utf8'), 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        return msg

    def send(self, html, recipients, title):
        sender = settings.EMAIL_SENDER
        if not title:
            title = u'Новая вакансия!'
        print html, recipients, title
        msg = self.__create_message(
                title,
                sender,
                recipients,
                html,
                "This email uses HTML!"
            )

        try:
            smtpserver = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_HOST_PORT)
            #smtpserver.set_debuglevel(args.debug)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            # getpass() prompts the user for their password (so it never appears in plain text)
            '''
                Enter login and password here
            '''
            smtpserver.login(settings.EMAIL_LOGIN, settings.EMAIL_PASSWORD)
            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.
            smtpserver.sendmail(sender, recipients, msg.as_string())
            print "Message sent to '%s'." % recipients
            message = True
            smtpserver.quit()
        except smtplib.SMTPAuthenticationError as e:
            print "Unable to send message: %s" % e
            message = False

        return message