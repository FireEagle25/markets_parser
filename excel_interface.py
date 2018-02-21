from openpyxl import load_workbook, Workbook

START_LOAD_DATA_COL = 2


def load_data(file_path="input.xlsx"):
    try:
        wb = load_workbook(file_path)
        values = []

        counter = START_LOAD_DATA_COL
        while True:
            value = wb[wb.sheetnames[0]]['A' + str(counter)].value
            if not value:
                break
            values.append(value)
            counter += 1
    finally:
        print('No input file')
        exit()

    return values


def save_data(products, file_path="output.xlsx"):
    wb = Workbook()

    sheet = wb.active

    sheet.title = "Товары"
    sheet.append(['Код', "Название", "Ссылка", "Вес упаковки", "Длина", "Ширина", "Высота"])

    for product in products:
        output_list = [product['id'], product['name'], product['url'], product['weight']]

        if isinstance(product['size'], list):
            output_list = output_list + [float(item) for item in product['size']]
        else:
            output_list.append(product['size'])

        sheet.append(output_list)

    wb.save(filename=file_path)