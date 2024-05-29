class SparseMatrix:
    """ 
        The sparse matrix class will contain all
        my functions: load_matrix(), add(), subract(), multiply(),
        divide()
    
    """

    def __init__(self, matrixPath=None, numRow=None, numCol=None):

        """if a file path is passed, 
            we will load the file in 
            load_matrix function

            else:
            we will just set the rows and col
            args passed in
        """

        if matrixPath:
            self.load_matrix(matrixPath)

        else:
            self.numRow = numRow
            self.numCol = numCol
            self.values = []

    def load_matrix(self, matrixPath):

        """
            We will read our input files
            and set our number of rows and cols
            we will then set parse the row, col and value
            of each matrix
        """
        self.values = []

        with open (matrixPath, 'r') as file:
            lines = file.readlines()
            
            self.numRow = int(lines[0].split('=')[1])
            self.numCol = int(lines[1].split('=')[1])

            for line in lines[2:]:
                line = line.strip()
                # row, col , value = line
                #the above is not the correct way to extract our values
                #this is why we need the parse entry function to do this
                try:
                    row, col, value =self.parse_entry(line)
                    self.set_element(row, col, value)

                except ValueError:
                    raise ValueError("Wrong File Fromat, Please check file format")
                

    def parse_entry(self, line):

        """
            Here we check if the file fromat is like:
            (0, kk, kk) i.e starts and end with parenthesis
            and have three entries
            So we will just extract those three entries,
        """

        if not line.startswith('(') or not line.endswith(')'):

            raise ValueError("Wrong File Fromat, Please check file format")

        parts = line[1:-1].split(',')

        if len(parts) != 3:
            raise ValueError('Wrong File Fromat, Please check file format')
        
        try:

            row = int(parts[0].strip())
            col = int(parts[1].strip())
            value = int(parts[2].strip())


        except ValueError:
            raise ValueError("Wrong File Fromat, Please check file format")
            
        return row, col, value
     

    def set_element(self, currRow, currCol, value):

        """
            Here we will set each line in this format:
            (row, col): value in the values object 
            so that when doing the matrix operation we will just 
            use the values of each file
        
        """
        if value != 0:
            self.values = [currRow, currCol, value]
        elif (currRow, currCol) in self.values:
            del self.values[(currRow, currCol)]



        


    def get_element(self, currRow, currCol):
        """This fuction will retrieve the value of the matrix 
        col and row passed into to:

        by default zero is the value if col or row not found
        """

        return self.values.get((currRow, currCol), 0)
    

    def add(self, other):
        for item in self.values:
            print(item)
            

        


            


if __name__ == "__main__":
    matirx =SparseMatrix(matrixPath='./Sample_Inputs/easy_sample_01_2.txt')
    matirx.add(None)
    