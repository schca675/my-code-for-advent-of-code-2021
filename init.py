import os
import errno

for i in range(10, 26):
    filename = "Day{}/test_data.txt".format(i)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as f:
        f.write("")
    filename = "Day{}/data.txt".format(i)
    with open(filename, "w") as f:
        f.write("")