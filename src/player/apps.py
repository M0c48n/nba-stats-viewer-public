from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class PlayerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'player'

    def ready(self):
        from player.ap_scheduler import start
        logger.info('スケジュール実行が開始されました。')
        start()