# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete, post_save

invalidate_signals = [post_delete, post_save]
