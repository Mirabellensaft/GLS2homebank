#!/usr/bin/env python3
import argparse
import csv

fieldnames_in = [
        'Kontonummer',
        'Buchungstag',
        'Wertstellung',
        'Auftraggeber/Empfänger',
        'Buchungstext',
        'VWZ1',
        'VWZ2',
        'VWZ3',
        'VWZ4',
        'VWZ5',
        'VWZ6',
        'VWZ7',
        'VWZ8',
        'VWZ9',
        'VWZ10',
        'VWZ11',
        'VWZ12',
        'VWZ13',
        'VWZ14',
        'Betrag',
        'Kontostand',
        'Währung'
]
fieldnames_out = [
        'date',
        'payment',  # "Zahlung" in HomeBank
        'info',
        'payee',
        'memo',
        'amount',
        'category',
        'tags'
]

parser = argparse.ArgumentParser(
        description='convert gls cvs file for homebank')
parser.add_argument('gls_csv')
args = parser.parse_args()

in_csv_filename = args.gls_csv
out_csv_filename = in_csv_filename.replace('.csv', '.homebank.csv')

with open(in_csv_filename, 'r', encoding='iso-8859-1') as csvfile, \
         open(out_csv_filename, 'w') as homebank_csvfile:
    reader = csv.DictReader(csvfile, fieldnames=fieldnames_in,
                            delimiter=';', quotechar='"')
    writer = csv.DictWriter(homebank_csvfile, fieldnames=fieldnames_out,
                            delimiter=';', quotechar='"')
    for row in reader:

        date = row['Buchungstag'].replace('.', '-')
        if row['VWZ1'] is not None:
            zweck = [
                row['VWZ1'],
                row['VWZ2'],
                row['VWZ3'],
                row['VWZ4'],
                row['VWZ5'],
                row['VWZ6'],
                row['VWZ7'],
                row['VWZ8'],
                row['VWZ9'],
                row['VWZ10'],
                row['VWZ11'],
                row['VWZ12'],
                row['VWZ13'],
                row['VWZ14']
            ]

            memo = ' '.join(zweck)
            memo = memo.rstrip(' ')

        else:
            memo = ''

        outrow = {
                'date':     date,
                'payment': 0,  # FIXME
                'memo':     memo,
                'payee':    row['Auftraggeber/Empfänger'],
                'amount':   row['Betrag'],
        }
        writer.writerow(outrow)
