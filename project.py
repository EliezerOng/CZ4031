from preprocessing import *
import annotation as an

if __name__ == '__main__':
    root = get_qep("select * from tpch1g.customer C, tpch1g.orders O where C.c_custkey = O.o_custkey")
    an.build_annotation(root)
