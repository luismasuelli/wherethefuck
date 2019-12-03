"""
There will be only one entry point here: The search method.

Anyone (authenticated or not) can request a search which will involve:
  - The map bounding box (mandatory if no flags specified; ignored otherwise).
  - The requested regions (if any, will only search among them).
  - The requested categories (if any, will only search among them).
  - Flags: {bookmarked, rated, or both} will restrict the search
      to only include the bookmarked, rated, or either of them.
"""
