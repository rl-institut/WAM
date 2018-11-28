
from wam.admin import wam_admin_site
from meta import models

wam_admin_site.register(models.Source)
wam_admin_site.register(models.SourceCategory)
