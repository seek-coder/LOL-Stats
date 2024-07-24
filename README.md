# LOL Stats Query Web-App (LAS region)
![imagen](https://github.com/user-attachments/assets/a9e4cd27-e5a7-4110-887b-d66b1e5816ac)

Web-App for League of Legends data queries, made by Leonardo Carabajal (Math teacher and Data Science student) and Catriel Gatto (Philosophy teacher and Computer's Science student). Its purpose is merely educational and instructive and we have NO intention on recieve any profit for it.

## Pre-requisites
Firstly, being in the root path, you'll have to install the dependencies from a terminal:
```
pip install requirements.txt
```

Secondly, to run this app, you'll need to add a personal API KEY from Riot's website. For this, you can write on the terminal (replace 'yourapikey' with yours):
```
echo "API_KEY=yourapikey" > web/statsgraph_web/statgraphs/.env
```
Then, be sure to be in the manage.py folder. You can simply run:
```
cd web/statsgraph_web/
```

In this path, just run:
```
python manage.py runserver
```

And if everything was done right, you'll now have access to the website that is located in localhost:8000

The website is in spanish. English version will be added soon. 

## Summary of functions
This app searches data from a LAS summoner (AMERICA) and returns info from the last 30 matches:

* Level
* Icon
* Total winrate
* Winrate per side
* Total playtime
* KDA
* a matplotlib's graph for total wins per day
* a matplotlib's graph for total wins per hour

Checkout our info in the 'About Us' section ;)!
