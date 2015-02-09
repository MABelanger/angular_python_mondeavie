class DayScheduleCal:
    def __init__(self, row_number_start, row_number_end, data, url):
        self.row_number_start = row_number_start # Start minute
        self.row_number_end = row_number_end # End minute
        self.data = data
        self.url = url

    def __str__(self):
        return u'DayScheduleCal : \n row_number_start:%s \n row_number_end:%s'\
                %(self.row_number_start, self.row_number_end)