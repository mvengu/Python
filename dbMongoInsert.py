from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017") #host uri
db = client.mymongodb    #Select the database
todos = db.todo #Select the collection name

def InsertMemberRecord(hnu, ona, mob):
    mydict = {"HouseNumber": hnu, "OwnerName": ona, "MobileNumber": mob }
    x = todos.insert_one(mydict)

def UpdateMemberRecord(id,hnu, ona, mob):
    myquery = { "_id": id }
    newvalues = { "$set": { "HouseNumber": hnu, "OwnerName":ona,"MobileNumber":mob } }
    todos.update_one(myquery,newvalues) 

def DeleteMemberRecord(id):
    myquery = { "_id": id }
    todos.delete_one(myquery) 

def listRecords():
    x = todos.find({})
    items = []
    print (x)
    for obj in x:
        print(obj)
        items.append(obj)
    return items

def get_member(HouseNumber):
    myquery={"HouseNumber" : HouseNumber}
    member = todos.find_one(myquery)
    if member is None:
        abort(404)
    return member

if __name__ == "__main__":
    listRecords()