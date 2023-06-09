# BWConfig.py

__version__ = "1.1.0"


class ConfigFile:
    """ simple config file support"""
    _recs = {}

    def __init__(self, fn):
        self._fh = open(fn, "rt")
        self.parse(self._fh)

    def parseline(self, line):
        if line[0] == "#":
            return
        if "#" in line:
            line = line.split("#", 2)[0]
        if "=" not in line:
            return
        (lhs, rhs) = line.split("=", 2)
        self._recs[lhs.strip()] = rhs.strip()

    def parse(self, fh):
        for line in fh.readlines():
            self.parseline(line)

    def recs(self):
        return self._recs


def test():
    import sys
    fn = sys.argv[1] if len(sys.argv) > 1 else "test.conf"

    try:
        conf = ConfigFile(fn)
    except IOError as error:
        print("could not open {}, ".format(fn), error)
    else:
        recs = conf.recs()
        for k in sorted(recs):
            print("{} is [{}]".format(k, recs[k]))


if __name__ == "__main__":
    test()
