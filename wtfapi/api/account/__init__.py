"""
Account: This clump of functions manage the account features for the API.

Their functions are like:
  - Main account management.
    - Register with {username} {email} {password} {confirmation}.
    - Login with {username} {password}.
    - Reset password {recovery key} with {new password} {confirmation}.
    - Logout.
      - Requires user logged in.
    - Close account.
      - Requires user logged in.
  - Profile management (All of these require user logged in).
    - Get profile.
    - Change password with {old password} {new password} {confirmation}.
    - Rate place {uuid} with {score}.
    - Remove rate from place {uuid}.
    - Bookmark place {uuid} (it will add the bookmark to the end).
    - Unbookmark place {uuid}.
    - Move bookmark {uuid} to the end or, if specified {uuid_other}, before {uuid_other}.
"""
