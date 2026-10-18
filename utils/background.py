"""Run slow work (network calls) off the UI thread and get the result back on it."""

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

_running = set()


class _Signals(QObject):
    done = Signal(object)
    failed = Signal(object)


class _Job(QRunnable):
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.signals = _Signals()

    def run(self):
        try:
            result = self.func()
        except Exception as error:  # passed back to the UI thread
            self.signals.failed.emit(error)
        else:
            self.signals.done.emit(result)


def run_in_background(func, on_done=None, on_error=None):
    """Call func() on a worker thread; on_done(result) / on_error(exception) run on the UI thread."""
    job = _Job(func)
    _running.add(job.signals)

    def finish(callback, value):
        _running.discard(job.signals)
        if callback:
            callback(value)

    job.signals.done.connect(lambda result: finish(on_done, result))
    job.signals.failed.connect(lambda error: finish(on_error, error))
    QThreadPool.globalInstance().start(job)
