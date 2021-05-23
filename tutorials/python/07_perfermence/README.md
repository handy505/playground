# ISSUE: AttributeError: module 'time' has no attribute 'clock'

ref: https://stackoverflow.com/questions/58569361/attributeerror-module-time-has-no-attribute-clock-in-python-3-8


time.clock() had deprecated since Python 3.3
use time.perf_counter() or time.procss_time() insted.

