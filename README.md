# Football Players ETL

ETL pipeline to retrieve football matches statistics from [Sportradar](https://sportradar.com/)

### Setup

1. Register on [Sportradar Developer](https://developer.sportradar.com/member/register)
2. Create a [New Appication](https://developer.sportradar.com/apps/register)
   1. Select the option "Issue a new key for Soccer Extended Trial"
3. Get the generated key


### Running

Clone the repository
````bash
https://github.com/felipeall/football-players-etl.git
````

Access the app root folder
````bash
cd football-players-etl
````

Create a .env file
````bash
cp .env.example .env
````

In the .env file, fill `SPORTRADAR_API_KEY`  with the generated key
````
SPORTRADAR_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
````

Instantiate the Docker container
````bash
docker compose up -d --build
````

Access the Airflow UI
````
http://localhost:8080
````

Trigger the `football_players_etl` DAG with a season payload
````
{"seasons": ["sr:season:94215"]}
````
---
Available seasons:

| Competition    | Season | URN             |
|----------------|--------|-----------------|
| LaLiga         | 22/23  | sr:season:94215 |
| LaLiga         | 21/22  | sr:season:84048 |
| LaLiga         | 20/21  | sr:season:77361 |
| Premier League | 22/23  | sr:season:93741 |
| Premier League | 21/22  | sr:season:83706 |
| Premier League | 20/21  | sr:season:77179 |
| Serie A        | 22/23  | sr:season:94203 |
| Serie A        | 21/22  | sr:season:83944 |
| Serie A        | 20/21  | sr:season:77547 |
| Bundesliga     | 22/23  | sr:season:93753 |
| Bundesliga     | 21/22  | sr:season:83872 |
| Bundesliga     | 20/21  | sr:season:77189 |
