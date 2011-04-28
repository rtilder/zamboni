import os

from django.conf import settings

import commonware.log
from celeryutils import task

from amo.decorators import set_modified_on
import amo.signals
from amo.utils import resize_image

task_log = commonware.log.getLogger('z.task')


@task
def delete_photo(dst, **kw):
    task_log.info('[1@None] Deleting photo: %s.' % dst)

    if not dst.startswith(settings.USERPICS_PATH):
        task_log.error("Someone tried deleting something they shouldn't: %s"
                       % dst)
        return

    try:
        os.remove(dst)
    except Exception, e:
        task_log.error("Error deleting userpic: %s" % e)


@task
@set_modified_on
def resize_photo(src, dst, **kw):
    """Resizes userpics to 200x200"""
    task_log.info('[1@None] Resizing photo: %s' % dst)

    try:
        resize_image(src, dst, (200, 200))
        return True
    except Exception, e:
        task_log.error("Error saving userpic: %s" % e)
