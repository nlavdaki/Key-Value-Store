			KV store project
		      ----------------


1. Data creation:
Included with the py generation program named genData.py you will find a file named keyFile.txt 
which contains keys for the values and their according types of the KV database in my deault:

keys keystype
Sk str
Ik int
Fk float
Stk str
Ink int

If you like you can add/change keys as long as you keep the format the same and use keystype the 
same as mine and dont use special characters.

To run the program on cmd you use the command:

python genData.py -k keyFile.txt -n 10 -d 1 -l 10 -m 2      *Note: keep the keyFile.txt on the same 
                                                              folder, else put the path/keyFile.txt

Where keyFile.txt is the one I provide and the parameters are -n: number of high-level-key lines , 
-d: the max depth (nesting), -l: the max length of str data, -m: the max number of keys per value.

When you run and everything goes (hopefully) pleasantly the cmd prints : "The process has Started!"
and when finished :"The process has Finished!".
Then you will have a dataToIndex.txt file with the requested KV database on the same folder as 
the keyFile.txt one.

2.Key Value Store
Included you will find kvServer.py and kvClient.py along with a server_list.txt. The server_list.txt 
is needed so that when you run the server, its IP and port will be stored there for client later to use.
First, run the server on cmd at servers' cd with :

python kvServer.py -a 127.0.0.1 -p 5001                    *Note:you can change -a and -p as you wish

-a is the IP address you want to use and -p is the port. 

When you have opened your servers open your client accordingly with the command:

python kvClient.py -s server_list.txt -i dataToIndex.txt -k 2 

-s server_list.txt is the file I provided you the IPs and ports are stored by line and separeted by space,
-i dataToIndex.txt is the data we have generated from genData.py.
-k is the number of the random servers you want to use for storing your data, chosen from the ones you have 
provided.

The moment you run your client you should see on your client screen the results from storing your data
on the server/s e.g. 'OK! key1 -> {'Sk': {'Sk': 'svmumumjff'}, 'Fk': {'Stk': 'vpllgtgi'}} stored succesfully', applied
as many times (k) as the servers you have chosen for all your data.

On your screen appears: 
Enter command (GET key, DELETE key, QUERY key.subkey, COMPUTE f(x,y,...) WHERE x = QUERY key1.key2 AND y = QUERY key3 AND …):

You Use:
GET keyd where d is the number of the key's value you want to get.
DELETE keyd same as above but in this case you delete the key chosen from all servers
QUERY keyd.subkey1.subkey2 where subkey1.ubkey2 are the nested keys in values, and you get the value of the subkey's path specified
COMPUTE f(x,y,...) WHERE x = QUERY key1.key2 AND y = QUERY key3 AND … where f(x,y..) is a mathematic formula you want to compute using
parameters of your choosing (x,y) here, and on the x = QUERY ...,y= QUERY ... part you define what number values you want your parameters
to get from your data base using the QUERY procces above. NOTE : you must choose nested subkeys with float or integer values.
