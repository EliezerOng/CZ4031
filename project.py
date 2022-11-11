from preprocessing import *
import annotation as an

if __name__ == '__main__':
    # root = get_qep("select * from tpch1g.customer C, tpch1g.orders O where C.c_custkey = O.o_custkey")
    root = get_qep(
        "select ps_partkey, sum(ps_supplycost * ps_availqty) as value from tpch1g.partsupp, tpch1g.supplier, tpch1g.nation where ps_suppkey = s_suppkey and s_nationkey = n_nationkey and n_name = 'GERMANY' and ps_supplycost > 2400 and s_acctbal > 25000 group by ps_partkey having sum(ps_supplycost * ps_availqty) > (select sum(ps_supplycost * ps_availqty) * 0.0001000000 from tpch1g.partsupp, tpch1g.supplier, tpch1g.nation where ps_suppkey = s_suppkey and s_nationkey = n_nationkey and n_name = 'Germany') order by value desc")
    an.build_annotation(root)
    print(root.info)
