from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup1 import User, Categories, Items, Base

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Shawon Dunston", email="shawon@cubs.com")
session.add(User1)
session.commit()


# Category for Soccer
category1 = Categories(user_id=1, name="Soccer")
session.add(category1)
session.commit()

#items for soccer
item1 = Items(user_id=1, title="Nike Pitch Training Soccer Ball",
description="""Built for intense training sessions and improving your footwork visibility to predict trajectory with ease.""", categories=category1)
session.add(item1)
session.commit()

item2 = Items(user_id=1, title="adidas Youth Ghost Soccer Shin Guards",
description="Built to ensure full ankle support and coverage. Guards are a great option for any position while offering a seamless, comfortable fit throughout each match.", categories=category1)
session.add(item2)
session.commit()

# Category for Football
category2 = Categories(user_id=1, name="Football")
session.add(category2)
session.commit()

#items for Football
item3 = Items(user_id=1, title="Riddell Speedflex Helmet",
description="""The goal was to design a helmet with fully integrated components and innovations.""", categories=category2)
session.add(item3)
session.commit()

item4 = Items(user_id=1, title="Champro AMT 1000 Pads",
description="Low-profile cantilever pad construction. Built-in clavicle pads for added protection. Padded epaulet. Integrated deltoid pads.", categories=category2)
session.add(item4)
session.commit()

# Category for Baseball
category3 = Categories(user_id=1, name="Baseball")
session.add(category3)
session.commit()

#items for soccer
item5 = Items(user_id=1, title="Rawlings Quatro USA Bat",
description="""For hitters entering coach or machine pitch leagues, the Rawlings Quatro USSSA Youth Bat is built with a tough alloy and 11 drop weight that gives hitters a lighter swing weight to perform their best.""", categories=category3)
session.add(item5)
session.commit()

item6 = Items(user_id=1, title="DeMarini Paradox Two-Tone Batting Helmet",
description="""The DeMarini Paradox Two-Tone Batting Helmet. The Paradox meets NOCSAE protection standards so you can enter the batter's box with confidence. Also comes in a two-toned rubberrized matte finish that gives it a modern look so you look good at-bat after at-bat.""", categories=category3)
session.add(item6)
session.commit()

print "added categories and items!"
