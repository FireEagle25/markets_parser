import sys

from excel_interface import load_data, save_data
from parsers.parser import Parser
from parsers.parser_implementations.buygoods_parser import BuygoodsParser
from parsers.parser_implementations.gearbest_parser import GearbestParser

GEARBEST_PARSER_ARG = 'gearbest'
BUYGOODS_PARSER_ARG = 'buygoods'


def show_hint():
    print('Необходимо указать в качетсве первого аргумента сайт с которого получать данные. Доступные варианты: ' + GEARBEST_PARSER_ARG + ', ' + BUYGOODS_PARSER_ARG + '.')
    print('В качестве второго аргумента можно указать имя входного файла')
    print('В качестве третьего аргумента можно указать имя выходного файла')


def get_args():
    if len(sys.argv) < 2:
        show_hint()
        exit()
    if sys.argv[1] not in [BUYGOODS_PARSER_ARG, GEARBEST_PARSER_ARG]:
        show_hint()
        exit()
    return sys.argv[1:]


def main():
    args = get_args()
    parser = Parser

    if len(args) >= 2:
        data = load_data(args[1])
    else:
        data = load_data()

    if args[0] == GEARBEST_PARSER_ARG:
        parser = GearbestParser(data)
    elif args[0] == BUYGOODS_PARSER_ARG:
        parser = BuygoodsParser(data)

    parsed_data = parser.parse()

    if len(args) >= 3:
        save_data(parsed_data, args[2])
    else:
        save_data(parsed_data)

    print("Успешно завершено")


if __name__ == "__main__":
    main()