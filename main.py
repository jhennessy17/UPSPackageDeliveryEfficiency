#Jeremiah Hennessy 001501081

import csv

#This hash table will represent each truck and the packages that are held on each truck
class packageHashTable:
    #10 buckets will be used in the hash
    def __init__(self):
        self.table = []
        self.packageNumber = 0
        for i in range(10):
            self.table.append([])

    #insert function will hash the address of the packages
    def insert(self, item):
        bucket = hash(item.address) % len(self.table)
        self.table[bucket].append(item)
        self.packageNumber += 1

    #Requirment F
    #The hash is developed to take in the address as the key for efficiency purposes
    #This lookup function is not necessary for the logic of this program
    #The later lookUp function is used for this purpose but I included this just in case
    def lookUp(self, packageID):
        for i in range(self.table.__len__()):
            for package in self.table[i]:
                if package.id == packageID:
                    return package

    #the address of the package will be used to locate and remove the package
    #the distance the truck has traveled will be used to convert the distance to time for the delivery status
    #of the truck
    def remove(self, address, truckDistance):
        bucket = hash(address) % len(self.table)

        #cast the table to a list so that it won't skip elements upon iterations
        #This loop is intended to deliver multiple packages to the same address simultaneously
        for package in list(self.table[bucket]):
            if package.address.__eq__(address):
                package.deliveryStatus = "Delivered at " + convertTime(truckDistance)
                self.table[bucket].remove(package)
                self.packageNumber -= 1

    #checks if the address passed corresponds to the address of a package
    def isAddressInHash(self, address):
        bucket = hash(address) % len(self.table)

        for package in self.table[bucket]:
            if package.address.__eq__(address):
                return True
        return False

    #returns a list of the packages left on the truck
    def remainingPackages(self):
        packageList = []
        for i in range(10):
            for package in self.table[i]:
                packageList.append(package)
        return packageList

    #sets the delivery status of the truck to be En Route and sets the time using the distance it has traveled
    def setInTransit(self, distance):
        for i in range(10):
            for package in self.table[i]:
                package.deliveryStatus = "En Route " + convertTime(distance)

    #sets the delivery status of the truck to be at the hub and sets the time using the distance the other trucks
    #have traveled
    def setHubTime(self, distance):
        for i in range(10):
            for package in self.table[i]:
                package.deliveryStatus = "At the Hub " + convertTime(distance)

#Class to hold the package data
class package:
    def __init__(self, id, address, city, state, zip, deadline, mass, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.deliveryStatus = 'At the hub'

    def __str__(self):
        return "ID: %s  Address: %s  City: %s  State: %s  Zip: %s  Mass: %sKg  Delivery Status: %s" % (self.id, self.address, self.city,
                                                                    self.state, self.zip, self.mass, self.deliveryStatus)

#Class to hold the address data and distance between the addresses
class address:
    def __init__(self):
        self.table = {}

    #Inserts each address as a key value pair of the address name and the set of distances to the other addresses
    def insertAddress(self, address, distanceSet):
        self.table[address] = distanceSet

    def lookUpAddress(self, address):
        return self.table[address]

    #used to find the closest address to a specified address
    #returns the closest address and the distance to that address
    def getClosestAddress(self, address, truckHash):
        #no distance will be greater than 100 so this is a good spot to start the variable at
        minDistance = 100
        keyList = list(self.table) #holds the names of the addresses
        #Loops through the set of distances
        for i in range(self.table[address].__len__()):
            #Finds the smallest number in the distance set
            if ((float(self.table[address][i]) != 0)) & (float(self.table[address][i]) < minDistance) \
                    & (truckHash.isAddressInHash(keyList[i])):
                minDistance = float(self.table[address][i])
                closestAddress = keyList[i]

        return closestAddress, minDistance

    #returns the distance to the hub
    def distanceToHub(self, address):
        return float(self.table[address][0])

#Loads the packages from the csv file
#Returns a list of the packages
def loadPackages():
    with open('WGUPS Package File.csv') as packageFile:
        packages = csv.reader(packageFile, delimiter=',')

        package_list = []
        for row in packages:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = row[5]
            mass = row[6]
            notes = row[7]
            package_list.append(package(id, address, city, state, zip, deadline, mass, notes))

        return package_list

#Loads the address data from the csv file
#Returns a list containing the address data
def loadAddressData():
    with open('WGUPS Distance Table.csv') as addressFile:
        addressCSV = csv.reader(addressFile, delimiter=',')

        address_list = address()
        iterAddress = iter(addressCSV)
        next(iterAddress)
        for row in iterAddress:
            distanceSet = []
            #only take in the part of the address that will match the package addresses
            addressRow = row[1].splitlines()[0]
            for i in range(2, 29):
                distanceSet.append(row[i])
            address_list.insertAddress(addressRow.lstrip(), distanceSet)
        return address_list

#Manually loads the packages onto each truckHash
def loadTrucks(truck1, truck2, truck3, packages):
    truck1.insert(packages[0])
    truck1.insert(packages[6])
    truck1.insert(packages[7])
    truck1.insert(packages[22])
    truck1.insert(packages[23])
    for package in packages[28:31]:
        truck1.insert(package)
    truck1.insert(packages[32])
    truck1.insert(packages[33])
    truck1.insert(packages[34])
    truck1.insert(packages[36])
    truck1.insert(packages[38])
    truck1.insert(packages[39])
    truck2.insert(packages[2])
    for package in packages[10:22]:
        truck2.insert(package)
    truck2.insert(packages[35])
    truck2.insert(packages[37])
    truck3.insert(packages[1])
    truck3.insert(packages[3])
    truck3.insert(packages[4])
    truck3.insert(packages[5])
    '''This address will not be known until 10:20AM but this package will not be delivered until 10:40AM,
    So to make the code simpler I will change the address here with the knowledge that it meets the requirement for when
    the change in address will be made'''
    packages[8].address = "410 S State St"
    truck3.insert(packages[8])
    truck3.insert(packages[9])
    for package in packages[24:28]:
        truck3.insert(package)
    truck3.insert(packages[31])

#Delivers packages based off of the amount of hours the trucks have been gone from the HUB
#The hours variable will be in decimal format of hours, meaning it will not contain minutes
#The function will print the status of the trucks and then end
def deliverPackages(truckHashList, addressList, hours):
    truck1Address = "HUB"
    truck2Address = "HUB"
    truck3Address = "HUB"
    #The trucks travel 18MPH meaning the amount of hours that they have been departed times 18 will result in
    #the total miles traveled by the truck
    totalDistanceToTravel = hours*18
    driver1Distance = 0
    driver2Distance = 0
    #Deliver packages for truck 1 and 2 until truck 1 has reached 5 packages remaining
    #The five package limit is set to ensure that the driver returns back to the hub to retrieve package 6
    #Which has a delivery deadline of 10:30 but did not arrive to the depot until 9:05 after the trucks left
    while(truckHashList[0].packageNumber > 5):
        # Find the closest address of each truck and the distance to that address
        # Add the distance traveled to the total distance traveled by the truck and update the current address
        # Of the truck
        truck1Address, distance = addressList.getClosestAddress(truck1Address, truckHashList[0])
        driver1Distance += distance
        truck2Address, distance = addressList.getClosestAddress(truck2Address, truckHashList[1])
        driver2Distance += distance
        #Makes sure the trucks still have time left to deliver packages
        if ((driver1Distance < totalDistanceToTravel) & (driver2Distance < totalDistanceToTravel)):
            truckHashList[0].remove(truck1Address, driver1Distance)
            truckHashList[1].remove(truck2Address, driver2Distance)
        else:
            #Prints the status of the trucks at a given moment in time and returns
            truckHashList[0].setInTransit(totalDistanceToTravel)
            truckHashList[1].setInTransit(totalDistanceToTravel)
            truckHashList[2].setHubTime(totalDistanceToTravel)
            print("Total Distance traveled by truck 1 is :" + str(driver1Distance))
            print("Total Distance traveled by truck 2 is :" + str(driver2Distance))
            print("Total Distance traveled by truck 3 is :" + str(0))
            return

    #Return truck1 home with five packages on it and move those packages to truck3 which already contains 11 preloaded
    #packages
    driver1Distance += addressList.distanceToHub(truck1Address)
    truck1Distance = driver1Distance
    packages = truckHashList[0].remainingPackages()
    for package in packages:
        truckHashList[2].insert(package)

    #Continue delivering for truck 2 while truck 1 returns to the HUB
    truck2Address, distance = addressList.getClosestAddress(truck2Address, truckHashList[1])
    driver2Distance += distance

    #Finish delivering packages of truck 2 and 3 simultaneously until truck 2 is finished
    # if returning truck 1 to the hub takes too much time stop delivering or if truck 2's next stop is too far
    if((driver1Distance < totalDistanceToTravel) & (driver2Distance < totalDistanceToTravel)):
        truckHashList[1].remove(truck2Address, driver2Distance)
        while((truckHashList[1].packageNumber > 0) & (truckHashList[2].packageNumber > 0)):
            #Find the closest address of each truck and the distance to that address
            #Add the distance traveled to the total distance traveled by the truck and update the current address
            #Of the truck
            truck3Address, distance = addressList.getClosestAddress(truck3Address, truckHashList[2])
            driver1Distance += distance
            truck2Address, distance = addressList.getClosestAddress(truck2Address, truckHashList[1])
            driver2Distance += distance
            # Makes sure the trucks still have time left to deliver packages
            if ((driver1Distance < totalDistanceToTravel) & (driver2Distance < totalDistanceToTravel)):
                truckHashList[1].remove(truck2Address, driver2Distance)
                truckHashList[2].remove(truck3Address, driver1Distance)
            else:
                #Prints the status of the trucks at a given moment in time and returns
                truckHashList[1].setInTransit(totalDistanceToTravel)
                truckHashList[2].setInTransit(totalDistanceToTravel)
                print("Total Distance traveled by truck 1 is :" + str(truck1Distance))
                print("Total Distance traveled by truck 2 is :" + str(driver2Distance))
                print("Total Distance traveled by truck 3 is :" + str(driver1Distance - truck1Distance))
                return
    else:
        #Prints the status of the trucks at a given moment in time and returns
        print("Total Distance traveled by truck 1 is :" + str(driver1Distance))
        print("Total Distance traveled by truck 2 is :" + str(driver2Distance))
        print("Total Distance traveled by truck 3 is :" + str(0))
        return

    #Finish delivering truck 3 if more distance is to be traveled based on the hours given earlier
    while(truckHashList[2].packageNumber > 0):
        truck3Address, distance = addressList.getClosestAddress(truck3Address, truckHashList[2])
        driver1Distance += distance
        if (driver1Distance < totalDistanceToTravel):
            truckHashList[2].remove(truck3Address, driver1Distance)
        else:
            truckHashList[2].setInTransit(totalDistanceToTravel)
            print("Total Distance traveled by truck 1 is :" + str(truck1Distance))
            print("Total Distance traveled by truck 2 is :" + str(driver2Distance))
            print("Total Distance traveled by truck 3 is :" + str(driver1Distance - truck1Distance))
            return

    #If the hours given were enough to complete the day then print the final distance traveled by each truck
    print("Total Distance traveled by truck 1 is :" + str(truck1Distance))
    print("Total Distance traveled by truck 2 is :" + str(driver2Distance))
    print("Total Distance traveled by truck 3 is :" + str(driver1Distance - truck1Distance))
    return

#Converts the distance the truck has traveled to the time
def convertTime(distance):
    hours = (distance/18) #converts the distance to hours
    minutes = int((hours - int(hours))*60) #converts the decimal of hours to minutes
    #correctly formats minutes if it is less than 10 minutes so that it will display 09 instead of 9 etc.
    if(minutes < 10):
        minutes = ("0" + str(minutes))
    #Adds the amount of hours the trucks have been traveling to 8 since the trucks left at 8:00 AM
    hour = int(hours) + 8
    #Formats the time to correctly show AM and PM values
    if(hours <= 5):
        return(str(hour) + ":" + str(minutes) + "AM")
    else:
        return(str((hour - 12)) + ":" + str(minutes) + "PM")

#Delivers all the packages for the day
#Prints the total distance each truck has traveled and the total distance traveled by each truck
#This function utilizes the same formula as the deliver packages formula but it does not concern time
def deliverAllPackages(truckHashList, addressList):
    truck1Address = "HUB"
    truck2Address = "HUB"
    truck3Address = "HUB"
    driver1Distance = 0
    driver2Distance = 0

    #Same algorithm as the deliverPackages function
    while(truckHashList[0].packageNumber > 5):
        truck1Address, distance = addressList.getClosestAddress(truck1Address, truckHashList[0])
        driver1Distance += distance
        truckHashList[0].remove(truck1Address, driver1Distance)

    while (truckHashList[1].packageNumber != 0):
        truck2Address, distance = addressList.getClosestAddress(truck2Address, truckHashList[1])
        driver2Distance += distance
        truckHashList[1].remove(truck2Address, driver2Distance)

    '''Return truck1 home with five packages on it and move those packages to truck3 which already contains 11 preloaded
    packages'''
    driver1Distance += addressList.distanceToHub(truck1Address)
    truck1Distance = driver1Distance
    print("Total Distance traveled by truck 1 is :" + str(truck1Distance))
    print("Total Distance traveled by truck 2 is :" + str(driver2Distance))
    packages = truckHashList[0].remainingPackages()
    for package in packages:
        truckHashList[2].insert(package)

    while (truckHashList[2].packageNumber != 0):
        truck3Address, distance = addressList.getClosestAddress(truck3Address, truckHashList[2])
        driver1Distance += distance
        truckHashList[2].remove(truck3Address, driver1Distance)

    print("Total Distance traveled by truck 3 is :" + str(driver1Distance - truck1Distance))

    return(driver1Distance + driver2Distance)

#Shows the data for each package
def showAllPackages(packages):
    for package in packages:
        print(package)

#Look up function for a specific package in the set of data
#Uses packageID and finds the package
#Satisfies requirement F
def lookUpPackage(packages, packageID):
    #The package ID will always be 1 more than the packages spot in the package list
    return packages[(packageID - 1)]

#Finds the amount of hours the trucks have been delivering based on a given time after 8:00AM
#Will only accept UTC times
def hoursPassed(time):
    #Verify the time given
    if (not time.__contains__(":")) | (time.__len__() < 4) | (time.__len__() > 5):
        return -1
    #Split the correctly formated string into hours and minutes
    time = time.split(":")
    #Ensure numbers were given in the string
    if (not time[0].isdigit()) | (not time[1].isdigit()):
        return -1
    #convert time to the decimal format of hours
    hour = int(time[0]) + float(time[1])/60
    #subtract the time by 8 to find the amount of time passed since 8:00AM
    return (hour - 8)

#Displays the interface for seeing the package data
def packageInterface(option, packages):
    while (option != 4):
        print("Would you like to:")
        print("1. Show All Package Data")
        print("2. Search A Package ID")
        print("3. Exit")
        print("4. Return to Main Menu")
        option = input("Choose your option: ")
        while ((not option.isdigit()) | (int(option) > 4) | (int(option) < 1)):
            option = input("Choose your option: ")
        option = int(option)

        if (option == 1):
            showAllPackages(packages)
            print("-------------------------------------")
            print("")

        if (option == 2):
            packageID = input("Enter the package ID: ")
            while ((not packageID.isdigit()) | (int(packageID) < 0) | (int(packageID) > 40)):
                packageID = input("Enter a valid package ID: ")
            print(lookUpPackage(packages, int(packageID)))
            print("-------------------------------------")
            print("")

        if (option == 3):
            exit("Program ended")

        if (option == 4):
            print("")


option = 4
while(option == 4):
    print("Welcome to the WGUPS Package Delivery System:")
    print("---------------------------------------------")
    print("Loading package data.........")
    try:
        packages = loadPackages()
    except:
        exit("Error loading package data")
    print("Loading address data.........")
    try:
        addressList = loadAddressData()
    except:
        exit("Error Loading address data")
    print("Loading trucks.....")
    try:
        truck1 = packageHashTable()
        truck2 = packageHashTable()
        truck3 = packageHashTable()
        loadTrucks(truck1, truck2, truck3, packages)
        truckHashList = (truck1, truck2, truck3)
    except:
        exit("Error Loading Trucks")
    print("Address, Package Data, and Trucks Loaded Successfully")
    print("---------------------------------------------")
    print("Enter a number corresponding to the action you would like to perform")
    print("1. Deliver All Packages")
    print("2. See Status of Packages at Specific Time")
    print("3. Exit program")
    print("---------------------------------------------")
    option = input("Choose your option: ")
    while ((not option.isdigit()) | (int(option) > 3) | (int(option) < 1)):
        option = input("Please enter a valid entry: ")
    option = int(option)

    if (option == 1):
        print("Packages delivered")
        print("Total Distance Traveled by all trucks is " + str(deliverAllPackages(truckHashList, addressList)))
        print("-------------------------------------------")
        print("")
        packageInterface(option, packages)
        option = 4

    if(option == 2):
        print("")
        print("Please Enter a time in UTC Format")
        print("Example 9:00 for 9:00AM or 13:00 for 1:00PM")
        time = input("Enter a time after 8:00AM: ")
        while((hoursPassed(time) < 0) | (hoursPassed(time) > 16)):
            time = input("Please enter valid input, which is a valid time after 8:00AM: ")

        print("Packages delivered")
        deliverPackages(truckHashList, addressList, hoursPassed(time))
        print("-------------------------------------------")
        print("")
        packageInterface(option, packages)
        option = 4


    if (option == 3):
        exit("Program ended")




