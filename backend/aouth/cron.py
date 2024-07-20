from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta
from users.models import User
from aouth.views import user_update_status
import logging

logger = logging.getLogger(__name__)

class CheckUserInactivityCron(CronJobBase):
    
    RUN_EVERY_MINS = 0.1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'aouth.cron.CheckUserInactivityCron'  # Unique code for this job

    def do(self):
        logger.info('Checking user inactivity and updating statuses...')
        now = timezone.now()
        inactivity_limit = timedelta(seconds=30)

        users = User.objects.all()

        for user in users:
            try:
                if user.username != 'root':
                    if now - user.last_activity > inactivity_limit and user.status != 'offline':
                        logger.info(f"User {user.username} is inactive. Updating status to offline.")
                        user.status = 'offline'
                        user.last_activity = None
                        user.save()
            except Exception as e:
                logger.error(f"Error updating status for user {user.id}: {e}")

        logger.info('Successfully checked user inactivity and updated statuses.')

class CheckUserUnverifiedCron(CronJobBase):
    RUN_EVERY_MINS = 0.1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'aouth.cron.CheckUserUnverifiedCron'  

    def do(self):
        print('Checking user verification status...')
        now = timezone.now()
        unverified_limit = timedelta(minutes=1)
        users = User.objects.all()

        for user in users:
            try:
                if user.username != 'root':
                    if user.is_verified is False and now - user.validation_code_expiration > unverified_limit:
                        logger.info(f"User {user.username} is unverified. Deleting user.")
                        user.delete()
            except Exception as e:
                logger.error(f"Error deleting user {user.id}: {e}")
