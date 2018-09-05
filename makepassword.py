#!/usr/bin/env python3
"""generate plaintext password"""

import random
CHOICES = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$^&*()+/?,."
PASSWORD_LENGTH = 200
print("".join([random.SystemRandom().choice(CHOICES) for _ in range(PASSWORD_LENGTH)]))
