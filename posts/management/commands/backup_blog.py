from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.mail import EmailMessage
from django.core.management.commands import diffsettings, dumpdata

import datetime

class Command(NoArgsCommand):
    """Backup Blog Command
    
    TODO: cleanup, add options
    """
    help = 'Meant to be run as a Cron Job, backs up database data, emails to admins'

    def handle_noargs(self, **options):
        diff = diffsettings.Command()
        dump = dumpdata.Command()

        date = datetime.datetime.now().strftime('%b-%d-%y')
        text = 'blog backup '+date
        msg = EmailMessage(
            subject=text,
            body=text,
            to=[addy[1] for addy in settings.ADMINS]
        )
        dump_data = dump.handle()
        if dump_data:
            msg.attach(
                'dump_'+date+'.json',
                dump_data,
                'application/json'
            )
        msg.send()
