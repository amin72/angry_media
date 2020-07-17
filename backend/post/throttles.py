from rest_framework.throttling import UserRateThrottle
from rest_framework import permissions


class ImageDayRateThrottle(UserRateThrottle):
    """
    Implement throttlling to allow requests per day for none safe methods.
    """

    rate = '10/day'

    def allow_request(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().allow_request(request, view)
