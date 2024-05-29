class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        if matrixFilePath:
            self.load_from_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols
            self.values = {}

    def load_from_file(self, matrixFilePath):
        self.values = {}
        with open(matrixFilePath, 'r') as f:
            lines = f.readlines()
            self.numRows = int(lines[0].split('=')[1])
            self.numCols = int(lines[1].split('=')[1])
            for line in lines[2:]:
                line = line.strip()
                if line:
                    try:
                        row, col, value = self.parse_entry(line)
                        self.set_element(row, col, value)
                    except ValueError:
                        raise ValueError("Input file has wrong format")

    def parse_entry(self, line):
        if not line.startswith('(') or not line.endswith(')'):
            raise ValueError("Input file has wrong format")
        parts = line[1:-1].split(',')
        if len(parts) != 3:
            raise ValueError("Input file has wrong format")
        try:
            row = int(parts[0])
            col = int(parts[1])
            value = int(parts[2])
        except ValueError:
            raise ValueError("Input file has wrong format")
        return row, col, value

    def get_element(self, currRow, currCol):
        return self.values.get((currRow, currCol), 0)

    def set_element(self, currRow, currCol, value):
        if value != 0:
            self.values[(currRow, currCol)] = value
        elif (currRow, currCol) in self.values:
            del self.values[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must agree for addition.")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for key in self.values:
            result.set_element(key[0], key[1], self.get_element(key[0], key[1]) + other.get_element(key[0], key[1]))
        for key in other.values:
            if key not in self.values:
                result.set_element(key[0], key[1], other.get_element(key[0], key[1]))
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions must agree for subtraction.")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for key in self.values:
            result.set_element(key[0], key[1], self.get_element(key[0], key[1]) - other.get_element(key[0], key[1]))
        for key in other.values:
            if key not in self.values:
                result.set_element(key[0], key[1], -other.get_element(key[0], key[1]))
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions must agree for multiplication.")
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for (i, k) in self.values:
            for j in range(other.numCols):
                if (k, j) in other.values:
                    current_value = result.get_element(i, j)
                    result.set_element(i, j, current_value + self.get_element(i, k) * other.get_element(k, j))
        return result

def read_matrix(file_path):
    try:
        return SparseMatrix(matrixFilePath=file_path)
    except ValueError as e:
        print(f"Error reading matrix from file {file_path}: {e}")
        return None

def write_matrix(matrix, file_path):
    with open(file_path, 'w') as f:
        f.write(f"rows={matrix.numRows}\n")
        f.write(f"cols={matrix.numCols}\n")
        for (row, col), value in matrix.values.items():
            f.write(f"({row}, {col}, {value})\n")

def main():
    import os
    import sys

    if len(sys.argv) != 4:
        print("Usage: python app.py <operation> <matrix_file_1> <matrix_file_2>")
        sys.exit(1)

    operation = sys.argv[1]
    file1 = sys.argv[2]
    file2 = sys.argv[3]

    matrix1 = read_matrix(file1)
    matrix2 = read_matrix(file2)

    if not matrix1 or not matrix2:
        sys.exit(1)

    result = None
    if operation == "add":
        result = matrix1.add(matrix2)
    elif operation == "subtract":
        result = matrix1.subtract(matrix2)
    elif operation == "multiply":
        result = matrix1.multiply(matrix2)
    else:
        print(f"Unsupported operation: {operation}")
        sys.exit(1)

    result_file = os.path.join(os.path.dirname(file1), "result.txt")
    write_matrix(result, result_file)
    print(f"Result written to {result_file}")

if __name__ == "__main__":
    main()
