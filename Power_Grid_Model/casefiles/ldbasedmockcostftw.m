
function mpc = ldbasedmockcostftw
mpc.version = '2';
mpc.baseMVA =  100.00;

%% bus data 
mpc.bus = [
1	3	100	0.00	0.00	0.00	1	0.9935453	-1.119907	138.00	1	1.100	0.900	5.22	0.00	0	0
2	2	0	0.00	0.00	0.00	1	0.9912250	-3.927372	69.00	1	1.100	0.900	5.25	0.00	0	0
3	1	110	0.00	0.00	0.00	1	0.9845477	-4.731145	69.00	1	1.100	0.900	5.71	-0.03	0	0
4	2	0	0.00	0.00	0.00	1	0.9787999	-5.745870	69.00	1	1.100	0.900	5.42	-0.01	0	0
5	1	110	0.00	0.00	0.00	1	0.9889847	-2.069792	138.00	1	1.100	0.900	5.28	0.00	0	0
6	2	5	0.00	0.00	0.00	1	0.9889847	-2.069792	138.00	1	1.100	0.900	5.28	0.00	0	0

];

%% generator data 
mpc.gen = [
1	16	0.80	0.80	-0.50	1.0000	2.80	1	60	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0	0	0	0	0.0000	0	0	0	0
2	16	0.80	0.80	-0.50	1.0000	2.80	1	130	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0	0	0	0	0.0000	0	0	0	0
4	16	0.80	0.80	-0.50	1.0000	2.80	1	130	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0	0	0	0	0.0000	0	0	0	0
6	16	0.80	0.80	-0.50	1.0000	2.80	1	5	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0	0	0	0	0.0000	0	0	0	0
];

%% generator cost data
mpc.gencost = [
2	0	0	3	0.0000	0.003	4.570	0.00
2	0	0	3	0.0000	0.002	4.570	0.00
2	0	0	3	0.0000	0.002	4.570	0.00
2	0	0	3	0.0000	0.002	4.570	0.00
];

%% branch data
mpc.branch = [
1	2	0.004840	0.123766	0.00000	123.20	123.20	123.20	0.00000	0.000	1	0.00	0.00	39.02	1.29	-38.95	0.62	0	0	0	0
1	4	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
1	6	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
1	6	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
1	6	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
1	6	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
1	6	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
2	3	0.003400	0.020913	0.00846	232.80	232.80	232.80	0.00000	0.000	1	0.00	0.00	79.42	8.98	-79.20	-8.46	0	0	0	0
4	5	0.003740	0.024173	0.00605	177.80	177.80	177.80	0.00000	0.000	1	0.00	0.00	-20.99	-8.73	21.01	8.25	0	0	0	0
];