from preprocessing import *
from annotation import *

if __name__ == '__main__':
    query_execution("select * from tpch1g.customer C, tpch1g.orders O where C.c_custkey = O.o_custkey")
