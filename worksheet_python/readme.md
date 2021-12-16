a Python class definition Worksheet for the simple spreadsheet objects (work-sheets) described below. A worksheet is a two-dimensional arrangement of cells, each
of which contains a simple value (string, integer or float). The columns are indexed using letters ('A', 'B', and so on{ at most 26!) while the rows are indexed numerically
beginning at one. Each cell has a label of the form \B3" consisting of its column letter and its row number.

w.read cell(label) -  Return the value in the cell denoted by the string 'label'. Ignore the possibility of there being no cell with that label.

w.write cell(label, newval) -  Replace the value in the cell denoted by the string `label` with the value of parameter `newval`. Return the old value from that cell. Ignore
the possibility of there being no cell with that label.

w.append(self, newvals) - Append a new row at the end of this worksheet i.e. beneath all the existing rows. Parameter `newvals` is a list and is optional. If `newvals`
is provided, use its values to populate the cells of the new row left to right. If `newvals` is not provided, the cells in the new row are populated with the value None.

w.show() - Print out the contents of the worksheet.
