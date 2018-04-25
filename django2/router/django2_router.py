class Django2Router(object):
    """
    A router to control all database operations on models in the
    django2 application.
    """

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'django2':
            return 'django2_db'
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'django2':
            return 'django2_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'django2' or \
                obj2._meta.app_label == 'django2':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if db == 'django2_db':
            return app_label == 'django2'
        elif app_label == 'django2':
            return False
