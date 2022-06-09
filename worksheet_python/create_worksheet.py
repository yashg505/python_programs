

class worksheet:

    def __init__(self, name, max_cols):

        #self.max_row = max_row
        self.max_cols = max_cols
        self.name = name
        self.col_names = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        self.ws = {i:[] for i in self.col_names.split()[:self.max_cols]}
        self.max_rows = len(self.ws["A"])

    def read_cell(self, cell_ref):
        col, row = [i for i in cell_ref]
        return self.ws[col][int(row)-1]
    
    def write_cell(self, cell_ref, new_value):
        col, row = [i for i in cell_ref]
        self.ws[col][row-1] = new_value
    
    def append(self, new_value):
        for i,j in zip(self.col_names.split()[:self.max_cols], new_value):
            if j != None:
                self.ws[i].append(j)
            else:
                self.ws[i].append(None)
    
    def show(self):
        for i in self.ws.keys():
            print(f'\t{i}', end = "")
        print('\n')
        for i in self.ws.keys():
            print('========', end='========')
        print('\n')
        for i in range(len(self.ws["A"])):
            print(f'[  {i+1}] : ', end='')
            for j in self.ws.keys():
                print(self.ws[j][i], end='\t')
            print('\n')
        for i in self.ws.keys():
            print('--------', end='--------')
    
if __name__ == "__main__":
    ws = worksheet('sheet1', 4)
    ws.append(['Tom', "Harry", 78, 76])
    ws.append(['Tom1', "Harry1", 79, 96])
    print(ws.read_cell("A2"))
