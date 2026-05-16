from db.mongo import MongoDB


insert_data = {
    "name":"sample2",
    "age":25,
    "gender":"male"
}
m = MongoDB("Testcollection",filterkey={"name":"sample2"})
m.deleteMany()








