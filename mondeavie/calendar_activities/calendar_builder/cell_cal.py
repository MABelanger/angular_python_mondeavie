class Cell:
    def __init__(self, rowspan=None, data="", row_number=None,\
            visible=False, day_number=0, is_label=False, url=""):
        self.rowspan = rowspan 
        self.data = data
        self.row_number = row_number
        self.visible = visible
        self.day_number = day_number
        self.is_label = is_label
        self.url = url

    def __str__(self):
        return u'_Cell : rowspan:%s , data:%s , row_number:%s, visible:%s,\
            day_number:%s'\
            %(self.rowspan, self.data, self.row_number, self.visible, self.day_number)

    def __repr__(self):
        return self.__str__()