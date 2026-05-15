from db.mongo import MongoDB


insert_data = {
    "name":"vicky",
    "age":25,
    "gender":"male"
}
m = MongoDB("Testcollection",findkey={"name":"vignesh"})
m.findOne()







