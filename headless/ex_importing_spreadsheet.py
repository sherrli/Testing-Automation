import spreadsheet

#print(spreadsheet.sheet)
x = spreadsheet.Spreadsheet()
#x.open_sheet('ex2')
print(x.client)
x.write_cell(5, 5, "pass\nfail")
