from enum import Enum


class ResponseCategories(Enum):
    positive = 'resolved'
    neutral = 'basic'
    negative = 'complaint'


class Priorities(Enum):
    resolved = 'low'
    basic = 'medium'
    complaint = 'high'
