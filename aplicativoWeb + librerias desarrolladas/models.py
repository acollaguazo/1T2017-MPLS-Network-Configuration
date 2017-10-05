from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse



# post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)