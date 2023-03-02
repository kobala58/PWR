# 1 Zaimportuj kolekcję „restaurants” z pliku restaurants.json
use restaurants
'switched to db restaurants'


db.createCollection("restaurants")
{ ok: 1 }

z tego miejsca import z GUI

# 2 Wypisz wszystkie dokumenty znajdujące się w kolekcji
db.restaurants.find({})

{ _id: ObjectId("63c66464592c0ac298f47dca"),
  address: 
   { building: '1007',
     coord: [ -73.856077, 40.848447 ],
     street: 'Morris Park Ave',
     zipcode: '10462' },
  borough: 'Bronx',
  cuisine: 'Bakery',
  grades: 
   [ { date: 2014-03-03T00:00:00.000Z, grade: 'A', score: 2 },
     { date: 2013-09-11T00:00:00.000Z, grade: 'A', score: 6 },
     { date: 2013-01-24T00:00:00.000Z, grade: 'A', score: 10 },
     { date: 2011-11-23T00:00:00.000Z, grade: 'A', score: 9 },
     { date: 2011-03-10T00:00:00.000Z, grade: 'B', score: 14 } ],
  name: 'Morris Park Bake Shop',
  restaurant_id: '30075445' }
{ _id: ObjectId("63c66464592c0ac298f47dcb"),
  address: 
   { building: '469',
     coord: [ -73.961704, 40.662942 ],
     street: 'Flatbush Avenue',
     zipcode: '11225' },
  borough: 'Brooklyn',
  cuisine: 'Hamburgers',
  grades: 
   [ { date: 2014-12-30T00:00:00.000Z, grade: 'A', score: 8 },
     { date: 2014-07-01T00:00:00.000Z, grade: 'B', score: 23 },
     { date: 2013-04-30T00:00:00.000Z, grade: 'A', score: 12 },
     { date: 2012-05-08T00:00:00.000Z, grade: 'A', score: 12 } ],
  name: 'Wendy\'S',
  restaurant_id: '30112340' }

# 3 Wypisz name, borough i cuisine dla wszystkich dokumentów znajdujących się w kolekcji

db.restaurants.find({},{'address.street': true, 'name': true, 'borough': true, 'cuisine': true})

# 4 Wypisz name, borough, address. street i cuisine wyłączając id (_id) dla wszystkich dokumentów znajdujących się w kolekcji

db.restaurants.find({},{'address.street': true, 'name': true, 'borough': true, 'cuisine': true, '_id': false})

# 5 Wypisz 5 pierwszych restauracji znajdujących się na Bronx 
db.restaurants.find({borough: "Bronx"}).limit(5)

# 6 Wypisz 5 kolejnych restauracji znajdujących się na Bronx (pomiń pierwsze 5 i wyświetl kolejne 5)
.skip() odpowiada za paginację w MongoDB

db.restaurants.find({borough: "Bronx"}).limit(5).skip(5)

# 7 Wypisz restauracje których score wynosi pomiędzy 5 a 10 

db.restaurants.find({'grades': {$elemMatch: {'score' :{$gte:5, $lte:10}}}})
