from cell_cal import Cell
'''
Convert col list to row list
'''
def get_row_lst(week):
    row_lst = []
    for row_number in range(0, 28):
        cell_lst = []
        for day in week:
            cell = day.get_cell(row_number)
            cell_lst.append(cell)
        row_lst.append(cell_lst)
    return row_lst


'''
add hour
'''
def add_col_hour(row_lst):
    for cell_lst in row_lst:
        first_cell = cell_lst[0]
        hour = (first_cell.row_number*30.0)/60 + 8.0

        # display hour only if is 1, 2 not 1.5, 2.5
        if hour == int(hour):
            data = str(int(hour)) + "h"
        else :
            data = ""

        cell = Cell(row_number=first_cell.row_number, data=data, visible=True, is_label=True)
        cell_lst.insert(0, cell)


def get_minute(hour):
    hr = str(hour).split(":")
    return int(hr[0])*60 + int(hr[1])

def minute_to_row_number(minute):
    return int(round((minute/30.0),0))

def get_row_number(hour_minute):
    minute = hour_minute - (8*60)
    return minute_to_row_number(minute)