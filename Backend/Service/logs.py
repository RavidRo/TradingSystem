from Backend.response import Response
from logging import info, warning, critical, basicConfig
import traceback


basicConfig(
    filename="logs.txt",
    format="%(asctime)s %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    filemode="a",
)


def logging(function):
    def inner(*args, **kwargs):
        # str = (
        #     f"Function: {function.__name__} , args: {args} {kwargs}  , result: "
        #     + "{level} - {result}"
        # )

        # try:
        result = function(*args, **kwargs)
        return result

    #     if result.succeeded():
    #         info(str.format(level="success", result=result.object))
    #     else:
    #         warning(str.format(level="fail", result=result.get_msg()))
    #     return result

    # except Exception:
    #     critical(str.format(level="exception", result=traceback.format_exc()))
    #     return Response(False, msg="An unexpected error as occurred")

    return inner