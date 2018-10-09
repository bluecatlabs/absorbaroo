# Copyright 2018 BlueCat Networks. All rights reserved.

#Added for ABSORBAROO
from apscheduler.schedulers.background import BackgroundScheduler
from bluecat_portal.workflows.ABSORBAROO.utils import get_value
from bluecat_portal.workflows.ABSORBAROO.Whitelistdigest import absorbaroo_sync

try:
        interval = get_value('wl.config', 'interval')
        if interval == 0:
                interval = 86400

        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(absorbaroo_sync, 'interval', seconds=int(interval))
        scheduler.start()
except Exception: pass

