from day_schedule_cal import DayScheduleCal, DayCal
import utils
import display

if __name__ == '__main__':

    ds1 = DayScheduleCal(0, 2, "data1") # Lundi de 0h a 2h AM 4 rowspan
    ds2 = DayScheduleCal(2, 4, "data2") # Lundi de 0h a 2h AM 4 rowspan
    ds3 = DayScheduleCal(10, 27, "data3") # Lundi de 0h a 2h AM 4 rowspan

    lundi = DayCal("lundi", 1)
    mardi = DayCal("mardi", 2)
    mercredi = DayCal("mercredi", 3)

    lundi.add_day_schedule(ds1)
    mardi.add_day_schedule(ds2)
    mercredi.add_day_schedule(ds3)


    week = []
    week.append(lundi)
    week.append(mardi)
    week.append(mercredi)


    row_lst = utils.get_row_lst(week)
    utils.add_col_hour(row_lst)

    display.print_css()
    display.print_table(row_lst)
    #print row_lst
    print utils.minute_to_row_number(44)
    print utils.get_row_number_start(510)