Description:
	The project was aimed at building a prototype of Google Maps for showing shortest path from BITS Hyderabad to RGIA Airport using A Star Algorithm using different map APIs and finally displaying the path on map.

Project Tech / API-Stack:
	1) Python3
	2) pipenv - for package management
	3) gmplot - for plotting on google maps
	4) BING Maps API - For fetching the distance matrix
	5) HERE Maps API - For fetching nodes and building underlying map
	6) flexpolyline - For encoding / decoding HERE maps response and paths

Setting up project:
	(every command should run in project's root directory)

	1) $ pip3 install pipenv
	2) $ pipenv install
	3) $ pipenv shell
	4) $ python3 main-online.py
	5) Now the final output map in saved in "my_map.html", open it in any browser

	NOTE: main-online.py executes every API call on the go, and doesn't use any storing of data. where as main-using-database.py uses the prevously stored data in binary files to generate the final path.


Results / Screenshots:
	Screenshots of different results is stored in plots/ folder.

Heuristics:
	Three different heuristics are used and results are recorded in plots/ folder.

	1) Distance Matrix from BING
	2) Duration Matrix from BING
	3) Straight line distance between points

Note:
	1) There are total of approx. 8000+ nodes to get complete path on roads only.
	2) We took an assumption that roads are unidirectional (but it doesn't matter as A start will move forward only)