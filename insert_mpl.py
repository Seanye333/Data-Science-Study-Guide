import json

path = r'C:/Users/seany/Documents/All Codes/Data Science Study Path/gen_matplotlib.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

marker = ']  # end SECTIONS'
idx = content.index(marker)

def format_section(sec):
    tqs = '"""'
    parts = []
    parts.append('    {')
    parts.append('        ' + '"title": ' + json.dumps(sec['title']) + ',')
    parts.append('        "examples": [')
    for ex in sec['examples']:
        parts.append('            {')
        parts.append('                ' + '"label": ' + json.dumps(ex['label']) + ',')
        parts.append('                ' + '"code": ' + tqs + ex['code'] + tqs)
        parts.append('            },')
    parts.append('        ],')
    parts.append('        ' + '"rw_scenario": ' + json.dumps(sec['rw_scenario']) + ',')
    parts.append('        ' + '"rw_code": ' + tqs + sec['rw_code'] + tqs + ',')
    parts.append('        ' + '"practice": ' + json.dumps(sec['practice']))
    parts.append('    },')
    return '\n'.join(parts) + '\n'

print(format_section({'title': 'Test', 'examples': [{ 'label': 'l', 'code': 'c' }], 'rw_scenario': 's', 'rw_code': 'r', 'practice': 'p'}))
