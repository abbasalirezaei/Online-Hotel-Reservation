class ActivationCodeError(Exception):
    """Raised when activation code is invalid, expired, or already used."""
    pass

class PasswordMismatchError(Exception):
    """Raised when new password and confirmation do not match."""
    pass

class AlreadyHotelOwnerError(Exception):
    """Raised when user has already submitted a hotel owner request."""
    pass