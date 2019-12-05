from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import Serializer, CharField, EmailField, RelatedField, IntegerField, ValidationError
from .transient import *
from ...models import POI


InvalidFlow = Exception("Invalid flow - please review internal usage of this serializer")


class CreateOnlySerializer(Serializer):
    """
    This base serializer only creates instances, but does not update.
    """

    def update(self, instance, validated_data):
        raise InvalidFlow


class RegisterSerializer(CreateOnlySerializer):
    """
    Serializer for registration. Involves:
      username
      e-mail
      password
      password confirmation
    """

    username = CharField(required=True)
    email = EmailField(required=True)
    password = CharField(required=True)
    password_confirmation = CharField(required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise ValidationError(_("Passwords don't match"))

    def create(self, validated_data):
        return RegisterAction(validated_data['username'], validated_data['email'], validated_data['password'],
                              validated_data['password_confirmation'])


class LoginSerializer(CreateOnlySerializer):
    """
    Serializer for log-in. Involves:
      username
      password
    """

    username = CharField(required=True)
    password = CharField(required=True)

    def create(self, validated_data):
        return LoginAction(validated_data['username'], validated_data['password'])


class ChangePasswordSerializer(CreateOnlySerializer):
    """
    Serializer for password change. Involves:
      current password
      new password
      new password confirmation
    """

    current_password = CharField(required=True)
    new_password = CharField(required=True)
    new_password_confirmation = CharField(required=True)

    def validate(self, attrs):
        if attrs['current_password'] == attrs['new_password']:
            raise ValidationError(_("New password must be different"))
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise ValidationError(_("Passwords don't match"))

    def create(self, validated_data):
        return ChangePasswordAction(validated_data['current_password'], validated_data['new_password'],
                                    validated_data['new_password_confirmation'])


class RequestPasswordReset(CreateOnlySerializer):
    """
    Serializer for request password reset. Involves:
      username
    The e-mail is assumed from the username.
    """

    username = CharField(required=True)

    def create(self, validated_data):
        return RequestPasswordResetAction(self.username)


class ResetPasswordSerializer(CreateOnlySerializer):
    """
    Serializer for password reset. Involves:
      recovery key
      new password
      new password confirmation
    """

    recovery_key = CharField(required=True)
    new_password = CharField(required=True)
    new_password_confirmation = CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise ValidationError(_("Passwords don't match"))

    def create(self, validated_data):
        return ResetPasswordAction(validated_data['recovery_key'], validated_data['new_password'],
                                   validated_data['new_password_confirmation'])


class CloseAccountSerializer(CreateOnlySerializer):
    """
    Serializer for close account. Involves:
      username
      current password
    Just for actual check of the data for the currently logged user.
    """

    username = CharField(required=True)
    password = CharField(required=True)

    def create(self, validated_data):
        return CloseAccountAction(validated_data['username'], validated_data['password'])


class RatePOISerializer(CreateOnlySerializer):
    """
    Serializer for POI rate. Involves:
      poi
      score
    """

    poi = RelatedField(queryset=POI.objects.all(), required=True)
    score = IntegerField(min_value=0, max_value=10, required=True)

    def create(self, validated_data):
        return RatePOIAction(self.poi, self.score)


class UnratePOISerializer(CreateOnlySerializer):
    """
    Serializer for POI unrate. Involves:
      poi
    """

    poi = RelatedField(queryset=POI.objects.all(), required=True)

    def create(self, validated_data):
        return UnratePOIAction(validated_data['poi'])


class BookmarkPOISerializer(CreateOnlySerializer):
    """
    Serializer for POI bookmark. Involves:
      poi
    """

    poi = RelatedField(queryset=POI.objects.all(), required=True)

    def create(self, validated_data):
        return BookmarkPOIAction(validated_data['poi'])


class UnbookmarkPOISerializer(CreateOnlySerializer):
    """
    Serializer for POI unbookmark. Involves:
      poi
    """

    poi = RelatedField(queryset=POI.objects.all(), required=True)

    def create(self, validated_data):
        return UnbookmarkPOIAction(validated_data['poi'])


class MovePOIBookmarkSerializer(CreateOnlySerializer):
    """
    Serializer for POI bookmark movement. Involves:
      poi
      before
    """

    poi = RelatedField(queryset=POI.objects.all(), required=True)
    before = RelatedField(queryset=POI.objects.all(), required=True)

    def create(self, validated_data):
        return MovePOIBookmarkAction(validated_data['poi'], validated_data['before'])


# Two endpoints will not have actions: logout, get profile.
