# Telegraph Data Engineer Exercise

### Description

This repo contains an ETL pipeline that can be used to find out the top 3 Telegraph articles which lead to users registering on the website. The pipeline extracts data from the hitlog csv file that contains data of pages visited by users, transforms the data to find the three most influential articles, and outputs the final data as a csv file.

The repo contains the following files:

- ``src/extract.py`` - A python script to read the data.<br>
- ``src/transform.py`` - A python script to transform the data to find the three most influential articles.<br>
- ``src/load.py`` - A python script to write the final output to a csv file.<br>
- ``main.py`` - A python script to execute the ETL process using the functions from extract.py, transform.py, and load.py<br>
- ``requirements.txt`` - A list of the required python libraries.<br>
- ``tests.py`` - A python script for unit testing.<br>
- ``notes.md`` - Some notes on logic and assumptions made about the input file.<br>
- ``hitlog.csv`` - A csv file with fake data of pages visited for several users.<br>
- ``totals.csv`` - A csv file that is the output of the ETL pipeline.<br>


### Instructions

- Ensure python3 is installed. Install required libraries by running the following in the terminal.

``` bash
  pip3 install -r requirements.txt
```

- Download the repository and set working directory to where the project is saved

- Run the pipleline by running the following in the terminal. 

```bash
  python3 main.py
```

- For testing run the following in the terminal.

```bash
  pytest -v -s tests.py 
```


