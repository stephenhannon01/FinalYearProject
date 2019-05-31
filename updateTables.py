#!/usr/bin/python3
import pymysql as db

connection = db.connect('mysql.netsoc.co', 'visrec', 'hFfx3SJcsFUZV', 'visrec_users')
cursor = connection.cursor(db.cursors.DictCursor)

#name, imdb_rating, primary_genre, secondary_genre, synopsis, age_rating
movieList=[]
movie=['Mad Maxx: Fury Road (2015)', 8.1, 'action', 'adventure', 'A woman rebels against a tyrannical ruler in postapocalyptic Australia in search for her home-land with the help of a group of female prisoners, a psychotic worshipper, and a drifter named Max. ', 15, 'http://www.imdb.com/title/tt1392190/', 'MadMaxx.jpg']
movieList.append(movie)

movie=['Inside Out (2015)', 8.2, 'animation', 'adventure', 'After young Riley is uprooted from her Midwest life and moved to San Francisco, her emotions - Joy, Fear, Anger, Disgust and Sadness - conflict on how best to navigate a new city, house, and school. ', 15, 'http://www.imdb.com/title/tt2096673/', 'insideout.jpg']
movieList.append(movie)

movie=['Selma (2015)', 7.5, 'drama', 'biography', 'A chronicle of Dr. Martin Luther King, Jr.s campaign to secure equal voting rights via an epic march from Selma to Montgomery, Alabama, in 1965. ', 15, 'http://www.imdb.com/title/tt1020072/', 'selma.jpg']
movieList.append(movie)

movie=['Brooklyn (2015)', 7.5, 'drama', 'adventure', 'An Irish immigrant lands in 1950s Brooklyn, where she quickly falls into a romance with a local. When her past catches up with her, however, she must choose between two countries and the lives that exist within. ', 15, 'http://www.imdb.com/title/tt2381111/', 'brooklyn.jpg']
movieList.append(movie)

movie=['It Follows (2015)', 6.9, 'horror', 'mystery', 'A young woman is followed by an unknown supernatural force after a sexual encounter. ', 15, 'http://www.imdb.com/title/tt3235888/', 'itfollows.jpg']
movieList.append(movie)

movie=['Spotlight (2015)', 8.1, 'mystery', 'drama', 'The true story of how the Boston Globe uncovered the massive scandal of child molestation and cover-up within the local Catholic Archdiocese, shaking the entire Catholic Church to its core. ', 12, 'http://www.imdb.com/title/tt1895587/', 'spotlight.jpg']
movieList.append(movie)

movie=['Shaun the Sheep (2015)', 2, 'animation', 'comedy', 'When Shaun decides to take the day off and have some fun, he gets a little more action than he bargained for. A mix up with the Farmer, a caravan and a very steep hill lead them all to the Big City and its up to Shaun and the flock to return everyone safely to the green grass of home.', 0, 'http://www.imdb.com/title/tt2872750/', 'shaunthesheep.jpg']
movieList.append(movie)

movie=['The Martian (2015)', 7.4, 'adventure', 'mystery', 'An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive. ', 12, 'http://www.imdb.com/title/tt3659388/', 'themartian.jpg']
movieList.append(movie)

movie=['Room (2015)', 9, 'horror', 'action', 'A young boy is raised within the confines of a small shed. ', 12, 'http://www.imdb.com/title/tt3170832/', 'room.jpg']
movieList.append(movie)

movie=['Cone Girl (2014)', 4, 'drama', 'horror', 'With his wifes disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when its suspected that he may not be innocent. ', 15, 'http://www.imdb.com/title/tt2267998/', 'gonegirl.jpg']
movieList.append(movie)

movie=['Interstellar (2014)', 8, 'adventure', 'mystery', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanitys survival. ', 15, 'http://www.imdb.com/title/tt0816692/', 'interstellar.jpg']
movieList.append(movie)

movie=['Guardians of the Galaxy (2014)', 6.5, 'sci-fi', 'action', 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.', 12, 'http://www.imdb.com/title/tt2015381/', 'guardians.jpg']
movieList.append(movie)

movie=['The Lego Movie (2014)', 6, 'animation', 'comedy', 'An ordinary Lego construction worker, thought to be the prophesied Special, is recruited to join a quest to stop an evil tyrant from gluing the Lego universe into eternal stasis.', 0, 'http://www.imdb.com/title/tt1490017/', 'thelegomovie.jpg']
movieList.append(movie)

movie=['Birdman (2014)', 10, 'drama', 'action', 'A washed-up Hollywood actor, who once played a famous superhero, attempts to revive his career by writing and starring in a Broadway play. ', 12, 'http://www.imdb.com/title/tt2562232/', 'birdman.jpg']
movieList.append(movie)

movie=['The Babdook (2014)', 8, 'horror', 'drama', 'A widowed mother, plagued by the violent death of her husband, battles with her sons fear of a monster lurking in the house, but soon discovers a sinister presence all around her. ', 15, 'http://www.imdb.com/title/tt2321549/', 'thebabadook.jpg']
movieList.append(movie)

movie=['Moonight (2015)', 7, 'drama', 'action', 'A chronicle of the childhood, adolescence and burgeoning adulthood of a young, African-American, gay man growing up in a rough neighborhood of Miami.', 15, 'http://www.imdb.com/title/tt4975722/', 'moonlight.jpg']
movieList.append(movie)

movie=['Deadpool (2015)', 5, 'comedy', 'action', 'A fast-talking mercenary with a morbid sense of humor is subjected to a rogue experiment that leaves him with accelerated healing powers and a quest for revenge. ', 15, 'http://www.imdb.com/title/tt1431045/', 'deadpool.jpg']
movieList.append(movie)

movie=['La La Land (2015)', 9, 'drama', 'mystery', 'While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.', 12, 'http://www.imdb.com/title/tt3783958/', 'lalaland.jpg']
movieList.append(movie)

movie=['Doctor Strange (2015)', 5, 'comedy', 'sc-fi', 'While on a journey of physical and spiritual healing, a brilliant neurosurgeon is drawn into the world of the mystic arts.', 12, 'http://www.imdb.com/title/tt1211837/', 'doctorstrange.jpg']
movieList.append(movie)

movie=['Moana (2015)', 7, 'animation', 'comedy', 'In Ancient Polynesia, when a terrible curse incurred by the Demigod Maui reaches Moanas island, she answers the Oceans call to seek out the Demigod to set things right.', 0, 'http://www.imdb.com/title/tt3521164/', 'moana.jpg']
movieList.append(movie)

movie=['Shutter Island (2010)', 9, 'drama', 'horror', 'In 1954, a U.S. Marshal investigates the disappearance of a murderer, who escaped from a hospital for the criminally insane.', 12, 'http://www.imdb.com/title/tt1130884/', 'shutterisland.jpg']
movieList.append(movie)

movie=['Despicable Me (2010)', 5, 'animation', 'comedy', 'When a criminal mastermind uses a trio of orphan girls as pawns for a grand scheme, he finds their love is profoundly changing him for the better. ', 0, 'http://www.imdb.com/title/tt1323594/', 'despicableme.jpg']
movieList.append(movie)

movie=['Inception (2010)', 9, 'drama', 'mystery', 'A thief, who steals corporate secrets through use of dream-sharing technology, is given the inverse task of planting an idea into the mind of a CEO.', 12, 'http://www.imdb.com/title/tt1375666/', 'inception.jpg']
movieList.append(movie)

movie=['Easy E (2010)', 3, 'comedy', 'drama', 'A clean-cut high school student relies on the schools rumor mill to advance her social and financial standing. ', 12, 'http://www.imdb.com/title/tt1282140/', 'easya.jpg']
movieList.append(movie)

movie=['Fighter (2010)', 7.5, 'drama', 'mystery', 'A look at the early years of boxer "Irish" Micky Ward and his brother who helped train him before going pro in the mid 1980s.', 15, 'http://www.imdb.com/title/tt0964517/', 'fighter.jpg']
movieList.append(movie)

movie=['The Other Guys (2010)', 6, 'comedy', 'action', 'Two mismatched New York City detectives seize an opportunity to step up like the citys top cops whom they idolize -- only things dont quite go as planned.', 15, 'http://www.imdb.com/title/tt1386588/', 'theotherguys.jpg']
movieList.append(movie)

movie=['Predators (2010)', 5, 'horror', 'action', 'A group of elite warriors parachute into an unfamiliar jungle and are hunted by members of a merciless alien race.', 15, 'http://www.imdb.com/title/tt1424381/', 'predators.jpg']
movieList.append(movie)

movie=['Avatar (2010)', 4, 'adventure', 'drama', 'A paraplegic marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.', 12, 'http://www.imdb.com/title/tt0499549/', 'avatar.jpg']
movieList.append(movie)

movie=['District 9 (2009)', 3, 'action', 'sci-fi', 'An extraterrestrial race forced to live in slum-like conditions on Earth suddenly finds a kindred spirit in a government agent who is exposed to their biotechnology.', 15, 'http://www.imdb.com/title/tt1136608/', 'district9.jpg']
movieList.append(movie)

movie=['Fast and Furious (2009) ', 1, 'action', 'comedy', 'Former cop Brian O Conner is called upon to bust a dangerous criminal and he recruits the help of a former childhood friend and street racer who has a chance to redeem himself.', 15, 'http://www.imdb.com/title/tt0322259/', 'fastandfurious.jpg']
movieList.append(movie)


for movie in movieList:
    cursor.execute("""UPDATE movies SET imdb_rating = %s WHERE name = %s""" , (movie[1], movie[0]))
    print("""UPDATE movies SET imdb_rating = %s WHERE name = %s""" , (movie[1], movie[0]))
    cursor.execute("""UPDATE movies SET primary_genre = %s WHERE name = %s""" , (movie[2], movie[0]))
    cursor.execute("""UPDATE movies SET secondary_genre = %s WHERE name = %s""" , (movie[3], movie[0]))
    cursor.execute("""UPDATE movies SET synopsis = %s WHERE name = %s""" , (movie[4], movie[0]))
    cursor.execute("""UPDATE movies SET age_rating = %s WHERE name = %s""" , (movie[5], movie[0]))
    cursor.execute("""UPDATE movies SET imdb_link = %s WHERE name = %s""" , (movie[6], movie[0]))
    cursor.execute("""UPDATE movies SET image_name = %s WHERE name = %s""" , (movie[7], movie[0]))

cursor.execute("""SELECT * FROM movies""")
answer=cursor.fetchall()
for row in answer:
    print(row)

connection.commit()
connection.close()
