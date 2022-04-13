from django.conf import settings as dj_settings


class Settings:
    """Lazy settings"""

    @property
    def AUTHOR_BACKEND(self):
        from .backends import AuthorDefaultBackend
        return getattr(dj_settings, 'AUTHOR_BACKEND', AuthorDefaultBackend)

    @property
    def AUTHOR_CREATED_BY_FIELD_NAME(self):
        return getattr(dj_settings, 'AUTHOR_CREATED_BY_FIELD_NAME', 'author')

    @property
    def AUTHOR_UPDATED_BY_FIELD_NAME(self):
        return getattr(dj_settings, 'AUTHOR_UPDATED_BY_FIELD_NAME', 'updated_by')

    @property
    def AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE(self):
        return getattr(dj_settings, 'AUTHOR_DO_NOT_UPDATE_WHILE_USER_IS_NONE', True)

    @property
    def AUTHOR_MODELS(self):
        return getattr(dj_settings, 'AUTHOR_MODELS', None)

    @property
    def AUTHOR_IGNORE_MODELS(self):
        return getattr(
            dj_settings,
            'AUTHOR_IGNORE_MODELS',
            [
                'auth.user',
                'auth.group',
                'auth.permission',
                'contenttypes.contenttype',
            ],
        )

    def __getattr__(self, name):
        """
        Return the setting with the specified name, from the project settings
        (if overridden), else from the default values passed in during
        construction.

        :param name: name of the setting to return
        :type name: str
        :return: the named setting
        :raises: AttributeError -- if the named setting is not found
        """
        if hasattr(dj_settings, name):
            return getattr(dj_settings, name)

        if hasattr(self, name):
            return getattr(self, name)

        raise AttributeError("'{name}' setting not found".format(name=name))


settings = Settings()
