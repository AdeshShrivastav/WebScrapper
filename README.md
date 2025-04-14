# Web Scraper Project

This project is a web scraper that extracts content from web pages using Selenium and BeautifulSoup, and then parses the content using a language model.

## Requirements

*   Python 3.6+
*   Selenium
*   BeautifulSoup4
*   Langchain
*   Ollama
*   streamlit

## Installation

1.  Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

2.  Download and install Ollama from [https://ollama.com/](https://ollama.com/).

3.  Pull the `llama3.2` model:

    ```bash
    ollama pull llama3.2
    ```

## How it Works

This web scraper works by following these steps:

1.  The user enters a website URL in the Streamlit app.
2.  The scraper uses Selenium to load the web page and extract the HTML content.
3.  The scraper uses BeautifulSoup to parse the HTML content and extract the desired data.
4.  The scraper follows links on the page to scrape additional pages, up to a specified maximum depth and number of pages.
5.  The scraped data is displayed in the Streamlit app.
6.  The user can then use a language model to parse the scraped data to extract specific information.

## Usage

1.  Run the main script:

    ```bash
    streamlit run main.py
    ```

2.  Enter the website URL in the text input field.
3.  Specify the maximum number of pages to scrape and the maximum depth to scrape in a page.
4.  Click the "Scrape Web Data" button.
5.  If you want to parse the scraped data, describe what you want to parse in the text area and click the "Parse Content" button.

## Notes

*   This project uses Selenium, so you need to have a compatible ChromeDriver executable in the same directory as the script. The `chromedriver.exe` file is included in this repository.
*   The language model parsing is done using Ollama. Make sure Ollama is installed and running before using the parsing functionality.
