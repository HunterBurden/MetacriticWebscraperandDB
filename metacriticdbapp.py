import sqlite3
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


connection = sqlite3.connect('metacriticgames.db')
db = connection.cursor()

run = True

print("Hello, welcome to the MetaCritic Game Database, what would you like to do?\n")

while(run == True):
    print("1. Search for a specific game.")
    print("2. Search for a group of games.")
    print("3. Search for games by developer.")
    print("4. Search for games by publisher.")
    print("5. Search for games by rating.")
    print("6. Search for games by Metascore.")
    print("7. Search for games by userscore.")
    print("8. Search for games by release date.")
    print("9. Search for games by genre.")
    print("10. Search for games by platform released on.")
    print("11. Search for Cover Art.")
    print("12. Search for games using a mixture of attributes.")
    print("13. Look at some graphical representations of the data.")
    print("14. Exit")
    print("Please enter the number of the option you want.\n")

    menu = input()
    if(menu == "1"):
        option_one = False
        
        while(option_one == False):
            new_name = False
            
            print("What game would you like to look for?(Not case sensitive, but game title must be exact).")
            print("Enter 1 if you would like to return to the main menu.")
            name = input("")
            if(name == "1"):
               option_one = True
               new_name = True
               
            print("What would you like to know about", name, "?")
            print("Please enter the number of the option you want.\n")

            while(new_name == False):
                print("1. Search for the developer.")
                print("2. Search for the publisher.")
                print("3. Search for the release date.")
                print("4. Search for rating.")
                print("5. Search for the Metacore.")
                print("6. Search for the userscore.")
                print("7. Search for the platforms released on.")
                print("8. Search for the genres.")
                print("9. Search for the cover art.")
                print("10. Search for a new game.")

                search = input("")
                if(search == "1"):
                    db.execute("select distinct developer from game where name like ?", (name,))
                    query = db.fetchall()
                    for i in query:
                        tup = i
                        print("\nDeveloper:", tup[0])
                    print("\n")
                elif(search == "2"):
                    db.execute("select distinct publisher from game where name like ?", (name,))
                    query = db.fetchall()
                    for i in query:
                        tup = i
                        print("\nPublisher:", tup[0])
                    print("\n")
                elif(search == "3"):
                    db.execute("select distinct release_date, platform from game where name like ?", (name,))
                    query = db.fetchall()
                    print("\nRelease Date on Platform:")
                    for i in query:
                        tup = i
                        print(tup[0], "on", tup[1])
                    print("\n")
                elif(search == "4"):
                    db.execute("select distinct rating from game where name like ?", (name,))
                    query = db.fetchall()
                    for i in query:
                        tup = i
                        print("\nRating:", tup[0])
                    print("\n")
                elif(search == "5"):
                    db.execute("select meta_score, platform from game where name like ?", (name,))
                    query = db.fetchall()
                    print("\nMetascore on Platform:")
                    for i in query:
                        tup = i
                        print(tup[0], "on", tup[1])
                    print("\n")
                elif(search == "6"):
                    db.execute("select user_score, platform from game where name like ?", (name,))
                    query = db.fetchall()
                    print("\nUserscore on Platform:")
                    for i in query:
                        tup = i
                        print(tup[0], "on", tup[1])
                    print("\n")
                elif(search == "7"):
                    db.execute("select platform from game where name like ?", (name,))
                    query = db.fetchall()
                    print("\nPlatform(s):")
                    for i in query:
                        tup = i
                        print(tup[0])
                    print("\n")
                elif(search == "8"):
                    genre_set = set()
                    db.execute("select id from game where name like ?", (name,))
                    ids = db.fetchall()
                    for i in ids:
                        number = i
                        for j in number:
                            db.execute("select distinct genre from (game natural join genre) where id = ?", (j,))
                            query = db.fetchall()
                            for k in query:
                                for l in k:
                                    genre_set.add(l)
                    print("\nGenre(s):")
                    for genre in genre_set:
                        print(genre)
                    print("\n")
                elif(search == "9"):
                    db.execute("select cover_art from game where name like ?", (name,))
                    query = db.fetchall()
                    for i in query:
                        tup = i
                        urllib.request.urlretrieve(tup[0], "cover_art.jpg")
                        img = Image.open("cover_art.jpg")
                        img.show()
                elif(search == "10"):
                    new_name = True
                else:
                    print("That is an invalid option, try again.")
                    print("\n")
                    
    elif(menu == "2"):
        option_two = False

        while(option_two == False):
            print("1. Search for all data in the database. This option outputs the data to a file named games.csv.(Warning! Database is large.).")
            print("2. Search for all games in the database(Warning! Database is large).")
            print("3. Search for a game starting with a certain character or set of characters.")
            print("4. Count all games")
            print("5. Count all unique titles.")
            print("6. Count all games starting with a certain character or set of characters.")
            print("7. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                name_list = list()
                dev_list = list()
                pub_list = list()
                rating_list = list()
                metascore_list = list()
                userscore_list = list()
                release_list = list()
                platform_list = list()
                cover_list = list()
                db.execute("select * from game")
                query = db.fetchall()
                for i in query:
                    tup = i
                    name_list.append(tup[1])
                    dev_list.append(tup[2])
                    pub_list.append(tup[3])
                    rating_list.append(tup[4])
                    metascore_list.append(tup[5])
                    userscore_list.append(tup[6])
                    release_list.append(tup[7])
                    platform_list.append(tup[8])
                    cover_list.append(tup[9])
                
                df = pd.DataFrame({'Name': name_list, 'Developer': dev_list, 'Publisher': pub_list, 'Rating': rating_list, 'Metascore': metascore_list, 'Userscore': userscore_list, 'Release Date': release_list,
                                   'Platform': platform_list, 'Cover Art': cover_list})
                df.to_csv(r"..\MetacriticWebscraperandDB\games.csv", index = False)
                print("\n")
            elif(search == "2"):
                db.execute("select distinct name from game")
                query = db.fetchall()
                print("\nGames:")
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "3"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select distinct name from game where name like ?", (char + '%',))
                print("\nGames beginning with " + "'" + char + "'" + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "4"):
                db.execute("select count(id) from game")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "games total in this database.")
                print("\n")
            elif(search == "5"):
                db.execute("select count(distinct name) from game")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "unique titles in this database.")
                print("\n")
            elif(search == "6"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select count(distinct name) from game where name like ?", (char + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) starting with " + "'" + char + "'" + " in this database.")
                print("\n")
            elif(search == "7"):
                option_two = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "3"):
        option_three = False

        while(option_three == False):
            print("1. Search for all developers.")
            print("2. Search for all developers starting with a certain character or set of characters.")
            print("3. Search for all games developed by a specified developer.")
            print("4. Count all developers")
            print("5. Count all developers starting with a certain character or set of characters.")
            print("6. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                db.execute("select distinct developer from game")
                print("\nDevelopers:")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "2"):
                print("Which developer(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select distinct developer from game where developer like ?", (char + '%',))
                print("\nDevelopers beginning with " + "'" + char + "'" + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "3"):
                print("Which developer would you like to search for?(Not case sensitive, but developer name must be exact.)")
                char = input("")
                db.execute("select distinct name from game where developer like ?", (char,))
                print("\nGames developed by", char + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "4"):
                db.execute("select count(distinct developer) from game")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "developers in this database.")
                print("\n")
            elif(search == "5"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select count(distinct developer) from game where developer like ?", (char + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "developer(s) starting with " + "'" + char + "'" + " in this database.")
                print("\n")
            elif(search == "6"):
                option_three = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "4"):
        option_four = False

        while(option_four == False):
            print("1. Search for all publishers.")
            print("2. Search for all publishers starting with a certain character or set of characters.")
            print("3. Search for all games published by a specified publisher.")
            print("4. Count all publishers")
            print("5. Count all publishers starting with a certain character or set of characters.")
            print("6. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                db.execute("select distinct publisher from game")
                print("\nPublishers:")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "2"):
                print("Which publisher(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select distinct publisher from game where publisher like ?", (char + '%',))
                print("\nPublisher(s) starting with " + "'" + char + "'" + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "3"):
                print("Which publisher would you like to search for?(Not case sensitive, but publisher name must be exact.)")
                char = input("")
                db.execute("select distinct name from game where publisher like ?", (char,))
                print("\nGames published by", char + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "4"):
                db.execute("select count(distinct publisher) from game")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "publishers in this database.")
                print("\n")
            elif(search == "5"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select count(distinct publisher) from game where publisher like ?", (char + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "publisher(s) containing " + "'" + char + "'" + " in this database.")
                print("\n")
            elif(search == "6"):
                option_four = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "5"):
        option_five = False

        while(option_five == False):
            print("1. Search for all ratings.")
            print("2. Search for all games of a specified rating.")
            print("3. Count all ratings")
            print("4. Count individual ratings.")
            print("5. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                db.execute("select distinct rating from game")
                query = db.fetchall()
                print("\nRatings:")
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "2"):
                print("What rating would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select distinct name from game where rating like ?", (char,))
                query = db.fetchall()
                print("\nGames with rating", char + ':')
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "3"):
                db.execute("select count(rating), rating from game group by rating")
                query = db.fetchall()
                print("\nOccurrences of each rating:")
                for i in query:
                    tup = i
                    print("There are", tup[0], "occurrence(s) of", tup[1], "in this database.")
                print("\n")
            elif(search == "4"):
                print("Which rating would you like to search for?(Not case sensitive.)")
                char = input("")
                db.execute("select count(rating) from game where rating like ?", (char + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "occurrence(s) of rating", char, "in this database.")
                print("\n")
            elif(search == "5"):
                option_five = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "6"):
        option_six = False

        while(option_six == False):
            print("1. Search for all games greater than a specified Metascore.")
            print("2. Search for all games less than a specified Metascore.")
            print("3. Search for all games equal to a specified Metascore.")
            print("4. Count all games greater than a specified Metascore.")
            print("5. Count all games less than a specified Metascore.")
            print("6. Count all games equal to a specified Metascore.")
            print("7. Average all Metascores of a specific game.")
            print("8. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select name, platform from game where meta_score > ?", (input_score,))
                query = db.fetchall()
                print("\nGame(s) with a Metascore greater than " + input_score + ':')
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "2"):
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select name, platform from game where meta_score < ?", (input_score,))
                query = db.fetchall()
                print("\nGame(s) with a Metascore less than " + input_score + ':')
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "3"):
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select name, platform from game where meta_score = ?", (input_score,))
                query = db.fetchall()
                print("\nGame(s) with a Metascore equal to " + input_score + ':')
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "4"):
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select count(name) from game where meta_score > ?", (input_score,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) with a Metascore greater than " + input_score + " in this database")
                print("\n")
            elif(search == "5"):
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select count(name) from game where meta_score < ?", (input_score,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) with a Metascore less than " + input_score + " in this database")
                print("\n")
            elif(search == "6"):
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select count(name) from game where meta_score = ?", (input_score,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) with a Metascore equal to " + input_score + " in this database")
                print("\n")
            elif(search == "7"):
                print("What game's scores would you like to average?(Not case sensitive but title must be exact.)")
                input_name = input("")
                db.execute("select avg(meta_score) from game where name like ?", (input_name,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("The average Metascore of", input_name, "is", tup[0])
                print("\n")
            elif(search == "8"):
                option_six = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "7"):
        option_seven = False

        while(option_seven == False):
            print("1. Search for all games greater than a specified userscore.")
            print("2. Search for all games less than a specified userscore.")
            print("3. Search for all games equal to a specified userscore.")
            print("4. Count all games greater than a specified userscore.")
            print("5. Count all games less than a specified userscore.")
            print("6. Count all games equal to a specified userscore.")
            print("7. Average all userscores of a specific game.")
            print("8. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select name, platform from game where user_score > ?", (input_score,))
                query = db.fetchall()
                print("\nGame(s) with a userscore greater than " + input_score + ':')
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "2"):
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select name, platform from game where user_score < ?", (input_score,))
                query = db.fetchall()
                print("\nGame(s) with a userscore less than " + input_score + ':')
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "3"):
                print("What score would you like to use(Format: 5.7, 8, 9.5, etc.)?")
                input_score = input("")
                db.execute("select name, platform from game where user_score = ?", (input_score,))
                query = db.fetchall()
                print("\nGame(s) with a userscore equal to " + input_score + ':')
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "4"):
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select count(name) from game where user_score > ?", (input_score,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) with a userscore greater than " + input_score + " in this database")
                print("\n")
            elif(search == "5"):
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select count(name) from game where user_score < ?", (input_score,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) with a userscore less than " + input_score + " in this database")
                print("\n")
            elif(search == "6"):
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select count(name) from game where user_score = ?", (input_score,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) with a userscore equal to " + input_score + " in this database")
                print("\n")
            elif(search == "7"):
                print("What game's scores would you like to average?(Not case sensitive but title must be exact.)")
                input_name = input("")
                db.execute("select avg(user_score) from game where name like ?", (input_name,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("The average userscore of", input_name, "is", tup[0])
                print("\n")
            elif(search == "8"):
                option_seven = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "8"):
       option_eight = False

       while(option_eight == False):
            print("1. Search for all games released after a specified date.")
            print("2. Search for all games released before a specified date.")
            print("3. Search for all games released on a specified date.")
            print("4. Count all games released on after specified date")
            print("5. Count all games released on before specified date")
            print("6. Count all games released on a specified date")
            print("7. Return to main menu")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select name, platform from game where release_date > ?", (date + '%',))
                query = db.fetchall()
                print("\nGame(s) released after", date)
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "2"):
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select name, platform from game where release_date < ?", (date + '%',))
                query = db.fetchall()
                print("\nGame(s) released before", date)
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "3"):
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select name, platform from game where release_date like ?", (date + '%',))
                query = db.fetchall()
                print("\nGame(s) released on", date)
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "4"):
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select count(name) from game where release_date > ?", (date + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("There were", tup[0], "game(s) released after", date)
                print("\n")
            elif(search == "5"):
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select count(name) from game where release_date < ?", (date + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("There were", tup[0], "game(s) released before", date)
                print("\n")
            elif(search == "6"):
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select count(name) from game where release_date like ?", (date + '%',))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("There were", tup[0], "game(s) released on", date)
                print("\n")
            elif(search == "7"):
                option_eight = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "9"):
        option_nine = False

        while(option_nine == False):
            print("1. Show all genres in the database.")
            print("2. Search for all games of a specific genre.")
            print("3. Count all games of a specific genre.")
            print("4. Search for the highest Metascore by genre.")
            print("5. Search for the lowest Metascore by genre.")
            print("6. Search for the highest userscore by genre.")
            print("7. Search for the lowest userscore by genre.")
            print("8. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                db.execute("select distinct genre from genre")
                query = db.fetchall()
                print("\nGenres:")
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "2"):
                print("Which genre would you like to search for?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select distinct name from (game natural join genre) where genre like ?", (input_genre,))
                query = db.fetchall()
                print("\nGame(s) belonging to the", input_genre, "genre:")
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "3"):
                print("Which genre would you like to count?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select count(distinct name) from (game natural join genre) where genre like ?", (input_genre,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThere are", tup[0], "game(s) in the", input_genre, "genre in this database")
                print("\n")
            elif(search == "4"):
                print("Which genre would you like to search for?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select name, platform, max(meta_score), genre from (game natural join genre) where genre like ?", (input_genre,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "on", tup[1], "with a score of", tup[2], "has the highest Metascore in the", tup[3], "genre")
                print("\n")
            elif(search == "5"):
                print("Which genre would you like to search for?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select name, platform, min(meta_score), genre from (game natural join genre) where genre like ?", (input_genre,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "on", tup[1], "with a score of", tup[2], "has the lowest Metascore in the", tup[3], "genre")
                print("\n")
            elif(search == "6"):
                print("Which genre would you like to search for?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select name, platform, max(user_score), genre from (game natural join genre) where genre like ?", (input_genre,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "on", tup[1], "with a score of", tup[2], "has the highest userscore in the", tup[3], "genre")
                print("\n")
            elif(search == "7"):
                print("Which genre would you like to search for?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select name, platform, min(user_score), genre from (game natural join genre) where genre like ?", (input_genre,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "on", tup[1], "with a score of", tup[2], "has the lowest userscore in the", tup[3], "genre")
                print("\n")
            elif(search == "8"):
                option_nine = True
            else:
                print("That is an invalid option, try again.")
                
    elif(menu == "10"):
        option_ten = False

        while(option_ten == False):
            print("1. Show all platforms in the database.")
            print("2. Search for all games of a specific platform.")
            print("3. Count all games of a specific platform.")
            print("4. Average all metascores of a specific platform.")
            print("5. Average all userscores of a specific platform.")
            print("6. Search for the newest game on a specified platform")
            print("7. Search for the oldest game on a specified platform")
            print("8. Search for the highest Metascore game on a specified platform")
            print("9. Search for the lowest Metascore on a specified platform")
            print("10. Search for the highest userscore game on a specified platform")
            print("11. Search for the lowest userscore on a specified platform")
            print("12. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                db.execute("select distinct platform from game")
                query = db.fetchall()
                print("\nPlatforms:")
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "2"):
                print("Which platform would you like to search for?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name from game where platform like ?", (input_platform,))
                query = db.fetchall()
                print("\nGame(s) on the", input_platform + ':')
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "3"):
                print("Which platform would you like to count?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select count(name) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\nThe number of game(s) on the", input_platform, "are", tup[0])
                print("\n")
            elif(search == "4"):
                print("Which platform would you like to average the Metascores of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select avg(meta_score) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("The average Metascore of the", input_platform, "is", tup[0])
                print("\n")
            elif(search == "5"):
                print("Which platform would you like to average the userscores of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select avg(user_score) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("The average userscore of the", input_platform, "is", tup[0])
                print("\n")
            elif(search == "6"):
                print("Which platform would you like to find the newest release of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name, platform, release_date from game where release_date in (select max(release_date) from game where platform like ?) and platform like ?", (input_platform, input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "was released on the", tup[1], "on", tup[2])
                print("\n")
            elif(search == "7"):
                print("Which platform would you like to find the oldest release of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name, platform, release_date from game where release_date in (select min(release_date) from game where platform like ?) and platform like ?", (input_platform, input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "was released on the", tup[1], "on", tup[2])
                print("\n")
            elif(search == "8"):
                print("Which platform would you like to find the highest Metascore of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name, platform, max(meta_score) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "was released on the", tup[1], "with a Metascore of", tup[2])
                print("\n")
            elif(search == "9"):
                print("Which platform would you like to find the lowest Metascore of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name, platform, min(meta_score) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "was released on the", tup[1], "with a Metascore of", tup[2])
                print("\n")
            elif(search == "10"):
                print("Which platform would you like to find the highest userscore of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name, platform, max(user_score) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "was released on the", tup[1], "with a userscore of", tup[2])
                print("\n")
            elif(search == "11"):
                print("Which platform would you like to find the lowest userscore of?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select name, platform, min(user_score) from game where platform like ?", (input_platform,))
                query = db.fetchall()
                for i in query:
                    tup = i
                    print("\n" + tup[0], "was released on the", tup[1], "with a userscore of", tup[2])
                print("\n")
            elif(search == "12"):
                option_ten = True
            else:
                print("That is an invalid option, try again.")

    elif(menu == "11"):
         option_eleven = False

         while(option_eleven == False):
             print("Please enter the name of the game that you would like to see the cover art of(Not case sensitive but game title must be exact).")
             print("Enter 1 if you wold like to return to the main menu.")

             search = input("")
             if(search == "1"):
                 option_eleven = True
             else:
                 db.execute("select cover_art from game where name like ?", (search,))
                 query = db.fetchall()
                 for i in query:
                     tup = i
                     urllib.request.urlretrieve(tup[0], "cover_art.jpg")
                     img = Image.open("cover_art.jpg")
                     img.show()
         
    elif(menu == "12"):
        option_twelve = False
        
        while(option_twelve == False):
            print("1. Search for all games with a certain character or set of characters and has a specified rating.")
            print("2. Search for all games with a certain character or set of characters and are greater than a specified Metascore.")
            print("3. Search for all games with a certain character or set of characters and are less than a specified Metascore.")
            print("4. Search for all games with a certain character or set of characters and is equal to a specified Metascore.")
            print("5. Search for all games with a certain character or set of characters and are greater than a specified userscore.")
            print("6. Search for all games with a certain character or set of characters and are less than a specified userscore.")
            print("7. Search for all games with a certain character or set of characters and is equal to a specified userscore.")
            print("8. Search for all games with a certain character or set of characters and released after a specified date.")
            print("9. Search for all games with a certain character or set of characters and released before a specified date.")
            print("10. Search for all games with a certain character or set of characters and released on a specified date.")
            print("11. Search for all games with a certain character or set of characters and belonging to a specified genre.")
            print("12. Search for all games with a certain character or set of characters and released on a specified platform.")
            print("13. Return to main menu.")
            print("Please enter the number of the option you want.\n")

            search = input("")
            if(search == "1"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("Which rating would you like to search for?(Not case sensitive.)")
                input_rating = input("")
                db.execute("select distinct(name), rating from game where name like ? and rating like ?", (char + '%', input_rating))
                print("\nGames beginning with " + "'" + char + "'", "and that have a rating of", input_rating + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "has a rating of", tup[1])
                print("\n")
            elif(search == "2"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select distinct name, platform from game where name like ? and meta_score > ?", (char + '%', input_score,))
                print("\nGames beginning with " + "'" + char + "'", "and greater than Metascore", input_score + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "3"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select distinct name, platform from game where name like ? and meta_score < ?", (char + '%', input_score,))
                print("\nGames beginning with " + "'" + char + "'", "and less than Metascore", input_score + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "4"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("What score would you like to use?(Format: 8, 71, 95, etc.)")
                input_score = input("")
                db.execute("select distinct name, platform from game where name like ? and meta_score = ?", (char + '%', input_score,))
                print("\nGames beginning with " + "'" + char + "'", "and equal to Metascore", input_score + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            if(search == "5"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select distinct name, platform from game where name like ? and user_score > ?", (char + '%', input_score,))
                print("\nGames beginning with " + "'" + char + "'", "and greater than userscore", input_score + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "6"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select distinct name, platform from game where name like ? and user_score < ?", (char + '%', input_score,))
                print("\nGames beginning with " + "'" + char + "'", "and less than userscore", input_score + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "7"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("What score would you like to use?(Format: 5.7, 8, 9.5, etc.)")
                input_score = input("")
                db.execute("select distinct name, platform from game where name like ? and user_score = ?", (char + '%', input_score,))
                print("\nGames beginning with " + "'" + char + "'", "and equal to userscore", input_score + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "8"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select name, platform, release_date from game where name like ? and release_date > ?", (char + '%', date + '%',))
                print("\nGames beginning with ", "'" + char + "'", "and released after", date + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1], "was released on", tup[2])
                print("\n")
            elif(search == "9"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select name, platform, release_date from game where name like ? and release_date < ?", (char + '%', date + '%',))
                print("\nGames beginning with ", "'" + char + "'", "and released before", date + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1], "was released on", tup[2])
                print("\n")
            elif(search == "10"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("Which date would you like to search for?(Format: YYYY-MM-DD, YYYY-MM, YYYY)")
                date = input("")
                db.execute("select name, platform, release_date from game where name like ? and release_date like ?", (char + '%', date + '%',))
                print("\nGames beginning with " + "'" + char + "'", "and released on", date + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1], "was released on", tup[2])
                print("\n")
            elif(search == "11"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("Which genre would you like to search for?(Not case sensitive but genre must be exact.)")
                input_genre = input("")
                db.execute("select distinct(name) from (game natural join genre) where name like ? and genre like ?", (char + '%', input_genre))
                print("\nGames beginning with ", "'" + char + "'", "and belong to the", input_genre, "genre:")
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0])
                print("\n")
            elif(search == "12"):
                print("Which character(s) would you like to search for?(Not case sensitive.)")
                char = input("")
                print("Which platform would you like to search for?(Not case sensitive but platform must be exact.)")
                input_platform = input("")
                db.execute("select distinct(name), platform from game where name like ? and platform like ?", (char + '%', input_platform))
                print("\nGames beginning with ", "'" + char + "'", "and are released on", input_platform + ':')
                query = db.fetchall()
                for i in query:
                    tup = i
                    print(tup[0], "on", tup[1])
                print("\n")
            elif(search == "13"):
                option_twelve = True
            else:
                print("That is an invalid option, try again.")
                    
    elif(menu == "13"):
        option_thirteen = False

        while(option_thirteen == False):
            print("1. Bar Graph of the total games released each year.")
            print("2. Circle Chart of games starting with each letter")
            print("3. Circle Chart of genres")
            print("4. Circle Chart of ratings")
            print("5. Scatter Plot of average Metascore by year")
            print("6. Scatter Plot of average userscore by year")
            print("7. Return to main menu.")
            print("Please enter the number of the option you want.")

            search = input("")
            if(search == "1"):
                year_list = list()
                game_list = list()
                for i in range(1995, 2022):
                    year = str(i)
                    db.execute("select count(name) from game where release_date like ?", (year + '%',))
                    query = db.fetchall()
                    for j in query:
                        tup = j
                        year_list.append(year)
                        game_list.append(tup[0])
                df = pd.DataFrame({'x': year_list, 'y': game_list})
                plt.bar(df.x, df.y)
                plt.xlabel("Year of Release")
                plt.ylabel("Number of Games Released")
                plt.show()
            elif(search == "2"):
                letter_list = list()
                game_list = list()
                letters = "abcdefghijklmnopqrstuvwxyz"
                for i in range(0, len(letters)):
                    db.execute("select count(name) from game where name like ?", (letters[i] + '%',))
                    query = db.fetchall()
                    for j in query:
                        tup = j
                        letter_list.append(letters[i])
                        game_list.append(tup[0])
                df = pd.DataFrame({'Letter': letter_list, 'Number of Games Starting with Letter': game_list}, index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
                df.plot.pie(y = 'Number of Games Starting with Letter', title = 'Letters', autopct='%1.1f%%', figsize=(10, 8))
                plt.show()
            elif(search == "3"):
                genre_list = list()
                count_list = list()
                db.execute("select genre, count(genre) from genre group by genre")
                query = db.fetchall()
                for j in query:
                    tup = j
                    genre_list.append(tup[0])
                    count_list.append(tup[1])
                df = pd.DataFrame({'Genre': genre_list, 'Number of Games Belonging to Genre': count_list}, index=[genre_list])
                df.plot.pie(y = 'Number of Games Belonging to Genre', autopct='%1.1f%%', figsize=(25, 10))
                plt.show()
            elif(search == "4"):
                rating_list = list()
                count_list = list()
                db.execute("select rating, count(rating) from game group by rating")
                query = db.fetchall()
                for j in query:
                    tup = j
                    rating_list.append(tup[0])
                    count_list.append(tup[1])
                df = pd.DataFrame({'Rating': rating_list, 'Number of Games Belonging to Rating': count_list}, index=[rating_list])
                df.plot.pie(y = 'Number of Games Belonging to Rating', autopct='%1.1f%%', figsize=(10, 8))
                plt.show()
            elif(search == "5"):
                year_list = list()
                score_list = list()
                for i in range(1995, 2022):
                    year = str(i)
                    db.execute("select avg(meta_score) from game where release_date like ?", (year + '%',))
                    query = db.fetchall()
                    for j in query:
                        tup = j
                        year_list.append(year)
                        score_list.append(tup[0])
                df = pd.DataFrame({'x': year_list, 'y': score_list})
                plt.scatter(df.x, df.y)
                plt.xlabel("Year")
                plt.ylabel("Average Metascore of Games")
                plt.show()
            elif(search == "6"):
                year_list = list()
                score_list = list()
                for i in range(1995, 2022):
                    year = str(i)
                    db.execute("select avg(user_score) from game where release_date like ?", (year + '%',))
                    query = db.fetchall()
                    for j in query:
                        tup = j
                        year_list.append(year)
                        score_list.append(tup[0])
                df = pd.DataFrame({'x': year_list, 'y': score_list})
                plt.scatter(df.x, df.y)
                plt.xlabel("Year")
                plt.ylabel("Average Userscore of Games")
                plt.show()
            elif(search == "7"):
                option_thirteen = True
            else:
                print("That is an invalid option, try again.")
            
    elif(menu == "14"):
        print("Thank you, have a nice day!")
        run = False

    else:
        print("That is an invalid option, try again.")
