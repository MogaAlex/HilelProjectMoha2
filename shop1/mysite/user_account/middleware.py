import logging
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

logger = logging.getLogger(__name__)

class GodModeMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.require_god_mode = getattr(settings, 'GOD_MODE', True)

    def __call__(self, request, **kwds):
        logger.info("God mode ")
        if request.user.is_authenticated:
            user = request.user
            logger.info(f'{user} is checked')
            if user.first_name and user.first_name.startswith('GOD_'):
                response = self.get_response(request)
                return response
        if self.require_god_mode:
            logger.warning('user not god mode')
            return redirect(reverse('user_account:login'))
        else:
            logger.info('no god mode checks required')
            response = self.get_response(request)
            return response


