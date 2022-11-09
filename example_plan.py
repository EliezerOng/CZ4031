var = {'Plan': {'Node Type': 'Sort', 'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 64299.06,
                'Total Cost': 64299.07, 'Plan Rows': 1, 'Plan Width': 36, 'Actual Startup Time': 75.565,
                'Actual Total Time': 98.617, 'Actual Rows': 0, 'Actual Loops': 1,
                'Output': ['partsupp.ps_partkey', '(sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric)))'],
                'Sort Key': ['(sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric))) DESC'],
                'Sort Method': 'quicksort', 'Sort Space Used': 25, 'Sort Space Type': 'Memory', 'Plans': [
        {'Node Type': 'Aggregate', 'Strategy': 'Plain', 'Partial Mode': 'Finalize', 'Parent Relationship': 'InitPlan',
         'Subplan Name': 'InitPlan 1 (returns $3)', 'Parallel Aware': False, 'Async Capable': False,
         'Startup Cost': 41504.36, 'Total Cost': 41504.37, 'Plan Rows': 1, 'Plan Width': 32, 'Actual Startup Time': 0.0,
         'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0,
         'Output': ['(sum((partsupp_1.ps_supplycost * (partsupp_1.ps_availqty)::numeric)) * 0.0001000000)'], 'Plans': [
            {'Node Type': 'Gather', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False,
             'Startup Cost': 41504.14, 'Total Cost': 41504.35, 'Plan Rows': 2, 'Plan Width': 32,
             'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0,
             'Output': ['(PARTIAL sum((partsupp_1.ps_supplycost * (partsupp_1.ps_availqty)::numeric)))'],
             'Workers Planned': 2, 'Workers Launched': 0, 'Single Copy': False, 'Plans': [
                {'Node Type': 'Aggregate', 'Strategy': 'Plain', 'Partial Mode': 'Partial',
                 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False,
                 'Startup Cost': 40504.14, 'Total Cost': 40504.15, 'Plan Rows': 1, 'Plan Width': 32,
                 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0,
                 'Output': ['PARTIAL sum((partsupp_1.ps_supplycost * (partsupp_1.ps_availqty)::numeric))'], 'Plans': [
                    {'Node Type': 'Nested Loop', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                     'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 0.45, 'Total Cost': 40489.43,
                     'Plan Rows': 1961, 'Plan Width': 10, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0,
                     'Actual Rows': 0, 'Actual Loops': 0,
                     'Output': ['partsupp_1.ps_supplycost', 'partsupp_1.ps_availqty'], 'Inner Unique': True, 'Plans': [
                        {'Node Type': 'Nested Loop', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                         'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 0.3, 'Total Cost': 32151.69,
                         'Plan Rows': 333333, 'Plan Width': 14, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0,
                         'Actual Rows': 0, 'Actual Loops': 0,
                         'Output': ['partsupp_1.ps_supplycost', 'partsupp_1.ps_availqty', 'supplier_1.s_nationkey'],
                         'Inner Unique': True, 'Plans': [
                            {'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': True,
                             'Async Capable': False, 'Relation Name': 'partsupp', 'Schema': 'public',
                             'Alias': 'partsupp_1', 'Startup Cost': 0.0, 'Total Cost': 20784.33, 'Plan Rows': 333333,
                             'Plan Width': 14, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0,
                             'Actual Loops': 0,
                             'Output': ['partsupp_1.ps_partkey', 'partsupp_1.ps_suppkey', 'partsupp_1.ps_availqty',
                                        'partsupp_1.ps_supplycost', 'partsupp_1.ps_comment']},
                            {'Node Type': 'Memoize', 'Parent Relationship': 'Inner', 'Parallel Aware': False,
                             'Async Capable': False, 'Startup Cost': 0.3, 'Total Cost': 0.31, 'Plan Rows': 1,
                             'Plan Width': 8, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0,
                             'Actual Loops': 0, 'Output': ['supplier_1.s_suppkey', 'supplier_1.s_nationkey'],
                             'Cache Key': 'partsupp_1.ps_suppkey', 'Cache Mode': 'logical', 'Plans': [
                                {'Node Type': 'Index Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                                 'Async Capable': False, 'Scan Direction': 'Forward', 'Index Name': 'supplier_pkey',
                                 'Relation Name': 'supplier', 'Schema': 'public', 'Alias': 'supplier_1',
                                 'Startup Cost': 0.29, 'Total Cost': 0.3, 'Plan Rows': 1, 'Plan Width': 8,
                                 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0,
                                 'Actual Loops': 0, 'Output': ['supplier_1.s_suppkey', 'supplier_1.s_nationkey'],
                                 'Index Cond': '(supplier_1.s_suppkey = partsupp_1.ps_suppkey)',
                                 'Rows Removed by Index Recheck': 0}]}]},
                        {'Node Type': 'Memoize', 'Parent Relationship': 'Inner', 'Parallel Aware': False,
                         'Async Capable': False, 'Startup Cost': 0.15, 'Total Cost': 0.18, 'Plan Rows': 1,
                         'Plan Width': 4, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0,
                         'Actual Loops': 0, 'Output': ['nation_1.n_nationkey'], 'Cache Key': 'supplier_1.s_nationkey',
                         'Cache Mode': 'logical', 'Plans': [
                            {'Node Type': 'Index Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                             'Async Capable': False, 'Scan Direction': 'Forward', 'Index Name': 'nation_pkey',
                             'Relation Name': 'nation', 'Schema': 'public', 'Alias': 'nation_1', 'Startup Cost': 0.14,
                             'Total Cost': 0.17, 'Plan Rows': 1, 'Plan Width': 4, 'Actual Startup Time': 0.0,
                             'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0,
                             'Output': ['nation_1.n_nationkey'],
                             'Index Cond': '(nation_1.n_nationkey = supplier_1.s_nationkey)',
                             'Rows Removed by Index Recheck': 0, 'Filter': "(nation_1.n_name = 'GERMANY'::bpchar)",
                             'Rows Removed by Filter': 0}]}]}]}]}]},
        {'Node Type': 'Aggregate', 'Strategy': 'Sorted', 'Partial Mode': 'Simple', 'Parent Relationship': 'Outer',
         'Parallel Aware': False, 'Async Capable': False, 'Startup Cost': 22794.65, 'Total Cost': 22794.68,
         'Plan Rows': 1, 'Plan Width': 36, 'Actual Startup Time': 75.545, 'Actual Total Time': 98.596, 'Actual Rows': 0,
         'Actual Loops': 1,
         'Output': ['partsupp.ps_partkey', 'sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric))'],
         'Group Key': ['partsupp.ps_partkey'],
         'Filter': '(sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric)) > $3)',
         'Rows Removed by Filter': 0, 'Plans': [
            {'Node Type': 'Sort', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False,
             'Startup Cost': 22794.65, 'Total Cost': 22794.65, 'Plan Rows': 1, 'Plan Width': 14,
             'Actual Startup Time': 75.543, 'Actual Total Time': 98.594, 'Actual Rows': 0, 'Actual Loops': 1,
             'Output': ['partsupp.ps_partkey', 'partsupp.ps_supplycost', 'partsupp.ps_availqty'],
             'Sort Key': ['partsupp.ps_partkey'], 'Sort Method': 'quicksort', 'Sort Space Used': 25,
             'Sort Space Type': 'Memory', 'Plans': [
                {'Node Type': 'Gather', 'Parent Relationship': 'Outer', 'Parallel Aware': False, 'Async Capable': False,
                 'Startup Cost': 1000.44, 'Total Cost': 22794.64, 'Plan Rows': 1, 'Plan Width': 14,
                 'Actual Startup Time': 75.533, 'Actual Total Time': 98.584, 'Actual Rows': 0, 'Actual Loops': 1,
                 'Output': ['partsupp.ps_partkey', 'partsupp.ps_supplycost', 'partsupp.ps_availqty'],
                 'Workers Planned': 2, 'Workers Launched': 2, 'Single Copy': False, 'Plans': [
                    {'Node Type': 'Nested Loop', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                     'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 0.44, 'Total Cost': 21794.54,
                     'Plan Rows': 1, 'Plan Width': 14, 'Actual Startup Time': 55.967, 'Actual Total Time': 55.968,
                     'Actual Rows': 0, 'Actual Loops': 3,
                     'Output': ['partsupp.ps_partkey', 'partsupp.ps_supplycost', 'partsupp.ps_availqty'],
                     'Inner Unique': True, 'Workers': [
                        {'Worker Number': 0, 'Actual Startup Time': 43.753, 'Actual Total Time': 43.754,
                         'Actual Rows': 0, 'Actual Loops': 1},
                        {'Worker Number': 1, 'Actual Startup Time': 49.401, 'Actual Total Time': 49.402,
                         'Actual Rows': 0, 'Actual Loops': 1}], 'Plans': [
                        {'Node Type': 'Nested Loop', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                         'Async Capable': False, 'Join Type': 'Inner', 'Startup Cost': 0.29, 'Total Cost': 21789.43,
                         'Plan Rows': 33, 'Plan Width': 18, 'Actual Startup Time': 55.966, 'Actual Total Time': 55.967,
                         'Actual Rows': 0, 'Actual Loops': 3,
                         'Output': ['partsupp.ps_partkey', 'partsupp.ps_supplycost', 'partsupp.ps_availqty',
                                    'supplier.s_nationkey'], 'Inner Unique': True, 'Workers': [
                            {'Worker Number': 0, 'Actual Startup Time': 43.752, 'Actual Total Time': 43.753,
                             'Actual Rows': 0, 'Actual Loops': 1},
                            {'Worker Number': 1, 'Actual Startup Time': 49.4, 'Actual Total Time': 49.401,
                             'Actual Rows': 0, 'Actual Loops': 1}], 'Plans': [
                            {'Node Type': 'Seq Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': True,
                             'Async Capable': False, 'Relation Name': 'partsupp', 'Schema': 'public',
                             'Alias': 'partsupp', 'Startup Cost': 0.0, 'Total Cost': 21617.67, 'Plan Rows': 33,
                             'Plan Width': 18, 'Actual Startup Time': 55.965, 'Actual Total Time': 55.965,
                             'Actual Rows': 0, 'Actual Loops': 3,
                             'Output': ['partsupp.ps_partkey', 'partsupp.ps_suppkey', 'partsupp.ps_availqty',
                                        'partsupp.ps_supplycost', 'partsupp.ps_comment'],
                             'Filter': "(partsupp.ps_supplycost > '10000'::numeric)", 'Rows Removed by Filter': 266667,
                             'Workers': [
                                 {'Worker Number': 0, 'Actual Startup Time': 43.751, 'Actual Total Time': 43.752,
                                  'Actual Rows': 0, 'Actual Loops': 1},
                                 {'Worker Number': 1, 'Actual Startup Time': 49.399, 'Actual Total Time': 49.399,
                                  'Actual Rows': 0, 'Actual Loops': 1}]},
                            {'Node Type': 'Index Scan', 'Parent Relationship': 'Inner', 'Parallel Aware': False,
                             'Async Capable': False, 'Scan Direction': 'Forward', 'Index Name': 'supplier_pkey',
                             'Relation Name': 'supplier', 'Schema': 'public', 'Alias': 'supplier', 'Startup Cost': 0.29,
                             'Total Cost': 5.21, 'Plan Rows': 1, 'Plan Width': 8, 'Actual Startup Time': 0.0,
                             'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0,
                             'Output': ['supplier.s_suppkey', 'supplier.s_name', 'supplier.s_address',
                                        'supplier.s_nationkey', 'supplier.s_phone', 'supplier.s_acctbal',
                                        'supplier.s_comment'],
                             'Index Cond': '(supplier.s_suppkey = partsupp.ps_suppkey)',
                             'Rows Removed by Index Recheck': 0, 'Filter': "(supplier.s_acctbal < '10000'::numeric)",
                             'Rows Removed by Filter': 0, 'Workers': []}]},
                        {'Node Type': 'Memoize', 'Parent Relationship': 'Inner', 'Parallel Aware': False,
                         'Async Capable': False, 'Startup Cost': 0.15, 'Total Cost': 0.18, 'Plan Rows': 1,
                         'Plan Width': 4, 'Actual Startup Time': 0.0, 'Actual Total Time': 0.0, 'Actual Rows': 0,
                         'Actual Loops': 0, 'Output': ['nation.n_nationkey'], 'Cache Key': 'supplier.s_nationkey',
                         'Cache Mode': 'logical', 'Workers': [], 'Plans': [
                            {'Node Type': 'Index Scan', 'Parent Relationship': 'Outer', 'Parallel Aware': False,
                             'Async Capable': False, 'Scan Direction': 'Forward', 'Index Name': 'nation_pkey',
                             'Relation Name': 'nation', 'Schema': 'public', 'Alias': 'nation', 'Startup Cost': 0.14,
                             'Total Cost': 0.17, 'Plan Rows': 1, 'Plan Width': 4, 'Actual Startup Time': 0.0,
                             'Actual Total Time': 0.0, 'Actual Rows': 0, 'Actual Loops': 0,
                             'Output': ['nation.n_nationkey'],
                             'Index Cond': '(nation.n_nationkey = supplier.s_nationkey)',
                             'Rows Removed by Index Recheck': 0, 'Filter': "(nation.n_name = 'GERMANY'::bpchar)",
                             'Rows Removed by Filter': 0, 'Workers': []}]}]}]}]}]}]},
       'Settings': {'enable_bitmapscan': 'off', 'enable_gathermerge': 'off', 'enable_hashjoin': 'off'},
       'Planning Time': 1.798, 'Triggers': [], 'Execution Time': 98.88}

var = [('Sort  (cost=46225.42..46225.42 rows=1 width=36) (actual time=71.699..98.168 rows=0 loops=1)',),
       ('  Output: partsupp.ps_partkey, (sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric)))',),
       ('  Sort Key: (sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric))) DESC',),
       ('  Sort Method: quicksort  Memory: 25kB',), ('  InitPlan 1 (returns $1)',),
       ('    ->  Finalize Aggregate  (cost=23430.72..23430.73 rows=1 width=32) (never executed)',),
       ('          Output: (sum((partsupp_1.ps_supplycost * (partsupp_1.ps_availqty)::numeric)) * 0.0001000000)',),
       ('          ->  Gather  (cost=23430.49..23430.70 rows=2 width=32) (never executed)',),
       ('                Output: (PARTIAL sum((partsupp_1.ps_supplycost * (partsupp_1.ps_availqty)::numeric)))',),
       ('                Workers Planned: 2',), ('                Workers Launched: 0',),
       ('                ->  Partial Aggregate  (cost=22430.49..22430.50 rows=1 width=32) (never executed)',),
       ('                      Output: PARTIAL sum((partsupp_1.ps_supplycost * (partsupp_1.ps_availqty)::numeric))',),
       ('                      ->  Hash Join  (cost=361.78..22415.78 rows=1961 width=10) (never executed)',),
       ('                            Output: partsupp_1.ps_supplycost, partsupp_1.ps_availqty',),
       ('                            Hash Cond: (partsupp_1.ps_suppkey = supplier_1.s_suppkey)',), (
       '                            ->  Parallel Seq Scan on public.partsupp partsupp_1  (cost=0.00..20784.33 rows=333333 width=14) (never executed)',),
       (
       '                                  Output: partsupp_1.ps_partkey, partsupp_1.ps_suppkey, partsupp_1.ps_availqty, partsupp_1.ps_supplycost, partsupp_1.ps_comment',),
       ('                            ->  Hash  (cost=361.04..361.04 rows=59 width=4) (never executed)',),
       ('                                  Output: supplier_1.s_suppkey',),
       ('                                  ->  Hash Join  (cost=12.14..361.04 rows=59 width=4) (never executed)',),
       ('                                        Output: supplier_1.s_suppkey',),
       ('                                        Inner Unique: true',),
       ('                                        Hash Cond: (supplier_1.s_nationkey = nation_1.n_nationkey)',), (
       '                                        ->  Seq Scan on public.supplier supplier_1  (cost=0.00..322.00 rows=10000 width=8) (never executed)',),
       (
       '                                              Output: supplier_1.s_suppkey, supplier_1.s_name, supplier_1.s_address, supplier_1.s_nationkey, supplier_1.s_phone, supplier_1.s_acctbal, supplier_1.s_comment',),
       ('                                        ->  Hash  (cost=12.13..12.13 rows=1 width=4) (never executed)',),
       ('                                              Output: nation_1.n_nationkey',), (
       '                                              ->  Seq Scan on public.nation nation_1  (cost=0.00..12.13 rows=1 width=4) (never executed)',),
       ('                                                    Output: nation_1.n_nationkey',),
       ("                                                    Filter: (nation_1.n_name = 'GERMANY'::bpchar)",),
       ('  ->  GroupAggregate  (cost=22794.65..22794.68 rows=1 width=36) (actual time=71.695..98.160 rows=0 loops=1)',),
       ('        Output: partsupp.ps_partkey, sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric))',),
       ('        Group Key: partsupp.ps_partkey',),
       ('        Filter: (sum((partsupp.ps_supplycost * (partsupp.ps_availqty)::numeric)) > $1)',),
       ('        ->  Sort  (cost=22794.65..22794.65 rows=1 width=14) (actual time=71.694..98.159 rows=0 loops=1)',),
       ('              Output: partsupp.ps_partkey, partsupp.ps_supplycost, partsupp.ps_availqty',),
       ('              Sort Key: partsupp.ps_partkey',), ('              Sort Method: quicksort  Memory: 25kB',), (
       '              ->  Gather  (cost=1000.44..22794.64 rows=1 width=14) (actual time=71.690..98.154 rows=0 loops=1)',),
       ('                    Output: partsupp.ps_partkey, partsupp.ps_supplycost, partsupp.ps_availqty',),
       ('                    Workers Planned: 2',), ('                    Workers Launched: 2',), (
       '                    ->  Nested Loop  (cost=0.44..21794.54 rows=1 width=14) (actual time=51.109..51.110 rows=0 loops=3)',),
       ('                          Output: partsupp.ps_partkey, partsupp.ps_supplycost, partsupp.ps_availqty',),
       ('                          Inner Unique: true',),
       ('                          Worker 0:  actual time=43.530..43.532 rows=0 loops=1',),
       ('                          Worker 1:  actual time=38.780..38.781 rows=0 loops=1',), (
       '                          ->  Nested Loop  (cost=0.29..21789.43 rows=33 width=18) (actual time=51.108..51.109 rows=0 loops=3)',),
       (
       '                                Output: partsupp.ps_partkey, partsupp.ps_supplycost, partsupp.ps_availqty, supplier.s_nationkey',),
       ('                                Inner Unique: true',),
       ('                                Worker 0:  actual time=43.530..43.530 rows=0 loops=1',),
       ('                                Worker 1:  actual time=38.779..38.780 rows=0 loops=1',), (
       '                                ->  Parallel Seq Scan on public.partsupp  (cost=0.00..21617.67 rows=33 width=18) (actual time=51.108..51.108 rows=0 loops=3)',),
       (
       '                                      Output: partsupp.ps_partkey, partsupp.ps_suppkey, partsupp.ps_availqty, partsupp.ps_supplycost, partsupp.ps_comment',),
       ("                                      Filter: (partsupp.ps_supplycost > '10000'::numeric)",),
       ('                                      Rows Removed by Filter: 266667',),
       ('                                      Worker 0:  actual time=43.529..43.529 rows=0 loops=1',),
       ('                                      Worker 1:  actual time=38.779..38.779 rows=0 loops=1',), (
       '                                ->  Index Scan using supplier_pkey on public.supplier  (cost=0.29..5.21 rows=1 width=8) (never executed)',),
       (
       '                                      Output: supplier.s_suppkey, supplier.s_name, supplier.s_address, supplier.s_nationkey, supplier.s_phone, supplier.s_acctbal, supplier.s_comment',),
       ('                                      Index Cond: (supplier.s_suppkey = partsupp.ps_suppkey)',),
       ("                                      Filter: (supplier.s_acctbal < '10000'::numeric)",),
       ('                          ->  Memoize  (cost=0.15..0.18 rows=1 width=4) (never executed)',),
       ('                                Output: nation.n_nationkey',),
       ('                                Cache Key: supplier.s_nationkey',),
       ('                                Cache Mode: logical',), (
       '                                ->  Index Scan using nation_pkey on public.nation  (cost=0.14..0.17 rows=1 width=4) (never executed)',),
       ('                                      Output: nation.n_nationkey',),
       ('                                      Index Cond: (nation.n_nationkey = supplier.s_nationkey)',),
       ("                                      Filter: (nation.n_name = 'GERMANY'::bpchar)",),
       ('Planning Time: 0.457 ms',), ('Execution Time: 98.234 ms',)]