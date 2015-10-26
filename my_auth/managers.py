# -*- coding: utf-8 -*-
from django.db import models


class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)
