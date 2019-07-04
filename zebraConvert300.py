"""
    zebraConvert300 scans text file and searches for zebra printing language codes and scales the code values
    representing dot values from a 203 dpi resolution to 300 dpi
    AE: 2019-07-02
"""

zebra_dict = {
    "FO": 2,
    "PW": -1,
    "FT": 2,
    "A0": -1,
    "A@": -1,
    "LL": -1,
    "LH": -1,
    "GB": -1,
    "FB": -1,
    "BY": 1,
    "B3": -1,
    "BC": -1,
    "B7": 2,
}


def scale_zpl(value):
    return round(int(value) * 300.0 / 203)


def scale_code(code, value_string):
    #print(code, value_string)
    values = value_string.split(',')
    scaled_code = code
    for idx, value in enumerate(values):
        if value.isdigit() and (zebra_dict[code] == -1 or idx < zebra_dict[code]):
            #print(idx, ": ", value, " -> ", scale_zpl(value))
            scaled_code += str(scale_zpl(value))
        else:
            scaled_code += value

        if idx < len(values) - 1:
            scaled_code += ","

    return scaled_code


def analyze_code(code):
    if code[:2] in zebra_dict.keys():
        return scale_code(code[:2], code[2:])
    else:
        return code


def search_zebra_codes(fragments):
    # print(len(fragments) , ": " , fragments[1])
    for idx, fragment in enumerate(fragments):
        zebra_code = fragment.split('^')
        if len(zebra_code) > 1:
            for idy, val in enumerate(zebra_code):
                if idy > 0 and len(val) > 0:
                    zebra_code[idy]=analyze_code(val)
        fragments[idx]='^'.join(zebra_code)

    return fragments


with open("DeliveryInfoPrintZebra.java") as in_file:
    with open("DeliveryInfoPrintZebra300.java",'w') as out_file:
        for line in in_file:
            fragments = line.split('"')
            if len(fragments) > 1:
                out_file.write('"'.join(search_zebra_codes(fragments)))
            else:
                out_file.write(line)