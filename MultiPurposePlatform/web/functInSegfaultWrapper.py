#! /usr/bin/env python3

# std imports
import multiprocessing as mp


def parametrized(dec):
    """This decorator can be used to create other decorators that accept arguments"""

    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)

        return repl

    return layer


@parametrized
def sigsev_guard(fcn, default_value=None, timeout=None):
    """Used as a decorator with arguments.
    The decorated function will be called with its input arguments in another process.

    If the execution lasts longer than *timeout* seconds, it will be considered failed.

    If the execution fails, *default_value* will be returned.
    """

    def _fcn_wrapper(*args, **kwargs):
        q = mp.Queue()
        p = mp.Process(target=lambda q: q.put(fcn(*args, **kwargs)), args=(q,))
        p.start()
        p.join(timeout=timeout)
        exit_code = p.exitcode

        if exit_code == 0:
            return q.get()

        print('Process did not exit correctly. Exit code: {}'.format(exit_code))
        return default_value

    return _fcn_wrapper