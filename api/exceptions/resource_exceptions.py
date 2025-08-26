class ResourceNotFoundException(Exception):
    pass

class ResourceConflictException(Exception):
    status_code = 409
    default_detail = 'Conflict: Resource already exists.'
    default_code = 'conflict'

class UnhandledResourceException(Exception):
    status_code = 500
    default_detail = 'An unexpected error occurred.'
    default_code = 'error'