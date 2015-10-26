import os
# init django enviroment
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
from scraper.utils import setup_django_env
setup_django_env(os.path.join(PROJECT_ROOT, '../website/'))


from apps.common.tasks.mailer import MailerTask

m = MailerTask()
m.run()
