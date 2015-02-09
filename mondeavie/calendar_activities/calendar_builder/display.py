def print_day_name(day_name_lst):
    html = '<tr class="cal">'
    #html += '\t<td class="cal no-border hour"></td><!-- empty td for the day name -->'
    for day_name in day_name_lst:
        html+= '\t<td class="day-name">%s</td>' %(day_name)
    html += "</tr>"

    return html

def print_cell(cell, colspan, row_lst_len):
    html = ""
    if cell.row_number == 9 or cell.row_number == 18 : 
        break_title = ""
        if cell.row_number == 9 :
            break_title = "D&icirc;ner"
        if cell.row_number == 18 :
            break_title = "Souper"

        if colspan == False:
            html = '<td class="cal cal-break" colspan=%s>' %(row_lst_len)
            #html += 'border:1px solid #5A8727; background-color:#B0D788;text-align:center;">%s</td>' %(break_title)
            html += '&nbsp;</td>'
            # Need to add empty <tr> to display the correct colspan
            html += '<tr class="cal"></tr>' 
            colspan = True
        else:
            pass
            #html = '<td></td>'

    else:
        if cell.visible:
            html_class = ''
            if cell.data and not cell.is_label:
                html_class = 'top-bottom-border'
            if cell.is_label:
                html_class = 'no-border hour'

            if cell.rowspan :
                html = '<td class="cal %s" rowspan="%s">' %(html_class, cell.rowspan)
                html += '\t<a class="cal" href="%s">' %(cell.url)
                html += '\t<div style="height:100%">'
                html += '%s' %(cell.data)
                html += '\t</div>'
                html += '\t</a>'
                html += '\t</td>'
            else:
                html = '<td class="cal %s" >%s</td>' %(html_class, cell.data) #&nbsp

        # if the cell is not visible, comment the td
        else:
            html = "<!-- <td></td> -->"

        # append the column name at the end in comment
        html += "<!-- %s -->" %(cell.day_number)

    
    html = "\t" + html + "\n"

    return html, colspan

def is_row_empty(row):
    row_len = len(row)
    for day_number in range(0, row_len):
        cell = row[day_number]
        if cell.data != "" or cell.visible == False:
            return False
    return True


def print_tr(row_lst):
    html = ""
    for row_number in range(0,len(row_lst)):

        colspan = False
        row_lst_len = len(row_lst[row_number])

        #row_empty = is_row_empty(row_lst[row_number])
        #if row_empty == False :
        html += '<tr class="cal">'
        for day_number in range(0, row_lst_len):
            cell = row_lst[row_number][day_number]
            html_tmp, colspan = print_cell(cell, colspan, row_lst_len)
            html += html_tmp
        html += "</tr>"
    return html

def print_table(row_lst):
    html = '<table class="cal">'
    html += print_day_name(['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'])
    html += print_tr(row_lst)
    html += "</table>"

    return html