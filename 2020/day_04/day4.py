import re
import unittest

def line_to_passeport(line) :
    passport = dict()
    line = line.replace('\n', ' ')
    for info in line.split(' ') :
        field,value = info.split(':')
        passport[field] = value
    return passport

with open('input.txt','r') as inputfile :
    passports = list(map(line_to_passeport, inputfile.read().split('\n\n')))

with open('example/input.txt','r') as inputfile :
    example = list(map(line_to_passeport, inputfile.read().split('\n\n')))


required_fileds = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'] #, 'cid']
n = len(required_fileds)


def is_valid(passport) :
    res = True
    k = 0
    while res and k < n :
        required_field = required_fileds[k]
        if required_field not in passport :
            res = False
        k += 1
    return res

def r1(passports) :
    res = 0
    for passport in passports :
        if is_valid(passport) :
            res += 1
    return res

print(
    is_valid(example[0]) == True,
    is_valid(example[1]) == False,
    is_valid(example[2]) == True,
    is_valid(example[3]) == False
)

print(r1(passports))



"""
Rules :
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
"""

with open('example/invalid_passports.txt','r') as inputfile :
    invalid_passports = list(map(line_to_passeport, inputfile.read().split('\n\n')))

with open('example/valid_passports.txt','r') as inputfile :
    valid_passports = list(map(line_to_passeport, inputfile.read().split('\n\n')))


def valid_number(value_str:str, mini:int, maxi:int) :
    res = True
    try :
        value = int(value_str)
    except ValueError :
        return False
    if not (mini <= value <= maxi) :
        return False
    return res

valid_ecl_values = "amb blu brn gry grn hzl oth".split(' ')

def is_valid2(passport) :
    res = True

    if not is_valid(passport) :
        return False

    if not valid_number(passport['byr'], 1920, 2002) :
        return False
    
    if not valid_number(passport['iyr'], 2010, 2020) :
        return False
    
    if not valid_number(passport['eyr'], 2020, 2030) :
        return False
    
    hgt = passport['hgt']
    value, unit = hgt[:-2], hgt[-2:]
    if unit == 'cm' :
        if not valid_number(value, 150, 193) :
            return False
    elif unit == 'in' :
        if not valid_number(value, 59, 76) :
            return False
    else :
        return False
    
    if not re.match("^#([0-9a-f]){6}$", passport['hcl']) :
        return False
    
    if passport['ecl'] not in valid_ecl_values :
        return False

    if not re.match("^[0-9]{9}$", passport['pid']) :
        return False
    
    return res


def r2(passports) :
    res = 0
    for passport in passports :
        if is_valid2(passport) :
            res += 1
    return res

print(f"{4 - r2(invalid_passports)} / 4 invalid test passports")
print(f"{r2(valid_passports)} / 4 valid test passports")
print(r2(passports))
