import xlrd
import xlwt


def read_data_from_excel(file_name, index=0):

    book = xlrd.open_workbook(file_name)
    sheet = book.sheet_by_index(index)
    nrows = sheet.nrows
    ncols = sheet.ncols
    data = []
    for i in range(nrows):
        row = []
        for j in range(ncols):
            row.append(sheet.cell_value(rowx=i, colx=j))
        data.append(row)

    return data


def write_data_to_file(file_name, data, index=0):
    import xlwt

    wb = xlwt.Workbook()
    ws = wb.add_sheet('sum')
    nrows = len(data)
    crows = len(data[0])
    for i in range(nrows):
        for j in range(crows):
            ws.write(i, j, data[i][j])

    wb.save(file_name)       


# print("The number of worksheets is {0}".format(book.nsheets))
# print("Worksheet name(s): {0}".format(book.sheet_names()))

# print("{0} {1} {2}".format(sh.name, )
# print("Cell D30 is {0}".format(sh.cell_value())

# for rx in range(sh.nrows):
#     print(sh.row(rx))






if __name__ == '__main__':

    data1 = read_data_from_excel('站亭宝盒总表(for巴士最新总表0719).xlsx')
    data2 = read_data_from_excel('站亭宝盒总表.xlsx')
    data3 = read_data_from_excel('站亭宝盒总表2.xlsx')
    data1.pop(0)
    data2.pop(0)
    data3.pop(0)

    data1_l = 30
    data2_l = 7
    data3_l = 38

    print(data1[0][2])
    print(data2[0][2])
    print(data3[0][2])
    
    flag = True

    for dt1 in data1:
        baima = dt1[2]
        flag = False
        for dt2 in data2:
            if baima == dt2[2]:
                if dt2[data2_l]:
                    flag = True
    
        for dt3 in data3:
            if baima == dt3[2]:
                # print(bool(dt3[data3_l]))
                if dt3[data3_l]:
                    flag = True
    
        if flag:
            dt1.append('OK')
        else:
            dt1.append('')
    
    for dt1 in data1:
        print(dt1[data1_l])
    
    write_data_to_file('sum.xls', data1)
