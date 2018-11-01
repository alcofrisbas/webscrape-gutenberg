import argparse
import sys
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", action="store", help="specify database file")
    parser.add_argument("action", action="store", help="what action to take [make|query|update]")
    # make args
    parser.add_argument("-r", "--range", action="store", nargs=2, help="range to capture when making db file", metavar='')
    # query args
    parser.add_argument("-q", "--query", action="store", nargs=2, help="query by col, then row", metavar='')
    parser.add_argument("--random-select", action="store", help="select n random records", metavar='')
    parser.add_argument("-f", "--filter", action="store", nargs=2, help="filter random selections by col and file", metavar='')
    parser.add_argument("-o", "--output_dir", action="store", default="saved_books", help="directory to save records", metavar='')

    args = parser.parse_args()
    if args.action == "make":
        print("making")
        if args.range:
            print("file range: {}-{}".format(args.range[0], args.range[1]))
        else:
            print("no range specified, aborting")
    elif args.action == "query":
        print("querying")
        if args.query:
            print(args.query)
        elif args.random_select:
            print(args.random_select)
        else:
            print("invalid query format")
    elif args.action == "update":
        pass
    else:
        print("'{}' is not a valid action".format(args.action))
    print(args)
