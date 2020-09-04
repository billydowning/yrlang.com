from django.db import models
from users.models import CustomUser, UserRole
from jsonfield import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating


class Notification(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    payload = JSONField()

    def __str__(self):
        return self.name


class Review(models.Model):
    ONTIME = 'on_time'
    LATE = 'late'
    COMMUNICCATE_WELL, NEED_TO_BE_CLEARER = 'communicates_well', 'needs_to_be_clearer'
    EAST_TO_WORK, CHALLANGINF_TO_WORK = 'easy_to_work_with', 'challenging_to_work_with'

    REVIEW_CHOICES_1 = [
        (ONTIME, 'on time at location'),
        (LATE, 'late at locations'),

    ]
    REVIEW_CHOICES_2 = [
        (COMMUNICCATE_WELL, 'communicate welll'),
        (NEED_TO_BE_CLEARER, 'need to be clear'),

    ]
    REVIEW_CHOICES_3 = [
        (EAST_TO_WORK, 'easy to work'),
        (CHALLANGINF_TO_WORK, 'challanging to work with'),

    ]

    date_posted = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    review_choice_1 = models.CharField(max_length=30, choices=REVIEW_CHOICES_1, null=True, blank=True)
    review_choice_2 = models.CharField(max_length=30, choices=REVIEW_CHOICES_2, null=True, blank=True)
    review_choice_3 = models.CharField(max_length=30, choices=REVIEW_CHOICES_3, null=True, blank=True)
    rating = GenericRelation(Rating, related_query_name='review_start_rating')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewer",null=True, blank=True)
    reviewee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviewee", null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return self.reviewer.email + "    ----->  "+self.reviewee.email
