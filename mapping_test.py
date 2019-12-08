def map_num(number, range_start, range_end, new_range_start, new_range_end):
    return (number-range_start)/(range_end-range_start) * (new_range_end-new_range_start) + new_range_start

print(map_num(7, 0, 9, 20, 29))