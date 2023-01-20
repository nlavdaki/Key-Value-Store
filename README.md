


Programming Assignment

In this project we will be creating a simple version of a distributed, fault-tolerant, Key-Value (KV)
database (or store), with a few tweaks. A key–value database, or key–value store, is a data storage paradigm designed for storing, retrieving, and managing associative arrays, and a data structure more commonly known today as a dictionary or hash table. Dictionaries contain a collection of objects, or records, which in turn have many different fields within them, each containing data. These records are stored and retrieved using a key that uniquely identifies the record, and is used to find the data within the database. In our case, we will be using a Trie instead of a hash table for storing all the
keys.


1. Data Creation 
Our KV store will be able to index data of arbitrary length and arbitrary nesting of the form:
key -> value
In this case, key represents the key of the data that we care to store and value is the payload (or
value) of the data that we want to store for that key. The value can also contain a set of additional
key -> value pairs. Here is an example of some data that we are interested in storing in our KV
store:
“person1” -> [ “name” -> “John” | “age” -> 22 ]
“person2” -> [ “name” -> “Mary” | “address” -> [ “street” -> “Panepistimiou” |“number” : 12 ] ]
“person3” -> [ “height” -> 1.75 | “profession” -> “student” ]
“person4” -> []
As you can see, the payload (or value) is also a set of key-value pairs and can be nested. For example,
person2 above, has another set of key values as the values of its subkey address. person4 has an
empty value. We only allow records of the form above, i.e. we either have an empty value or a value
with key-value pairs. For example the following data is incorrect:
“person5” -> “hello” <-- wrong value is not key->value or []
“person6” -> [ “address” -> [ “there” ]] <-- wrong, value inside address is not key:value or []
For each value, we can store either an empty Integer (e.g. 12), a Float (e.g. 12.5), a String (e.g.
“hello”, a set of Key Value pairs (e.g. [ “key1” -> 5 | “key2” -> “five” ], or an empty set of
KV value pairs (i.e., []). Each key is of type String only.
Your first task will be to write a program that generates syntactically correct data that will be loaded to
your key value store. Your program should operate as follows:

genData -k keyFile.txt -n 1000 -d 3 -l 4 -m 5

where
-n indicates the number of lines (i.e. separate data) that we would like to generate (e.g. 1000)
-d is the maximum level of nesting (i.e. how many times in a line a value can have a set of key ->
values). Zero means no nesting, i.e. there is only one set of key-values per line (in the value of the
high level key)
-m is the maximum number of keys inside each value.
-l is the maximum length of a string value whenever you need to generate a string. For example 4
means that we can generate Strings of up to length 4 (e.g. “ab”, “abcd”, “a”). We should not generate
empty strings (i.e. “” is not correct). Strings can be only letters (upper and lowercase) and numbers. No
symbols.
-k keyFile.txt is a file containing a space-separated list of key names and their data types that we
can potentially use for creating data. For 

The goal of the program is to randomly generate as much data as was specified by the -n parameter, up
to the given length (-l) of strings, up to (-m) keys per nesting level and up to the given nesting level
(-d). Do not worry if the data does not make sense (e.g. age contains an address). This task is meant for
you to create datasets that you can use to develop the remainder of the project. You can use random
key names and types for the keyFile.txt if you like and you can create your own keyFile.txt. For only
the top-level keys you can either generate random strings or you can generate keys of the form key1,
key2, key3, etc. for easier debugging.


2. Key Value Store 
This part consists of two programs, a Key-Value client that will be accepting queries and will be
redirecting requests to the Key-Value servers, collecting the results and presenting them to the user
and a KV Server that will be storing the actual data and will be handling the queries coming from the
client. We describe each of these modules next.
2-a ) KV Client (20%)
The client should start with the following command:

kvClient -s serverFile.txt -i dataToIndex.txt -k 2

The serverFile.txt is a space separated list of server IPs and their respective ports that will be
listening for queries and indexing commands. 


The dataToIndex.txt is a file containing data that was output from the previous part of the project
that was generating the data.
The k value is the replication factor, i.e. how many different servers will have the same replicated
data.

Once the kvClient starts, it connects to all the servers, and for each line dataToIndex.txt it
randomly picks k servers where it sends a request of the form PUT data. For example, for the first line
above in the first part of the project it will send the following command to each one of the k servers
(there needs to be a white space after PUT, but all other whitespace is flexible):
PUT “person1” -> [ “name” -> “John” | “age” -> 22 ]
Each of the servers now stores (in-memory) the data that was sent over the socket. If everything was
successful it should respond to the client with OK or ERROR if there was a problem.
Once the indexing process has completed, the client now expects from the keyboard one of the
following commands:
a) GET key
In this case, the data with the given high-level key (i.e., you won’t be searching inside any value) is
queried across all servers and if the results are found it is printed on the screen. For example:
GET person1
Should query all three servers of the example above and print:
person1 -> [ name -> John | age -> 22 ]
GET name
Should return NOT FOUND as name is not a high-level key.
You are free to handle quotes “” as you like. Specifically, the following input and output is also
correct, but please specify how you handle this (as well as any other assumptions you make) in your
README:
GET “person1”
“person1” -> [ “name” -> “John” | “age” -> 22 ]
Since we implemented k-replication, the client should continue to work unless k servers are down. For
example, for k=2 if we had 3 servers running and one is down (i.e., 2 left) the server can still compute
correct results. If >= 2 servers are down the client should output a warning indicating that k or more
servers are down and therefore it cannot guarantee the correct output.
b) DELETE key
This command deletes the specified high-level key (i.e., you don’t need to search within each value).
This command needs to be forwarded to all servers. If there is even one server down, delete cannot be
reliably executed and thus there should be a message indicating that delete cannot happen.
c) QUERY keypath
This command is similar to GET above but is meant to return the value of a subkey in the value part of
the high level path. For example, for the data
“person2” -> [ “name” -> “Mary” | “address” -> [ “street” -> “Panepistimiou” | “number”-> 12 ]]
QUERY person2
should return (i.e. the same as GET)
person2 -> [ name -> Mary | address -> [ street -> Panepistimiou | number -> 12 ] ]
QUERY person2.name
should return
person2.name -> Mary
QUERY person2.address.number
should return
person2.address.number -> 12
Both GET and QUERY should specify that the key was not found if a query with a non-existent key was
asked. QUERY works in an identical way to GET as far as replication (i.e., number of available servers)
is concerned.
d) COMPUTE f(x) WHERE x = QUERY key1.key2…
In this case you need to compute a formula with values coming from a query to the KV store. Here is an
example COMPUTE:
COMPUTE 2*x WHERE x = QUERY person2.address.number
In this case, x should be equal to 12 and therefore the answer should be 24, which is what should be
printed in the output:
24
For this question you should be able to compute simple formulas of at most 2 literals where only one
can be a query. You should implement basic arithmetic functions of addition, subtraction, division,
multiplication and power. Here are some examples:
COMPUTE 2-x WHERE x = QUERY person2.address.number // -10
COMPUTE x+x WHERE x = QUERY person2.address.number // 24
COMPUTE x/2 WHERE x = QUERY person2.address.number // 6
COMPUTE 2^x WHERE x = QUERY person2.address.number // 4096

2-b ) KV Server 

The KV Server will be starting at a specific IP and port and will be serving queries coming from the KV
client. The KV Server should start as follows:
kvServer -a ip_address -p port
The server starts at the specified IP address and port (which should be one from the server file that the
client is accepting as input) and is waiting for queries. Once the query is received (as described in the
client section above), the server parses the query. If the query is incorrect (e.g. missing }) the server
returns ERROR to the client together with a message describing the error. If the query is correct, the
server looks up its internal data structures and attempts to find the data corresponding to the query. If
the data is found, it is returned. If the data is not found, then NOTFOUND is returned.
In order to search the data internally (in-memory) efficiently the server maintains a data structure
called a trie (see here for more details) where the top-level keys are stored. When a query comes in,
the server uses the trie to identify whether the key exists, and if so, follows the path where the values
are stored. In the case of a QUERY command, the values at the final level are searched linearly (take
care of the nesting though) or using another Trie.
Here is one example of a trie for a set of keywords:
Example: standard trie for the set of strings
S = { bear, bell, bid, bull, buy, sell, stock, stop }
For the key “bear” we would be looking for the data in the leftmost branch of the tree.
2-c ) Advanced Query Functionality (30%)
In this case, you will be extending the COMPUTE operation to allow for more advanced computations.
More specifically, you will be able to handle more variables as well as precedence of the operators and
parentheses. You should also recognize trigonometric (sin, cos, tan) and logarithmic (base 10)
functions.
COMPUTE f(x,y,...) WHERE x = QUERY key1.key2 AND y = QUERY key3 AND …
Here are some examples:
COMPUTE 2*x+3 WHERE x = QUERY person2.address.number // 27
COMPUTE 2*(x+3) WHERE x = QUERY person2.address.number // 30
COMPUTE 2/(x+3*(y+z)) WHERE x = QUERY person2.address.number AND
y = QUERY person1.age AND
z = QUERY person3.height // 19.625
COMPUTE log(2*(x+3)) WHERE x = QUERY person2.address.number // 1.477
COMPUTE cos(x)-tan(2*y+3) WHERE x = QUERY person2.address.number AND
y = QUERY person1.age // -0.09422
