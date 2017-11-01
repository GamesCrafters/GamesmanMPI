import logging
import objgraph
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Set by init_debug, retains what the MPI process' rank is.
process_rank = -1


def init_debug(rank):
    """Given a rank creates a log file.

    Args:
    rank: The MPI rank of a process.
    """
    global process_rank
    process_rank = rank
    logging.basicConfig(filename='logs/proc' + str(rank), level=logging.DEBUG)


def debug_send(send):
    def func_wrapper(*args, **kwargs):
        for arg in args:
            # TODO
            pass
        return send(*args, **kwargs)
    return func_wrapper


def debug_recv(recv):
    def func_wrapper(*args, **kwargs):
        res = recv(*args, **kwargs)
        # TODO
        return res
    return func_wrapper


def debug_abort(abort):
    def func_wrapper():
        pp.pprint(objgraph.get_leaking_objects())
        abort()
    return func_wrapper
