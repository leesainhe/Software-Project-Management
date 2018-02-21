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
