#1. Używając kolekcji „restaurants” wykonaj poniższe zadania
#2. Dodaj własną restaurację „Student Culture Zone” używając polecenia „insertOne”

db.restaurants.insertOne({name: "Student Culture Zone"})

#3. Zmień nazwę dodanej restaucacji na „Student Culture Zone PWR”

db.restaurants.updateOne({name: "Student Culture Zone"}, {$set:{name: "Student Culture Zone PWR"}})


#4. Usuń dodaną restaurację

db.restaurants.deleteOne({name: "Student Culture Zone PWR"})


#5. Zmień nazwę pola „name” na „restaurant _name”


db.restaurants.updateMany({},{$rename:{"name":"restaurant_name"}})


#6. Dodaj pole warunkowe „A class”: true jeżeli restauracja posiada przynajmniej jeden grade 
„A”, używając „$cond”

db.restaurants.aggregate(
  {$addFields:
    {"A class":
      {$cond:{
        if:{grades:{grade:"A"}},
          then:true,
          else:false}}}
  },
  {$merge: {into: "restaurants",
            on: "_id", 
            whenMatched: "replace",
            whenNotMatched: "insert" }})

db.restaurants.updateMany({},[{$set:{"A class":{$cond:{if:{$anyElementTrue:{$map:{input:"$grades",as:"grade",in:{$eq:["$$grade.grade","A"]}}}},then:true,else:false}}}}])
