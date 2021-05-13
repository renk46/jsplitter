import json, os, sys, argparse, logging

sys.stdout.reconfigure(encoding="utf-8")
dir = os.path.dirname(__file__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

_logger = logging.getLogger()
_logger.addHandler(handler)

def create_file(pathfile, data):
    path = os.path.dirname(pathfile)
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(pathfile, "w")
    f.write(json.dumps(data))
    f.close()

def split_json_array(json, piece=50, filename=False):
    partial_data = []
    filename = "%s_" % filename if filename else ''
    l = len(json)
    printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, rec in enumerate(json):
        partial_data.append(rec)
        if (i+1) % piece == 0:
            create_file("%s/output/%s%s.json" % (dir, filename, i+1), partial_data)
            partial_data = []
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    if len(partial_data) > 0:
        create_file("%s/output/%s%s.json" % (dir, filename, l), partial_data)

def split_json_file(pathfile, piece):
    try:
        _logger.debug("Load file: %s" % pathfile)
        json_data = json.loads(open(pathfile, 'r', encoding='utf-8').read())
        filename = os.path.basename(os.path.splitext(pathfile)[0])
        if piece: split_json_array(json_data, int(piece), filename=filename)
        else: split_json_array(json_data, filename=filename)
    except json.decoder.JSONDecodeError:
        _logger.warning("Failed to decode file: %s" % file)

def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

parser = argparse.ArgumentParser()
parser.add_argument('--path')
parser.add_argument('--piece')
args = parser.parse_args()

if not args.path:
    parser.print_help()
elif os.path.isfile(args.path):
    split_json_file(args.path, args.piece)
elif os.path.isdir(args.path):
    files = os.listdir(args.path)
    for file in files:
        split_json_file(os.path.join(args.path, file), args.piece)
else:
    parser.print_help()