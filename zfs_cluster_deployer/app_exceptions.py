
from flask_restful import abort


class HTTPExceptions(object):
    msg = "HTTP Error: %s"

    @classmethod
    def not_found(cls, message=msg % "Object does not exist"):
        abort(404, message=message)

    @classmethod
    def already_exists(cls, message=msg % "Object already exists"):
        abort(409, message=message)

    @classmethod
    def internal_server_error(cls, message=msg % "Internal Server Error"):
        abort(500, message=message)

    @classmethod
    def missing_parameter(cls, message=msg % "Missing parameter"):
        abort(400, message=message)

    @classmethod
    def not_authorized(cls, message=msg % "Not authorized"):
        abort(401, message=message)

    @classmethod
    def method_not_allowed(cls, message=msg % "Method not allowed"):
        abort(405, message=message)

    @classmethod
    def time_out_error(cls, message=msg % "Time Out Error"):
        abort(504, message=message)