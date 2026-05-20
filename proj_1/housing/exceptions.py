class HousingServiceError(Exception):
    """Base exception for housing service errors."""


class InvalidRepairRequestError(HousingServiceError):
    """Raised when repair request data is invalid."""


class UnauthorizedRepairActionError(HousingServiceError):
    """Raised when user is not allowed to perform an action."""