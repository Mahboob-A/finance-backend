from django.http import JsonResponse
from django.views import View

from loguru import logger


class TestLoggingView(View):
    """A simple view to test logging functionality.
    It logs messages at different levels and returns a JSON response
    indicating the completion of the logging test.
    """
    def get(self, request, *args, **kwargs):
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        
        return JsonResponse({"message": "Logging test completed successfully."})


