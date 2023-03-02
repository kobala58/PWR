Lista 11

# 1. Używając kolekcji „restaurants” wykonaj poniższe zadania
# 2. Wypisz wszystkie dokumenty których grade wynosi A, score wynosi 9 i data ma wartość 
ISODate("2014-08-11T00:00:00Z")


db.restaurants.find({"grades.grade":"A","grades.score":9,"grades.date":ISODate("2014-08-11T00:00:00Z")})

# 3. Wyświetl wszystkie restauracje w kolejności alfabetycznej po nazwie restauracji

db.restaurants.find({},{"name":true,"_id":false}).sort({"name":true})


# 4. Wypisz wszystkie restauracje które nie posiadają wartości dla pola address.building

db.restaurants.find({"address.building": {$exists: false}}, {"name": true})
db.restaurants.find({"address.building": {$type: "null"}}, {"name": true})
db.restaurants.find({"address.building": null}, {"name": true})

# 5. Wypisz wszystkie restauracje których nazwa rozpoczyna się od słowa „Shop”, niezależnie od 
wielkości liter

db.restaurants.find({"name":{$regex:"(?i)/^Shop(?-i)"}},{"name":true})

# 6. Wypisz wszystkie restauracje których nazwa zawiera słowa: „Shop” oraz „Pizza”, niezależnie 
od wielkości liter

db.restaurants.find({"name":{$regex:"(?i)shop.*pizza(?-i)"}},{"name":true})
Regex -> 
  ?i = case insensitive
  . = allcharacters
