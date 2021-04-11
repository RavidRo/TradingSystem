from Backend.response import Response
import logging
import traceback


logging.basicConfig(
    filename="logs.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    filemode="a",
    force=True,
)


def loging(function):
    def inner(*args, **kwargs):
        msg = f"Function: {function.__name__} , args: {args[1:]} {kwargs}  , result: "
        to_format = "{level} - {result}"

        try:
            result = function(*args, **kwargs)
            if not isinstance(result, Response):
                logging.info(msg + to_format.format(level="success", result=result))
            elif result.succeeded():
                logging.info(msg + to_format.format(level="success", result=result.object))
            else:
                logging.warning(msg + to_format.format(level="fail", result=result.get_msg()))
            return result

        except Exception:
            logging.critical(
                msg + to_format.format(level="exception", result=traceback.format_exc())
            )
            return Response(False, msg="An unexpected error as occurred")

    return inner