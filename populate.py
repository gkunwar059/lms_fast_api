from database import session,Members,Books,Base,MemberBook,MemberMagazine,Magazine,Publisher,Records,Category

pub=Publisher(name="Minesh",contact_no=9804844,address="Daraba Marg")

session.add(pub)

cat=Category(name="Sajilo xa")
session.add(cat)


book1=Books(isbn=98,title="test1",author="Ram harikrina",price=2500,publishers=pub,categories=cat)
session.add(book1)
book2=Books(isbn=89,title="test2",author="Ram harskrisa",price=2500,publishers=pub,categories=cat)
session.add(book2)


member1=Members(name="Abishepok hrel",member_type='Customer',email='abie923@gmail.com',address='setpul ',contact_no=957699937)
session.add(member1)
member2=Members(name="Abis pokhel",member_type='Customer',email='ab1283@gmail.com',address='setoul ',contact_no=957659997)
session.add(member2)


book1.members=[member1,member2]
member1.books=[book1,book2]
session.commit()














# member1=Members(name="Ganesh jkunr",member_type="Customer",email="ragubir@gmail.com",address='kalopujjjl',contact_no=656565)
# session.add(member1)

# book1=Books(isbn='4001',title='MOha aaya',author="Laxmi Praad Devkota",price=400,publishers=pub,categories=cat)
# session.add(book1)
# # session.commit()


# magazine=Magazine(issn='5001',title='Sadha Bhari',price=1400,editor="Pras Khanal",publishers=pub,categories=cat)
# session.add(magazine)
# # session.commit()



# record=Records(members=member1,books=book1,magazines=magazine,category=cat,publishers=pub)
# session.add(record)
# session.commit()









































# # add member
# member1=Members(name="Adesh pokhrel",member_type='staff',email='adh123@gmail.com',address='samakoshi',contact_no=981022869)
# session.add(member1)

# member2=Members(name="Abishek pokhrel",member_type='Customer',email='abiek123@gmail.com',address='setopul ',contact_no=986576537)
# session.add(member2)

# session.commit()


# # book
# book1=Books(isbn=2211,title="Muna Madan",author="Ram krishna",price=2500)
# session.add(book1)

# book2=Books(isbn=11,title="Madan Krishna",author="krishna",price=200)
# session.add(book2)
# session.commit()


# # book to member
# book1.members=[member1,member2]
# book2.members=[member2]

# member1.books=[book1,book2]
# member1.books=[book1]

# session.commit()


# # member to test the magazine 
# m1=Members(name="Ramesh pokhrel",member_type='customer',email='ggprbhu123@gmail.com',address='samkoshii',contact_no=9882869)
# session.add(m1)

# m2=Members(name="Ganesh k",member_type='user',email='yyabindra3@gmail.com',address='sshii',contact_no=9870069)
# session.add(m2)

# session.commit()

# # aadd magazine
# mag= Magazine(issn=39,title='Fashion HUb',price=345,editor="Ramshah")
# session.add(mag)

# mag2= Magazine(issn=65,title='History HUb',price=360,editor="Harish Shah")
# session.add(mag2)

# mag3= Magazine(issn=70,title='HUb',price=390,editor="Harish Gaah")
# session.add(mag2)


# mag.members=[m1,m2]
# mag2.members=[m1]
# session.commit()



