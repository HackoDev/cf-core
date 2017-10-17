from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import SimpleLazyObject
from model_utils.choices import Choices

PROFILE_TYPE_CHOICES = Choices(
    ('REGULAR', "Пользователь системы"),
    ('NCO', "Некомерческая организация"),
    ('ORGANIZATION', "ООО/ОАО")
)

MODERATE_STATUS_CHOICES = Choices(
    (None, 'WAIT', "Ожидает проверки"),
    (True, 'ALLOWED', "Разрешено"),
    (False, 'BANNED', "Отклонено"),
)


class ModerateQuerySet(models.QuerySet):
    def waiting(self):
        return self.filter(is_available=MODERATE_STATUS_CHOICES.WAIT)

    def allowed(self):
        return self.filter(is_available=MODERATE_STATUS_CHOICES.ALLOWED)

    def banned(self):
        return self.filter(is_available=MODERATE_STATUS_CHOICES.BANNED)


class ProjectQuerySet(ModerateQuerySet):
    def waiting(self):
        return super(ProjectQuerySet, self).waiting().filter(
            origin__isnull=True)

    def allowed(self):
        return super(ProjectQuerySet, self).allowed().filter(
            origin__isnull=True)

    def banned(self):
        return super(ProjectQuerySet, self).banned().filter(
            origin__isnull=True)

    def drafts(self):
        return super(ProjectQuerySet, self).filter(origin__isnull=False)


class ModerateManager(models.Manager):
    def get_queryset(self):
        return ModerateQuerySet(self.model, using=self.db)

    def allowed(self):
        return self.get_queryset().allowed()

    def banned(self):
        return self.get_queryset().banned()

    def waiting(self):
        return self.get_queryset().waiting()


class ProjectManager(ModerateManager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self.db)


class PublishedProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self.db).allowed().filter(
            owner__profile__base_type=PROFILE_TYPE_CHOICES.NCO)


class WaitProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self.db).waiting().filter(
            owner__profile__base_type=PROFILE_TYPE_CHOICES.NCO)


class BannedProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self.db).banned()


class DraftProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self.db).drafts().filter(
            owner__profile__base_type=PROFILE_TYPE_CHOICES.NCO)


class ProxyFileManager(ModerateManager):
    def __init__(self, *args, **kwargs):
        """
        ModelManager для выборки файлов связанных с конкретной сущностью.
        Будет использоваться при наследовании базовой модели файла.
        """

        super(ProxyFileManager, self).__init__(*args, **kwargs)
        self.content_type = SimpleLazyObject(
            lambda: ContentType.objects.get_for_model(
                self.model.related_model))

    def get_queryset(self):
        """
        Фильтрация записей на основе ContentType связанной модели. 
        """
        return super(ProxyFileManager, self).get_queryset().filter(
            content_type__id=self.content_type.id
        )


class PartnerManager(models.Manager):
    def get_queryset(self):
        return super(PartnerManager, self).get_queryset().filter(
            base_type=self.model.BASE_TYPE
        )
