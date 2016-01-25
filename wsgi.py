from app import app

app.secret_key="lolsup"
if __name__=="__main__":
	#app.secret_key="lolsup"
	app.debug=True
	app.run()


