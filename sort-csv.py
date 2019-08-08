import csv
from consolemsg import error, warn

args = None


def sortData(data, sequence, column, file_excluded):
    sorted_data = []
    for item in sequence:
        for info in data:
            if len(info) < column:
                data.remove(info)
            elif item.lower() == info[1].lower():
                sorted_data.append(info)
                data.remove(info)
                break
    if column:
        acum = 0
        excluded = getFileInfo(file_excluded)
        for info in data:
            if (info[1].lower() not in excluded):
                try:
                    acum += int(info[column - 1])
                except:
                    error("[ACUM] trying to accumulate a non integer value")
        item = []
        for i in xrange(column):
            if i is (column - 2):
                item.append("ALTRES")
            elif i is (column - 1):
                item.append(acum)
            else:
                item.append("-")
        sorted_data.append(item)
    return sorted_data


def getFileInfo(file_name):
    lines = []
    with open(file_name) as f:
        for line in f:
            lines.append(line.strip().lower())
    return lines


def parseArgs():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--f',
        default=None,
        help="--f + 'file_to_sort.csv'"
    )
    parser.add_argument(
        '--s',
        default=None,
        help="--s + 'sequence_with_the_sort_order.txt'"
    )
    parser.add_argument(
        '--tab',
        action='store_true',
        help="--tab => Indicates that separation uses tabulations instead of commas."
    )
    parser.add_argument(
        '--c',
        default=None,
        type=int,
        help="--c + N => Acumulates the values of all rows (from the specified column N) in the final row."
    )
    parser.add_argument(
        '--e',
        default=None,
        help="--e + 'file_with_the_names_we_want_to_exclude_in_acum.txt'"
    )
    parser.add_argument(
        '--o',
        default=None,
        help="--o + 'file_name_output.csv'"
    )
    return parser.parse_args()


def showInfo():
    print("REQUIERED: --f file_name.csv --s sequence.txt")
    print("OPTIONAL: --tab --acum int --e to_exclude.txt --o output.csv")
    print("HELP: --h or --help for help")


def main():
    global args
    args = parseArgs()

    if args.f is None or args.s is None:
        error("Missing arguments!")
        showInfo()
        return -1

    if args.tab:
        csv.register_dialect('tabs', delimiter='\t')

    sequence = getFileInfo(args.s)

    with open(args.f, "r+") as f:
        if args.tab:
            data = csv.reader(f, dialect='tabs')
            warn("Using TAB '\t' as separator!")
        else:
            data = csv.reader(f)
            warn("Using comma ',' as separator!")

        data = [row for row in data]
        sorted_data = sortData(data, sequence, args.c, args.e)

        if args.o is not None:
            out = open(args.o, "w")
            output = csv.writer(out)
        else:
            f.seek(0)
            f.truncate()
            output = csv.writer(f)

        for row in sorted_data:
            output.writerow(row)

        if args.o is not None:
            out.close()


if __name__ == '__main__':
    main()
