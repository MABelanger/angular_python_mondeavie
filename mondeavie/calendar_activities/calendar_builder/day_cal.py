from cell_cal import Cell
class DayCal:
    def __init__(self, day_name, day_number):
        self.day_name = day_name
        self.day_number = day_number
        self.cell_lst = []
        self.td_lst = []

    def add_day_schedule(self, day_schedule):
        rs = day_schedule.row_number_end - day_schedule.row_number_start
        for i in range(0, rs) :
            row_number = day_schedule.row_number_start + i
            if i is 0:
                cell = Cell(row_number=row_number, rowspan=rs,\
                    data=day_schedule.data,\
                    day_number=self.day_number, visible=True, url=day_schedule.url)
            else :
                cell = Cell(row_number=row_number, day_number=self.day_number,\
                    visible=False)

            self.cell_lst.append(cell)

    def get_cell(self, row_number):
        for cell in self.cell_lst:
            if cell.row_number == row_number:
                return cell
        return Cell(row_number=row_number, visible=True,\
                day_number=self.day_number) # Visible empty cell

    def get_cell_lst(self):
        return sorted(self.cell_lst, key=lambda cell: cell.row_number)

    def __str__(self):
        return u'Day : \n day_name:%s \n cell_lst:%s' %(self.day_name, self.cell_lst)

    def __repr__(self):
        return self.__str__()