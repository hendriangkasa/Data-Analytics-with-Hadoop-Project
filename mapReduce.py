from mrjob.job import MRJob
from mrjob.step import MRStep

import csv
import json

cols = 'order_id,order_date,user_id,payment_name,shipper_name,order_price,order_discount,voucher_name,voucher_price,order_total,rating_status'.split(',')

def csv_readline(line):
    for row in csv.reader([line]):
        return row

class OrderDateCount(MRJob):
    def steps(self):
        return [ 
            MRStep(mapper=self.mapper, reducer=self.reducer),
            MRStep(reducer=self.sort)
        ]

    def mapper(self, _, line):
        row = dict(zip(cols, csv_readline(line)))

        if row['order_id'] != 'order_id':
            yield row['order_date'][0:7], 1

    def reducer(self, key, values):
        yield None, (key, sum(values))

    def sort(self, key, values):
        data = []
        for order_date, order_count in values:
            data.append((order_date, order_count))
            data.sort()
        
        for order_date, order_count in data:
            yield order_date, order_count

if __name__ == '__main__':
    OrderDateCount.run()