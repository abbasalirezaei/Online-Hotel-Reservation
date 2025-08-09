from django.db import models


class PaymentMethod(models.TextChoices):
    """Enumeration for payment methods."""
    ONLINE = 'online', 'Online Gateway'
    CASH = 'cash', 'Cash Payment'
    CARD = 'card', 'Card Payment'
    WALLET = 'wallet', 'Wallet Balance'
    CRYPTO = 'crypto', 'Cryptocurrency'
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'

class PaymentStatus(models.TextChoices):
    """Enumeration for actual payment status after booking."""
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'
    REFUNDED = 'refunded', 'Refunded'
    CANCELLED = 'cancelled', 'Cancelled'


