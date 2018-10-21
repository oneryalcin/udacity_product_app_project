from catalog_app.models import Category, Item
from catalog_app import db


# Create few categories
football = Category(name='Football')
basketball = Category(name="Basketball")
swimming = Category(name="Swimming")
db.session.add_all([football, basketball, swimming])
db.session.commit()


# Add two items per category
fball = Item(1, "Football Ball", "The Adidas Fevernova was the official match ball of 2002 FIFA World Cup "
                                 "in South Korea and Japan, manufactured by Adidas.")
fjersey = Item(1, "Maradona Jersey", "This classical Argentinian jersey was worn by Maradona during the World Cup "
                                     "match between Argentina and England, where he score 2 honest goals")
bball = Item(2, "Basketball Ball", "Spalding developed its first basketball in 1894 and is currently a leading "
                                   "producer. Since 1983, it has been the Official ball supplier to the National "
                                   "Basketball Association (NBA).")
bjersey = Item(2, "Michael Jordan Jersey", "Legendary Red Chicago Bulls Number 23 Jersey worn by Michael Jordan "
                                           "during 1996-1997 NBA season ")
goggle = Item(3, "Swimming Goggles", "Must be watertight to prevent water, such as salt water when swimming in the "
                                     "ocean, or chlorinated water when swimming in a pool, from irritating the eyes or "
                                     "blurring vision. Allow swimmers to see clearly underwater.")
boardshort = Item(3, "Boardshort", "Boardshorts are a type of swimwear and casual wear in the form of relatively long "
                                   "(approximately knee length) loose-fitting shorts that are designed to be "
                                   "quick-drying and are generally made from strong and smooth polyester or nylon "
                                   "material. ")
db.session.add_all([fball, bball, goggle, fjersey, bjersey, boardshort])
db.session.commit()


