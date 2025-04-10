# Analysing the UK Analyst Role: What Do Employers Want and What Do They Offer?

## Introduction
This repository contains the final project for BEE2041 Data Science in Economics. The project analyses the UK analyst job market in April 2025 using job listing data obtained from webscraping Reed.co.uk, exploring features such as the job skills, salary, locations, and employment types to provide insights for aspiring analysts. The findings are presented in blog.ipynb and formatted to blog.pdf using source/blog_format.py. Data procesing and analysis takes place in source/data_analysis.ipynb, with the visualisation plots saved to results/. The dataset was obtained using the script in source/scraping.py and saved to data/reed_uk_data_analyst_skills.csv.

## Repository overview

```
|-- data/
    |-- reed_uk_data_analyst_skills.csv
|-- results/
    |-- visualisation plots from source/data_analysis.ipynb
|-- source/
    |-- blog_format.py # Blog to pdf code (blog.ipynb to blog.pdf)
    |-- data_analysis.ipynb # Data processing, analysis, and visualisation code
    |-- scraping.py # Webscraping data collection code
|-- blog.ipynb # Blog source code
|-- blog.pdf # Formatted blog in pdf format
|-- README.md
|-- bee2041.yml # Anaconda environment
```

## Running instructions
1. This project was ran in an anaconda environment "bee2041.yml". To create an anaconda environment, ensure that "bee2041.yml" is in the path of your anaconda prompt command line and run the command "conda env create --file bee2041.yml", followed by "conda activate bee2041" to activate the environment. Additionally, ensure that a version of LaTeX is installed on your machine to run source/blog_format.py. The script was able to run using [MiKTeX](https://miktex.org/).
2. Run source/scraping.py to webscrape [Reed.co.uk](https://www.reed.co.uk/jobs/data-analyst-jobs-in-united-kingdom). The results are saved to data/reed_uk_data_analyst_skills.csv. Note that reed.co.uk allows webscraping - checked using https://www.reed.co.uk/robots.txt.
3. The data processing, cleaning, and analysis takes place in the notebook source/data_analysis.ipynb. Running this script will save the visualisation plots to results/.
4. Finally, running source/blog_format.py will format blog.ipynb into blog.pdf for readability.

## References
https://www.datacamp.com/blog/top-programming-languages-for-data-scientists-in-2022  
https://www.datacamp.com/blog/the-9-best-data-analytics-tools-for-data-analysts-in-2023
