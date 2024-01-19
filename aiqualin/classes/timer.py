from time import perf_counter


class Timer:
    def __init__(self, name: str = "", no_print: bool = False) -> None:
        self.do_print = not no_print
        self.name = name

        self._start_time: float = -1.0
        self._end_time: float = -1.0
        self.intervals: list[float] = []

    def __enter__(self) -> None:
        self._start_time = perf_counter()

    def __exit__(self, *args, **kwargs) -> None:
        self._end_time = perf_counter()

        self.intervals.append(self._end_time - self._start_time)

        if self.do_print:
            name_to_print = self.name if self.name != "" else "Timer"
            print(f"{name_to_print} took {self.last_interval * 1000:.2f} ms")

    @property
    def last_interval(self) -> float:
        return self.intervals[-1]
