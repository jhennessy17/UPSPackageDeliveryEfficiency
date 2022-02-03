# UPSPackageDeliveryEfficiency

A. 

The program uses a form of the nearest neighbor algorithm.  The program finds the nearest address that is associated with the packages on a given truck and moves the truck to that address. Given any package data, the program will self-adjust and decide the best route for the truck based on the closest address to each previous address after beginning at the HUB.

B1.  
•	Comments in the code help to show certain logic that I will further describe here.  
•	The main problem of delivering the packages is solved in the functions deliverPackages and deliverAllPackages.  The deliver packages function concerns with the status of the trucks at a specific time, whereas the deliverAllPackages function is only concerned with the route and distance all trucks will travel by the end of the day.  
•	Both functions take a list of the hash table built to replicate the trucks containing the packages, and a list of the address data read from the provided file.  The functions start the trucks addresses at the Hub and find the nearest package address for the truck to travel after that.
•	The nearest address is calculated by using the address class function getClosestAddress
•	This function will search through the distance data of the given address, and return the closest address and the distance to that address
•	The function cross references the hash table to make sure only distance data for addresses in the specific hash table are checked and accounted for
•	After moving the truck hash to the next closest address the algorithm will remove the package from the hash table.
•	Once removed the delivery status of the package will be updated with the given time of delivery
•	The time is calculated by calculating the amount of hours passed since 8:00AM based on the distance the truck has traveled
•	This is calculated by converting distance to hours and the converting hours to hours and minutes
•	The functions move through each closest address for each package on the truck until the truck/hash table contain no more packages
•	The functions keep track of the total distance traveled for each truck after moving from address to address.  
•	The algorithm is designed to return truck1 back to the Hub when it has five packages remaining in it’s hash.  The reason for this is to satisfy the package requirement for package 6, which states it must be delivered by 10:30, but will not arrive to the station until 9:05.  The specific number of 5 packages left is chosen because truck3 was preloaded with 11 packages and will be able to have 5 packages moved to it to satisfy the 16 package max requirement.  
•	The biggest difference in the two algorithms is that the deliverPackages function will keep track of which trucks are delivering packages at what time.  
•	This is done by calculating the max distance the trucks can travel.  
•	The max distance is calculated by taking a given time entered and finding the amount of time that has passed(in hours) since the departure time of 8:00AM.  This time in hours is then multiplied by 18MPH(The speed of the trucks) to calculate the miles the trucks can travel
•	Both functions print the distance traveled by each truck
•	deliverPacakages will return once the distance that corresponds to the given time entered constraint has been met
•	deliverPacakages will also update the delivery status of each package whether it is en route, at the hub, delivered.  Each status will contain the time which is calculated the same way as described earlier
•	deliverAllPackages will return the total distance traveled by each truck by the end of the day

B2.

The program was written using a Macbook pro 2020 with an M1 chip on Mac OS Big Sur.  The programming language used was python 3.  The IDE used was Pycharm version 2021.1.2 Community Edition

B3.

The space time complexity of the hash table, the package class, and the address class is O(N).  The space time complexity of the entire program is O(N). Big O time complexity of the program and the algorithms for delivering the packages is O(N^2). 

B4.

The hash tables ability to hold any number of packages makes it scalable(even though the specific problem constrains this specific hash table to holding 16 packages).  The algorithms for finding the routes for each truck can be used for any number of packages, however the algorithms are specifically constrained to three trucks.  This could be easily adjusted however.  The number of packages is constrained to the specific loading of the 40 packages, however any further packages loaded could be delivered no problem as long as the packages are manually loaded using the same function.  The functions that load the packages and address data are scalable to any number of packages or address data.  The deliverPackages function adapts to any given time throughout the delivery day.

B5.

The program is efficient because the Big O time complexity of the program is O(N^2).  The code is well documented and the idea behind using the hash table is easy to understand.  It is also efficient to use the addresses in the hash function for the data structure because it will allow packages being delivered to the same address to be treated as one delivery, as it would be done in real life.



B6.

The strengths of the hash table is that it can hold any number of packages and be modeled after any number of trucks, that it has built in functions to keep track of the delivery status of each package including the time, and that it uses the address of each package to quickly access any package and to access packages that are being delivered to the same address.  The weaknesses include the hash tables inability to search packages by the ID(Though the program is built with this in mind, and satisfies the requirement F in a later part),  and the functions that iterate each bucket and each element of each bucket defeat the purpose of having the easy to access buckets of a hash table.

D1

The hash table I built replicates the different trucks.  Each truck has it’s own hash table that corresponds to it and the packages that it holds.  The structure uses the hashed value of the address of each package on the truck.  This allows the hash to associate two packages with the same address as being in the same bucket that way both can be delivered at the same time efficiently, as a real delivery truck would do.  It also allows for a quick and efficient way of checking if an address is a specific hash table.  This is important because each address contains the distances to each address that will be traveled to even though each truck won’t need to go to each address due to packages being spread between the various trucks.

I1

The strengths of the algorithms for calculating the trucks routes are that they will work for any number of packages on the three trucks, and that they deliver the packages using an efficient nearest neighbor fashion.  The weaknesses are that they are constrained to 3 trucks, and that how the packages are loaded will drastically affect the outcome of the algorithm, which is a process that the algorithm has no control over.

I3

Two other algorithms that could have been used in the solution include Dijkstras algorithm and a Floyd Warshall algorithm.

a.	Dijkstras algorithm would have been different because it would have required me to build a graph data structure for the addresses and find the shortest paths by searching through the weights of the nodes in the graph.  The Floyd Warshall algorithm would also require a graph to be built, but would go about finding the shortest path by checking the distances between each pair of nodes instead of checking the shortest distance from one vertex to all other nodes.

J

If I were to do this project again I would find a way to optimize my algorithm to be able to dynamically load packages to the trucks instead of doing it manually.  I would want to build heuristic way for finding an optimal solution for loading the trucks, while still meeting the special instruction requirements for the packages.

K1

The trucks are delivered with a distance of 100.7 miles which is less than the required 140.  All specifications were met in terms of when the packages needed to be delivered, which truck they needed to be on, and when they could be picked up from the HUB.

a.	The lookup function is optimized so that adding more packages will increase the time required to run the function, but separating the packages into the buckets with the hashed value of the address as the key will make searching for packages much faster than a traditional list.
b.	The space time complexity of the hash table is O(n)
c.	Adding trucks would not affect the hash table directly because each truck is modeled as it’s own hash table.  Therefore it would only mean that more packages would be loaded onto a different hash table rather than just the original 3 trucks(hash tables).  Once again, adding more cities won’t directly affect the hash table, but the algorithm used to find the shortest paths for the trucks will use have to use the hash tables isAddressInHash function more due to more addresses being required to be checked.

K2

I could have used a basic dictionary or a list to accommodate the requirements of problem
	
a.	The dictionary would have used a traditional key value pair set up instead of using a hash function to place the packages into different buckets.  The key could have used the itemID in this scenario.  A traditional list could have been used to place the packages in spots where the spot in the list had a relationship to the itemID.  This would have been an efficient way to implement a list in a similar way to the dictionary, however even if the packages were placed in the list at random, a regular search could still replicate a lookup function
