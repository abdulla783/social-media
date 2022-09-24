from django.db.models import TextChoices


class RelationshipChoice(TextChoices):
    SINGLE = 'single'
    COMMITTED = 'committed'
    NO_INTEREST = 'no interest'
    MARRIED = 'married'
    COMPLICATED = 'complicated'
    