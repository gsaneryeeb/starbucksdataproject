### Starbucks Stores Spider：

You can get detailed data of all Starbucks Store in China and save them to the MongoDB database.

**Run**

* Install MongoDB

* Configure db.conf 

* The sock5 agent is enabled by default. To disable it, modify the following section in the user_agents.py file
  ```
  ip_proxy = {
      'http': 'socks5://127.0.0.1:1080',
      'https': 'socks5://127.0.0.1:1080'
      }
  ```

  Change into

  ```
  ip_proxy = {}
  ```

* pip install -r requirements.txt 安装Python依赖

* python starbuck.py

Output csv file
* python stabuckscsv.py 


**Implementation process**

- Starbucks China offical Website：

> <https://www.starbucks.com.cn/stores/?features=&bounds=115.490644%2C39.670253%2C117.231978%2C40.221932>

The official website of Starbucks (China) provides us with the function of querying stores, and then we use this function to capture the number of Starbucks stores in China.

First, get the Starbucks store query API through analysis of developer tools as follows:

> <https://www.starbucks.com.cn/api/stores/nearby?lat=39.904989&lon=116.405285&limit=1000&locale=ZH&features=&radius=100000>

Further analysis revealed that: Starbucks official website uses Gaode map to store geographic information. The query rule of a city store is to specify the latitude and longitude of the target city center, and query the number of stores within 100 kilometers of the target area. So use the following algorithm to get the number of Starbucks stores.

-step 1: Grab the Starbucks store information query API and analyze the API construction rules. The Starbucks store query API is obtained through developer tool traffic analysis, and the API string is analyzed. It is known that Starbucks official website uses Gaode map to store geographic information. The query rule of a city store is to specify the latitude and longitude of the target city center, and query the target area within 100 kilometers The number of stores within.
-step 2: Use Gaode map geo / inverse geocoding function to get city latitude and longitude coordinates by city name. Register for the Gaode Open Platform and become a Gaode Map developer. Query the development documents provided by Gaode Map using Gaode Map geo / inverse geocoding function to obtain the city latitude and longitude coordinates by city name.
-step 3: Use Baidu city and code comparison table to extract all cities in China, use step2 method to obtain its latitude and longitude, construct api-url to get store information and save it to MongoDB

