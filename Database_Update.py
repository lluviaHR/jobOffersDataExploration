#
# the database is stored as a list of lists such as DB=[[job offer 1], [job offer 2],...]
#
import sys
import os

#removes all items from the database
def clear():
    global myDatabase
    myDatabase = []    

def idAlreayInTheDatabase(id):
    global myDatabase
    #get ids already in the database
    idsAlreadyInDB = [jobOffer[attributePositions['Job ID']] for jobOffer in myDatabase]
    return id in idsAlreadyInDB

def insert(fieldValues):            
    #if the new id is not already in the database insert it
    id = fieldValues[attributePositions['Job ID']]
    if not idAlreayInTheDatabase(id):
        myDatabase.append(fieldValues)
  
  
def update_all(params):
    query_field_name = params[0]
    query_field_value = params[1]
    update_field_name = params[2]
    update_field_value = params[3]
  
    updatedRowCount = 0

    #for each
    for jobOffer in myDatabase:
        x = jobOffer
        #if it matches the query
        if x[attributePositions[query_field_name]] == query_field_value:
            #if trying to update job id and another job id is already in the database  don't update
            if query_field_name == 'Job ID' and idAlreayInTheDatabase(update_field_value):
                continue
            #update values and the count
            x[attributePositions[update_field_name]] = update_field_value
            updatedRowCount += 1 
    #print count
    print updatedRowCount


def delete_all(params):
    #need to use the global command here, otherwise since we are attributing a value to the variable myDatabase
    #python is going to treat it as a local variable
    global myDatabase
    field_name, field_value = params
    #just keep the job offers that have the values for attribute field name different from field_value
    #this avoids problems with deleting items in sequence from the list
    myDatabase = [z for z in myDatabase if z[attributePositions[field_name]] != field_value]


def find(params):
    field_name = params[0]
    field_value = params[1]
    
    #loops through the list sorted by ids as integers (notice that this conversion 
    #is necessary since the ids are stored as strings in myDatabase)
    for jobOffer in sorted(myDatabase,key=lambda x: int(x[0])):
        #if job offer matches query
        if jobOffer[attributePositions[field_name]] == field_value:
            print "|".join(jobOffer)
    
def count(params):
  field_name, field_value = params
  count = 0

  #loops through the list sorted by ids as integers (notice that this conversion 
  #is necessary since the ids are stored as strings in myDatabase)
  for jobOffer in sorted(myDatabase,key=lambda x: int(x[0])):
    if jobOffer[attributePositions[field_name]] == field_value:
        count += 1
  print count


def dump(params):
    #loops through the list sorted by ids as integers (notice that this conversion 
    #is necessary since the ids are stored as strings in myDatabase)
    for jobOffer in sorted(myDatabase,key=lambda x: int(x[0])):
        print "|".join(jobOffer)


def view(fieldNames):
    #loops through the list sorted by ids as integers (notice that this conversion 
    #is necessary since the ids are stored as strings in myDatabase)
    for jobOffer in sorted(myDatabase,key=lambda x: int(x[0])):
        VIEW = []
        #for each field in fieldNames, include it in the VEW list        
        for fieldName in fieldNames:
            VIEW.append(jobOffer[attributePositions[fieldName]])        
        #prints the fields in VIEW joined by |
        print "|".join(VIEW)


def executeCommand(commandLine):
  tokens = commandLine.split('|') 
  command = tokens[0]
  parameters = tokens[1:]

  if command == 'insert':
    insert(parameters)
  elif command == 'delete_all':
    delete_all(parameters)
  elif command == 'update_all':
    update_all(parameters)
  elif command == 'find':
    find(parameters)
  elif command == 'count':
    count(parameters)
  elif command == 'count_unique':
    count_unique(parameters)
  elif command == 'clear':
    clear()
  elif command == 'dump':
    dump(parameters)
  elif command == 'view':
    view(parameters)
  else:
    print 'ERROR: Command %s does not exist' % (command,)
    assert(False)
    
    
def executeCommands(commandFileName):
  f = open(commandFileName)
  for line in f:
    executeCommand(line.strip())
    

if __name__ == '__main__':
    
    #attributePositionsionary with the positions of each attribute
    attributePositions = {}
    attributePositions['Job ID'] = 0
    attributePositions['Agency'] = 1
    attributePositions['#Of Positions'] = 2
    attributePositions['Business Title'] = 3
    attributePositions['Civil Service Title'] = 4
    attributePositions['Salary Range From'] = 5
    attributePositions['Salary Range To'] = 6
    attributePositions['Salary Frequency'] = 7 
    attributePositions['Work Location'] = 8
    attributePositions['Division/Work Unit'] = 9
    attributePositions['Job Description'] = 10
    attributePositions['Minimum Qual Requirements'] = 11
    attributePositions['Preferred Skills'] = 12
    attributePositions['Additional Information'] = 13
    attributePositions['Posting Date'] = 14
  
    #initialize myDatabase list
    myDatabase=[]  
  
    #test if the data base file 'DataBase.db' was already created, if so, load the data from it
    if os.path.isfile('DataBase.db'):    
        DataBase = open('DataBase.db','r')
        for line in DataBase:
            myDatabase.append(line.strip().split('|'))
        DataBase.close()  
      
    #execute commands 	  
    executeCommands(sys.argv[1])
  
    #write database file for persistence
    Database = open('DataBase.db','w')
    for jobOffers in myDatabase:
        Database.write('|'.join(jobOffers) + '\n') 
    Database.close()  
