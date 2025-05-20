from lhc.entities import Locus, Interval

def parse_gff(line: str, index=1) -> Locus:
    parts = line.rstrip('\r\n').split('\t')
    if len(parts) <= 8:
        print(parts)
    attributes = parse_attributes(parts[8])
    attributes['source'] = parts[1]
    attributes['feature'] = parts[2]
    attributes['score'] = parts[5]
    attributes['frame'] = parts[7]
    return Locus(
        chromosome=parts[0],
        interval=Interval(int(parts[3]) - index, int(parts[4])),
        strand=parts[6],
        data=attributes,
    )
    
def parse_attributes(line):
    attributes = {}
    for part in line.split(';'):
        if part:
            key, value = part.split('=', 1) if '=' in part else part
            if ',' in value:
                value = value.split(',')
            attributes[key] = value
    return attributes
