# Anusha Gupta
# Final Project - final_project.py
# CS 110

#importing modules 
from flask import Flask, request
import os
import random
import tmdbsimple as tmdb 

#creating a Flask web app
app = Flask(__name__)

#enabling debugging mode
app.debug = True

#setting the tmdb API key
tmdb.API_KEY = '163a588832d56a1e13a0997bd6382df3'

#function to generate final HTML page with styles
def final_page_with_style(body, centered=False, button=True):

	#initializing an empty HTML string
    html = ''
    html += '<html>'
    html += '<head>'
    html += '<style>'
    #styling the body
    if centered:
    	html += 'body {background-color: black; color: white; text-align: center;'
    	html += 'font-family: "Georgia", sans-serif; display: flex; justify-content: center;'
    	html += 'align-items: center; height: 100vh; margin: 0;}'
    else:
    	html += 'body {background-color: black; color: white; text-align: center;'
    	html += 'font-family: "Georgia", sans-serif; color: grey;}'
    #styling the buttons
    if button:
	    html += 'button {border: none; font-size: 20px; background-color: transparent; cursor: pointer;}'
    else:
    	html += 'button {border: 1px solid grey; font-size: 25px; background-color: black; cursor: pointer;' 
    	html += 'font-family: "Georgia", sans-serif; color: grey;}'
    #styling the heading
    html += 'h1 {font-size: 40px; color: white;}'
    #styling the table data
    html += 'td {text-align: center; font-size: 25px; font-family: "Georgia", sans-serif; color: grey;}'
    html += '</style>'
    html += '</head>'
    html += '<body>'
    html += body
    html += '</body>'
    html += '</html>'

    #returning the final HTML pages
    return html

#defining route for the root URL
@app.route('/')

#function for selecting genre
def select_genre():

	#building HTML content for genre selection page
	body = '<form method = "POST" action = "genre">'
	body += '<h1> Which genre would you like to watch? </h1>'
	body += '<table>'
	body += '<tr>'
	#creating image buttons for selecting between different genres
	body += '<th> <button type = "submit" name = "genre" value = "28">'
	body += '<img src="http://bit.ly/3uDXUxX" alt="Action" width="300" height="300">'
	body += '</button> </th>'
	body += '<th> <button type = "submit" name = "genre" value = "27">'
	body += '<img src="https://bit.ly/47SwKlg" alt="Horror" width="300" height="300">'
	body += '</button> </th>'
	body += '<th> <button type = "submit" name = "genre" value = "10749">'
	body += '<img src="https://bit.ly/3GFI3lj" alt="Romance" width="300" height="300">'
	body += '</button> </th>'
	body += '<th> <button type = "submit" name = "genre" value = "18">'
	body += '<img src="https://bit.ly/3uKf1hl" alt="Drama" width="300" height="300">'
	body += '</button> </th>'
	body += '</tr>'
	#creating text representation of the genres below the buttons
	body += '<tr>'
	body += '<td> Action </td>'
	body += '<td> Horror </td>'
	body += '<td> Romance </td>'
	body += '<td> Drama </td>'
	body += '</tr>'
	body += '</table>'
	body += '</form>'

	#returning the page with genre options
	return final_page_with_style(body, centered=True)

#defining route for the '/genre' URL with the POST method
@app.route('/genre', methods=['POST'])

#function for selecting type
def select_type():

	#retrieving genre info from form submission
	genre = request.form["genre"]

	if not genre:
		return "Genre not found in form submission."

	#building HTML content for type selection page
	body = '<form method = "POST" action = "recommend">'
	body += '<h1> Movie or TV Show? </h1>'
	body += '<table>'
	body += '<tr>'
	#creating image buttons for selecting between Movie and TV Show
	body += '<th> <button type = "submit" name = "type" value = "movie">'
	body += '<img src="https://bit.ly/3GmCA2v" alt="Movie" width="300" height="300">'
	body += '</button> </th>'
	body += '<th> <button type = "submit" name = "type" value = "tv_show">'
	body += '<img src="https://bit.ly/4a1nVrd" alt="TV Show" width="300" height="300">'
	body += '</button> </th>'
	body += '</tr>'
	#creating text representation of the options below the buttons
	body += '<tr>'
	body += '<td> Movie </td>'
	body += '<td> TV Show </td>'
	body += '</tr>'
	body += '</table>'
	body += f'<input type = "hidden" name = "genre" value = "{genre}">' 
	body += '</form>'

	#returning the page with type options
	return final_page_with_style(body, centered=True)

#defining route for the '/recommend' URL with the POST method
@app.route('/recommend', methods=['POST'])

#function to generate recommendation
def recommendation():
	
	#retrieving genre and type info from form submission
	genre_id = request.form["genre"]
	movie_or_tv = request.form["type"]
	discover = tmdb.Discover()

	if not genre_id or not movie_or_tv:
		return "Genre or type not found in the form submission."

	#initializing an empty body string
	body = ''

	#generating recommendation based on user's choice
	if movie_or_tv == "movie":

		#fetching movie details
  		movie_list = discover.movie(with_genres = genre_id, with_original_language='en')['results']
  		chosen_movie = random.choice(movie_list)
  		movie_id = chosen_movie['id']
  		movie = tmdb.Movies(movie_id)

  		#fetching overview
  		overview = chosen_movie['overview']

  		#fetching details of the movie's director
  		movie_credits = movie.credits()
  		director = "Director information not available"
  		crew = movie_credits['crew']
  		for person in crew:
  			if person['job'] == 'Director':
  				director = person['name']
  				break

  		#fetching details of the movie's cast
  		cast = movie_credits['cast'][:3]

  		#fetching trailers
  		video_results = movie.videos()['results']
  		if video_results:
  			trailer = video_results[0]
  			trailer_key = trailer['key'] 
  		else:
  			trailer_key = None

  		#fetching poster information
  		poster_path = chosen_movie['poster_path']
  		title = chosen_movie['title']
  		poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

  		#building HTML content for movie recommendation
  		body += '<h1> Your Movie Recommendation! </h1>'
  		body += '<table style="margin: auto;">'
  		body += '<tr>'
  		#left column for movie poster and title
  		body += '<td style="padding-right: 50px;">'
  		body += f'<img src="{poster_url}" width = "600px" alt="{title}">'
  		body += f'<p>{title}</p>'
  		body += '</td>'
  		#right column for embedded YouTube trailer
  		body += '<td>'
  		body += f'<iframe width="750" height="415" src="https://www.youtube.com/embed/{trailer_key}" frameborder="0" allowfullscreen style="margin-top: -460px;"></iframe>'
  		body += '</td>'
  		body += '</tr>'
  		#creating a movie details box
  		body += '<tr>'
  		body += '<td colspan = "2">'
  		body += '<div style = "width: 750px; height: 415px; border: 1px solid grey; background-color: black; color: grey; overflow: auto; margin-top: -500px; margin-bottom: 20px; margin-left: 650px; font-size: 20px; font-family: "Georgia", sans-serif;">'
  		body += f'<h2>Overview:</h2><p>{overview}</p>'
  		body += f'<h2>Director:</h2><p>{director}</p>'
  		body += '<h2>Cast:</h2>'
  		for actor in cast:
  			body += f'{actor["name"]} as {actor["character"]}<br>'
  		body += '</div>'
  		body += '</td>'
  		body += '</tr>'
  		#creating button for suggesting another movie
  		body += '<tr>'
  		body += '<td style="text-align: center; margin-top: 20px;" colspan = "2">'
  		body += '<form style="display: inline-block; margin-right: 10px;" method="POST" action="/recommend">'
  		body += '<button type="submit" name="suggest_again" value="movie">Suggest Again</button>'
  		body += f'<input type="hidden" name="genre" value="{genre_id}">'
  		body += f'<input type="hidden" name="type" value="movie">'
  		body += '</form>'
  		#creating button to go back to the genre selection
  		body += '<a href = "/"> <button>Go Back</button> </a>'
  		body += '</td>'
  		body += '</tr>'
  		body += '</table>'

	elif movie_or_tv == "tv_show":

		#changing genre id for TV shows
		tv_show_genre_id = ''
		if genre_id == '28':
			tv_show_genre_id = '10759'
		elif genre_id == '27':
			tv_show_genre_id = '10765'
		elif genre_id == '10749':
			tv_show_genre_id = '10749'
		else:
			tv_show_genre_id = '18'

		#fetching TV show details
		tv_show_list = discover.tv(with_genres = tv_show_genre_id, with_original_language='en')['results']
		chosen_show = random.choice(tv_show_list)
		show_id = chosen_show['id']
		tv_show = tmdb.TV(show_id)

		#fetching overview
		overview = chosen_show['overview']

		#fetching details of the TV show's director
		tv_show_credits = tv_show.credits()
		crew = tv_show_credits['crew']
		director = "Director information not available"
		for person in crew:
			if person['job'] == 'Director':
				director = person['name']
				break

		#fetching details of the TV show's cast
		cast = tv_show_credits['cast'][:3]

		#fetching trailers
		video_results = tv_show.videos()['results']
		if video_results:
			trailer = video_results[0]
			trailer_key = trailer['key'] 
		else:
			trailer_key = None

		#fetching poster information
		poster_path = chosen_show['poster_path']
		name = chosen_show['name']
		poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

		#building HTML content for TV show recommendation
		body += '<h1> Your TV Show recommendation! </h1>'
		body += '<table style="margin: auto;">'
		body += '<tr>'
		#left column for TV show poster and name
		body += '<td style="padding-right: 50px;">'
		body += f'<img src="{poster_url}" width = "600px" alt="{name}">'
		body += f'<p>{name}</p>'
		body += '</td>'
		#right column for embedded YouTube trailer
		body += '<td>'
		body += f'<iframe width="750" height="415" src="https://www.youtube.com/embed/{trailer_key}" frameborder="0" allowfullscreen style="margin-top: -460px;"></iframe>'
		body += '</td>'
		body += '</tr>'
		#creating a movie details box
		body += '<tr>'
		body += '<td colspan = "2">'
		body += '<div style = "width: 750px; height: 415px; border: 1px solid grey; background-color: black; color: grey; overflow: auto; margin-top: -500px; margin-bottom: 20px; margin-left: 650px; font-size: 20px; font-family: "Georgia", sans-serif;">'
		body += f'<h2>Overview:</h2><p>{overview}</p>'
		body += f'<h2>Director:</h2><p>{director}</p>'
		body += '<h2>Cast:</h2>'
		for actor in cast:
			body += f'{actor["name"]} as {actor["character"]}<br>'
		body += '</div>'
		body += '</td>'
		body += '</tr>'
		#creating button for suggesting another TV show
		body += '<tr>'
		body += '<td style="text-align: center; margin-top: 20px;" colspan = "2">'
		body += '<form style="display: inline-block; margin-right: 10px;" method="POST" action="/recommend">'
		body += '<button type="submit" name="suggest_again" value="tv_show">Suggest Again</button>'
		body += f'<input type="hidden" name="genre" value="{genre_id}">'
		body += f'<input type="hidden" name="type" value="tv_show">'
		body += '</form>'
		#creating button to go back to the genre selection
		body += '<a href = "/"> <button>Go Back</button> </a>'
		body += '</td>'
		body += '</tr>'
		body += '</table>'

	else:
		return "Invalid movie or TV show type selected."

	#returning the page with recommendation content
	return final_page_with_style(body, button=False)

#running the Flask webapp
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))