from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db.models import Max, F
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class ReducedUnicodeUsernameValidator(RegexValidator):
    regex = r'^[\w_]+$'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and _ characters.'
    )
    flags = 0


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model for this system. Users will not be able to interact
      between themselves (this is NOT a social network) but they may
      rate any POI in a 0-10 scale, and bookmark them.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and _ only.'),
        validators=[ReducedUnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """

        send_mail(subject, message, from_email, [self.email], **kwargs)

    def rate(self, poi, score):
        """
        Rates a POI with some score for this user.
        :param poi: The poi to rate.
        :param score: The score to give
        """

        score = max(0, min(10, score))
        rating, created = self.ratings.get_or_create(poi=poi, defaults={'score': score})
        if not created:
            rating.score = score
            rating.save()

    def unrate(self, poi):
        """
        Removes the rate of a POI for this user.
        :param poi: The poi to unrate.
        :return: True if the rating was deleted. False if no rating existed.
        """

        try:
            rating = self.ratings.get(poi=poi)
            rating.delete()
            return True
        except Rating.DoesNotExist:
            return False

    def bookmark(self, poi):
        """
        Adds a POI as bookmark (inserts it at last).
        :param poi: The POI to add.
        :return: The new or existing bookmark, and whether it was just created.
        """

        try:
            return self.bookmarks.get(poi=poi), False
        except Bookmark.DoesNotExist:
            order = 1 + (self.bookmarks.aggregate(max=Max('order'))['max'] or 0)
            return self.bookmarks.create(poi=poi, order=order), True

    def unbookmark(self, poi):
        """
        Removes the POI from bookmark (and fills the order gap).
        :param poi: The POI to remove from bookmarks.
        :return: Whether the POI was just removed.
        """

        try:
            bookmark = self.bookmarks.get(poi=poi)
            order = bookmark.order
            bookmark.delete()
            self.bookmarks.filter(order_gt=order).update(order=F('order') - 1)
            return True
        except Bookmark.DoesNotExist:
            return False

    def bookmark_move(self, bookmark, before=None):
        """
        Inserts a bookmark BEFORE another bookmark, or
          at the end of the user's bookmarks list.

        Both bookmarks must belong to the current user.
        :param bookmark: The bookmark to insert, which must exist a priori.
        :param before: The reference bookmark to insert the new bookmark
          before, or None to move the bookmark to the end of the list.
        :return:
        """

        def _popout(bookmark_to_pop):
            order = bookmark_to_pop.order
            bookmark_to_pop.order = 0
            bookmark_to_pop.save()
            self.bookmarks.filter(order_gt=order).update(order=F('order') - 1)

        def _pushback(bookmark_to_push):
            bookmark_to_push.order = 1 + (self.bookmarks.aggregate(max=Max('order'))['max'] or 0)
            bookmark_to_push.save()

        if bookmark.user != self:
            return False
        elif before is None:
            _popout(bookmark)
            _pushback(bookmark)
            return True
        elif before.user != self:
            return False
        else:
            _popout(bookmark)
            # Yes: Intentionally reload the `before` bookmark.
            before = self.bookmarks.get(id=before.id)
            # Now `bookmark.order` must be the same as `before.order`...
            bookmark.order = before.order
            # ...but before saving we must push elements in that/+ order, one step further.
            self.bookmarks.filter(order_gte=bookmark.order).update(order=F('order') + 1)
            # Now, save the bookmark.
            bookmark.save()
            return True


class Bookmark(models.Model):
    """
    Bookmarks are held by users (essentially, favorite POIs), and they keep a
      certain order.
    """

    # Timestamp fields.
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # References and order.
    user = models.ForeignKey(User, related_name='bookmarks', on_delete=models.PROTECT)
    poi = models.ForeignKey('POI', related_name='bookmarks', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = (('user', 'poi'), ('user', 'order'))


class Rating(models.Model):
    """
    Ratings are the users' scores given to different POIs.
    """

    # Timestamp fields.
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # References and score.
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.PROTECT)
    poi = models.ForeignKey('POI', related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])

    class Meta:
        unique_together = (('user', 'poi'),)
