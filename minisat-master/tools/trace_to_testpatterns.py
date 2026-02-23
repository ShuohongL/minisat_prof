# python
import os
import re
import argparse
from math import ceil

def parse_line_for_op_and_key(line, data_width=5, activity_width=16):
    l = line.lower()
    # Extract first integer (vid) if present
    m = re.search(r'(-?\d+)', line)
    if m:
        key = int(m.group(1))
    else:
        # no explicit key - use 0 as placeholder for ops like build
        key = 0

    # Extract activity value if present (integer or float)
    act_m = re.search(r'activity\s*[=:]?\s*([0-9]+(?:\.[0-9]+)?)', line, re.IGNORECASE)
    activity = None
    if act_m:
        activity = act_m.group(1)

    # Determine op
    if 'insert' in l:
        op = f"insert_variable({data_width}'d{key});"
        vid = -1
    elif 'update_activity' in l:
        op = f"bump_activity({data_width}'d{key}, $rtoi({activity} * 4096.0));"
        vid = -1
    elif 'remove_max' in l:
        op = f"remove_max;"
        vid = key
    # elif 'rebuild' in l or 'rebuilding' in l:
    #     op = 'build'
    # elif 'check heap' in l:
    #     op = "check_expected_state;"
    #     vid = -1
    else:
        return None

    return op, vid

def process_file(in_path, out_tv, out_pattern,data_width=4, activity_width=8):
    os.makedirs(os.path.dirname(out_tv) or '.', exist_ok=True)
    os.makedirs(os.path.dirname(out_pattern) or '.', exist_ok=True)

    with open(in_path, 'r') as fin, \
            open(out_tv, 'w') as ftv, \
            open(out_pattern, 'w') as fout:
        for ln in fin:
            ln_strip = ln.strip()
            if not ln_strip:
                continue
            parsed = parse_line_for_op_and_key(ln_strip)
            if parsed is None:
                # skip unknown lines
                continue
            op_name, vid = parsed
            ftv.write('{}  // {}  \n'.format(op_name, ln_strip))
            if vid != -1:
                fout.write(f'{vid} ')
            # ftv.write("check_expected_state(); \n")

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Convert heap operation log to Verilog test patterns')
    p.add_argument('--in', dest='infile', default='./output/heap_operations.txt', help='input log file (default: ./output/heap_operations.txt)')
    p.add_argument('--out-tv', dest='out_tv', default='./output/heap_testpatterns.tv', help='output human-readable test vectors')
    p.add_argument('--out-pattern', dest='out_pattern', default='./output/expected_vid_seq.txt', help='output human-readable test vectors')
    p.add_argument('--data-width', dest='data_width', type=int, default=4, help='opcode bit width')
    p.add_argument('--activity-width', dest='activity_width', type=int, default=8, help='key field bit width')
    args = p.parse_args()

    infile = args.infile
    if not os.path.exists(infile):
        print('Input file not found:', infile)
        raise SystemExit(1)

    process_file(infile, args.out_tv, args.out_pattern,args.data_width, args.activity_width)
    print('Wrote', args.out_tv)
