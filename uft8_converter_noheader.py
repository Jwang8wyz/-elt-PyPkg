import pandas as pd
import chardet

class File_utf8_Preprocessor:
    def __init__(self, file_path, delimiter):
        self.file_path = file_path
        self.delimiter = delimiter
        self.df = None

    def detect_encoding(self):
        with open(self.file_path, 'rb') as file:
            result = chardet.detect(file.read())
            return result['encoding']

    def read_and_convert(self):
        encoding = self.detect_encoding()
        self.df = pd.read_csv(self.file_path, delimiter=self.delimiter, encoding=encoding, dtype=str,header=None)

        # Convert all columns to strings first
        self.df = self.df.astype(str)
       
        # Then convert every value to UTF-8
        for col in self.df.columns:
            self.df[col] = self.df[col].apply(lambda x: x.encode('utf-8').decode('utf-8'))

    def get_dataframe(self):
        return self.df

    def save_to_csv(self,output_file_path):
        self.df.to_csv(output_file_path, index=False, encoding='utf-8')
        

# file=File_utf8_Preprocessor('/mnt/Reports/FreedomSFTP/PO_Due/PO_QTY_DUE_Report_CSV_20240217.csv','|')
# file.read_and_convert()
# df=file.get_dataframe()
# print(df)
# file.save_to_csv('/elt/data_bucket/PO_QTY_DUE_Report_CSV_demoutf8.csv')

