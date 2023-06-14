import logging


class CustomHandlers:
    def __init__(self):
        self._handlers = []

    def register(self, handler, args: dict = None, weight=0, is_raise=True):
        nh = self._Handler(handler, args, weight, is_raise)
        i = 0
        for handler in self._handlers:
            if handler.weight <= nh.weight:
                break
            i += 1
        self._handlers.insert(i, nh)

    def exec(self):
        for handler in self._handlers:
            handler.exec()

    class _Handler:
        weight = 0
        is_raise = False
        handler = None

        def __init__(self, handler, args: dict = None, weight=0, is_raise=True):
            self.handler = handler
            self.args = args
            self.weight = weight
            self.is_raise = is_raise

        def exec(self):
            try:
                if self.args:
                    self.handler(**self.args)
                else:
                    self.handler()
            except Exception as e:
                if self.is_raise:
                    raise Exception(e)
                else:
                    logging.error(e)