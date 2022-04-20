from evraz.classic.app.errors import AppError


class NotFound(AppError):
    msg_template = "Object not found"
    code = 'not_found'


class NotAvailable(AppError):
    msg_template = "Object not available"
    code = 'not_available'
