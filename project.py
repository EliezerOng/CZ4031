from preprocessing import *
import annotation as an
import interface

DEFAULT_PARAMS = {

    'enable_async_append': 'ON',
    'enable_bitmapscan': 'ON',
    'enable_gathermerge': 'ON',
    'enable_hashagg': 'ON',
    'enable_hashjoin': 'ON',
    'enable_incremental_sort': 'ON',
    'enable_indexscan': 'ON',
    'enable_indexonlyscan': 'ON',
    'enable_material': 'ON',
    'enable_memoize': 'ON',
    'enable_mergejoin': 'ON',
    'enable_nestloop': 'ON',
    'enable_parallel_append': 'ON',
    'enable_parallel_hash': 'ON',
    'enable_partition_pruning': 'ON',
    'enable_partitionwise_join': 'OFF',
    'enable_partitionwise_aggregate': 'OFF',
    'enable_seqscan': 'ON',
    'enable_sort': 'ON',
    'enable_tidscan': 'ON'

}


if __name__ == '__main__':

   #  print("QEP Costs")
   #  root = get_qep("select * from customer C, orders O where C.c_custkey = O.o_custkey")
   # # root = get_qep(
   #      #"select ps_partkey, sum(ps_supplycost * ps_availqty) as value from tpch1g.partsupp, tpch1g.supplier, tpch1g.nation where ps_suppkey = s_suppkey and s_nationkey = n_nationkey and n_name = 'GERMANY' and ps_supplycost > 2400 and s_acctbal > 25000 group by ps_partkey having sum(ps_supplycost * ps_availqty) > (select sum(ps_supplycost * ps_availqty) * 0.0001000000 from tpch1g.partsupp, tpch1g.supplier, tpch1g.nation where ps_suppkey = s_suppkey and s_nationkey = n_nationkey and n_name = 'Germany') order by value desc")
   #  an.build_annotation(root)
   #  print("Total cost for this plan: " + str(root.total_cost))
   #
   #  print("================================================================")
   #
   #  print("AQP 1")
   #  # DEFAULT_PARAMS['enable_hashjoin'] = 'OFF'
   #  root = get_aqp(DEFAULT_PARAMS,"select * from customer C, orders O where C.c_custkey = O.o_custkey")
   #  an.build_annotation(root)
   #  #print(root.info)
   #  print("Total cost for this plan: " + str(root.total_cost))

    interface.create_main_window()


