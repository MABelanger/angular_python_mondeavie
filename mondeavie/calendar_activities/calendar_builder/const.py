class _Const(object):
    def constant(f):
        def fset(self, value):
            raise SyntaxError
        def fget(self):
            return f()
        return property(fget, fset)

    @constant
    def NUMBER_ROWS():
        return (22-8)*2 # 22h - 8h * 2 for 30 min = 28 rows

    @constant
    def HOUR_START():
        return 8

    @constant
    def NUMBER_MINUTES():
        return (22-8)*60  # 840 minutes
    @constant
    def NUMBER_DAYS():
        return 2