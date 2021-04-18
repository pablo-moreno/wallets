from .base import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment=ENVIRONMENT,
        release=APP_VERSION,
    )
