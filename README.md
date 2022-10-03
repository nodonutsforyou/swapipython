# Small Python framework to test https://swapi.dev/documentation API
---
I'm not sure what specifically happened, but the first email to me with this assignment got lost. So I've received this assignment only today. And HR have asked me to complete it as soon as possible. I had only one evening to work on it, so please make a discount for that if I missed something.

## What I have done
I've created a small Python framework, using pytest and requests libraries. To run the test you can simply run:
```
pip install -r requirements.txt
pytest
```
There would be some failed tests, but this is expected.
Alternativly, I've added a docker image to run the suite. More details bellow.
 #### Task 1
```
 Before you start, to validate the request itself, we would like to see a test suite that hits all the possible endpoints.
```
 Implemented in `test_all_endpoints.py` file
 I used https://swapi.dev/api/ call to get the list of all the endpoints. The python code parses the result to create a parameter list for a test. Test itself does nothing other than simply checking response codes. 
Documentation for the API has info that there should be a schema endpoint. I thought there should be a nice way to get a json schema call, so i could test every single reply with the provided schema. But somehow all the /schema/ endpoint returns 404 codes. I've tried to find references to this call in the provided CLI, but they have no references to it whatsoever. I assume this is a bug, so I have failed tests here.
 #### Task 2
 ```
 We want to will take a subset of these APIs, namely the People API, and we will write actual
tests for it (see “People” Section: https://swapi.dev/documentation#people). You will find
the requirements on the response on the websites (See “Attributes”).
For example, we want to validate if the name of the response is never empty.
HINT: Don’t think about valid input only.
```
Implemented in `test_people.py` file
I did an extensive test over pagination. As positive tests and also negative scenarios. I've added a simple positive test with checking if the required fields are present, but I'm not sure what the requirements for the types of the fields are. Also there are some negative tests for the `/people/:id/` endpoint. And `/people/schema/` test, which is always failing
#### Task 3
```
Write a test that:
• fails if the person has no hair color (i.e. hair color is n/a)
• fails if a person has no gender (i.e. gender is unknown or n/a)
• fails if the person has not piloted a vehicle
```
Implemented in `test_people.py/test_hair_color_gender_vehicles`
Not only it fails for those conditions, it has an informative error message. For example if R2D2 fails on all 3 conditions, the error message would contain all 3 failed conditions, not only the first one.
#### Task 4
```
Write a test that find All Details about the home world, films, vehicles, and starships for Luke
Skywalker assuming you only know the name “Luke Skywalker”.
```
Implemented in `test_search.py` file
Does the simple search call, and checks all the calls in the results. Checks the response codes of all the calls, and checks that there is only 1 search result in the response. Does not make any additional checks.
#### Task 5
```
Provide a README file to explain what you have done and how we can run the tests ourselves.
```
Implemented in `README.md` file, you are reading it at the moment


### Additional things I've added
Just as quick addition, i've addded a docker image, so you can run it in VM.
Do build image, you should start `run_in_docker.sh`
After that, you can start the suite by running the image:
```
docker run swapi
	
```

