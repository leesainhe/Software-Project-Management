
class DBCommunicator:

	def __init__(self, cursor):
        	self.cursor = cursor

	def get_movies(self):
	        return self.cursor.execute('''SELECT id, movie_name, movie_rating
                                      FROM Movies
                                      ORDER BY movie_rating DESC''')

	def get_seats(self, movie_id):
        	return self.cursor.execute('''SELECT seats.id, seat_type, seat_time,
                                             seat_date, movie_id, movie_name
                                      FROM seats
                                      JOIN Movies
                                      ON seats.movie_id = Movies.id
                                      WHERE movie_id = ?
                                      ORDER BY seat_date''', (str(movie_id), ))

	def get_seats_with_date(self, movie_id, date):
	        return self.cursor.execute('''SELECT seats.id, seat_type, seat_time,
                                             seat_date, movie_id, movie_name
                                      FROM seats
                                      JOIN Movies
                                      ON seats.movie_id = Movies.id
                                      WHERE movie_id = ? AND seat_date = ?
                                      ORDER BY seat_date''', (str(movie_id), str(date)))


class controller:

	def __init__(self, db_communicator):
        	self.db_communicator = db_communicator
	
	def generate_movies_table(self):
        	table = PrettyTable(["id", "movie_name", "movie_rating"])
        	for row in self.db_communicator.get_movies():
            		table.add_row([row["id"], row["movie_name"], row["movie_rating"]])
		return table

	def show_movies(self, *args):
        	print(self.controller.generate_movies_table())
	
	def generate_seats_table(self, movie_id, date):
        	if date is not None:
        	    db_result = self.db_communicator.get_seats_with_date(movie_id, date)
        	else:
        	    db_result = self.db_communicator.get_seats(movie_id)

        	table = PrettyTable(["seat_id", "seat_type", "seat_time",
                             "seat_date", "movie_id", "movie_name"])
	        for row in db_result:
	            table.add_row([row["id"], row["seat_type"], row["seat_time"],
                           row["seat_date"], row["movie_id"],
                           row["movie_name"]])
        	return table

class CLI:
	def __init__(self, controller):
        	self.controller = controller

        	self.__user_is_active = True
        	self.commands = {"show_movies": self.show_movies,"show_seats": self.show_seats,
            				"make_reservations": self.make_reservations,"exit": self.exit}

	def show_movies(self, *args):
        	print(self.controller.generate_movies_table())

	def show_seats(self, *args):
        	movie_id = args[0]
        	date = None
        	if len(args) > 1:
        	    date = args[1]
	print(self.controller.generate_seats_table(movie_id, date))

	def show_reservations(self, data):
        	print(self.controller.generate_reservations_table(data))


	def make_reservations(self, *args):

		//input user data
		username = input("Enter your name: ")
		number_of_tickets = int(input("Enter number of tickets: "))
		
        	self.show_movies()
		//show_movies() is the class for displaying movies available in the theatre
	
		movie_id = int(input("Enter movie id: "))

        	self.show_seats(movie_id)
		//show_seats() is the function for showing available seats

        	seat_id = int(input("Enter seat id: "))
        	self.show_reservations(self.controller.create_cinema(seat_id))
		
def main():
    db = sqlite3.connect("cinema_data.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    db_communicator = DBCommunicator(cursor)
    controller = Controller(db_communicator)
    cli = CLI(controller)
    cli.start()


if __name__ == '__main__':
    main()
