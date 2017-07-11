import xlsxwriter
import string


# pip install XlsxWriter


class ExcelDriver(object):
    def __init__(self, file_path=None):
        self.file_path = file_path

        self.work_book = xlsxwriter.Workbook(self.file_path)
        self._is_inited = False

    def write(self, item):
        self.current_index += 1
        for name, value in item.items():
            if self.header_indexes.get(name):
                index = self.header_indexes[name]

                self.work_sheet.write('{}{}'.format(index, str(self.current_index)), value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.work_book.close()

    def init(self, sheet_name, headers):
        self._is_inited = True
        if not self.work_book:
            self.work_book = xlsxwriter.Workbook(self.file_path)
        self.work_sheet = self.work_book.add_worksheet(sheet_name)
        self.header_indexes = dict(zip(headers, string.ascii_uppercase[:len(headers)]))
        for name, index in self.header_indexes.items():
            self.work_sheet.write('{}1'.format(index), name)

        self.current_index = 1

    def switch_sheet(self, sheet_name, headers):
        if getattr(self, "work_sheet", None) and self.work_sheet.name == sheet_name:
            return

        self.init(sheet_name, headers)

    def close(self):
        self.work_book.close()


if __name__ == '__main__':
    fpath = 'test.xlsx'
    excel = ExcelDriver(fpath)

    with excel as f:
        f.switch_sheet("sheet_1", ["name", "age", "gender"])
        f.write({"name": "wenter", "age": 100, "gender": None})
        f.write({"name": "wenter_2", "age": 100, "gender": None})

