class RegisterAction:
    """
    Action parsed from the registration endpoint.
    """

    def __init__(self, username, email, password, password_confirmation):
        self.username = username
        self.email = email
        self.password = password
        self.password_confirmation = password_confirmation


class LoginAction:
    """
    Action parsed from the login endpoint.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password


class ChangePasswordAction:
    """
    Action parsed from the internal change password endpoint (i.e. while logged in).
    """

    def __init__(self, current_password, new_password, new_password_confirmation):
        self.current_password = current_password
        self.new_password = new_password
        self.new_password_confirmation = new_password_confirmation


class RequestPasswordResetAction:
    """
    Action parsed from the external change password flow start (i.e. trigger a
      password reset change).
    """

    def __init__(self, username):
        self.username = username


class ResetPasswordAction:
    """
    Action parsed from the external change password endpoint (i.e. on password reset).
    Ideally, the recovery key uses the same django format for password reset.
    """

    def __init__(self, recovery_key, new_password, new_password_confirmation):
        self.recovery_key = recovery_key
        self.new_password = new_password
        self.new_password_confirmation = new_password_confirmation


class CloseAccountAction:
    """
    Action parsed from the close account endpoint.

    Since accounts are not that sensitive (they don't manage personal / identifying data),
      accounts can freely be opened / closed with no restrictions or more risks than only
      having to create all the bookmarks again.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password


class RatePOIAction:
    """
    Action parsed from the POI rate endpoint.
    """

    def __init__(self, poi, score):
        self.poi = poi
        self.score = score


class UnratePOIAction:
    """
    Action parsed from the POI unrate endpoint.
    """

    def __init__(self, poi):
        self.poi = poi


class BookmarkPOIAction:
    """
    Action parsed from the POI bookmark endpoint.
    """

    def __init__(self, poi):
        self.poi = poi


class MovePOIBookmarkAction:
    """
    Action parsed from the POI bookmark move endpoint.
    """

    def __init__(self, poi, before):
        self.poi = poi
        self.before = before


class UnbookmarkPOIAction:
    """
    Action parsed from the POI unbookmark endpoint.
    """

    def __init__(self, poi):
        self.poi = poi


# Two endpoints will not have actions: logout, get profile.
