*) To setup development environment:

Install virtualenv

From the root of the repository, create a virtual environment with:
	virtualenv oppian-env
	
Activate the environment:
	source oppian-env/bin/activate
	
Install required components:
	pip install --no-deps --requirement requirements.txt
	

*) To run server:
	
	./manage.py syncdb
	
	./manage.py runserver_plus localhost:8080
	