import selenium.webdriver as wd
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from collections import deque


# Function to scrape web pages and return the links, prioritizing navigation links
def scrape_web(start_url, max_pages=10, max_depth=2):
    print("Launching Chrome")
    driver_path = "./chromedriver.exe"
    options = wd.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for better performance
    
    driver = wd.Chrome(service=Service(driver_path), options=options)
    base_domain = urlparse(start_url).netloc
    
    visited_urls = set()
    queue = deque([(start_url, 0)])  # (url, depth)
    all_content = []

    try:
        while queue and len(visited_urls) < max_pages:
            current_url, depth = queue.popleft()
            
            if current_url in visited_urls or depth > max_depth:
                continue
                
            print(f"Scraping: {current_url} (Depth: {depth})")
            
            try:
                driver.get(current_url)
                html = driver.page_source
                visited_urls.add(current_url)
                
                # Extract content
                soup = BeautifulSoup(html, 'html.parser')
                content = {
                    'url': current_url,
                    'title': soup.title.string if soup.title else 'No title',
                    'content': clean_cont(str(soup.body)) if soup.body else ''
                }
                all_content.append(content)
                
                # Find new links if not at max depth
                if depth < max_depth:
                    links = extract_links(html)
                    for link in links:
                        # Here we are joining the link from ancor tab to base link so that we get a new page link
                        absolute_url = urljoin(current_url, link)
                        # Cheaking that the absolute url belongs to same domain
                        if is_valid_url(absolute_url, base_domain) and absolute_url not in visited_urls:
                            queue.append((absolute_url, depth + 1))
                
            except Exception as e:
                print(f"Error scraping {current_url}: {str(e)}")
                continue
                
    finally:
        driver.quit()
        
    return all_content



def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = []

    # First, extract all links from "Navigation Bar"
    nav_elements = soup.find_all('nav')
    for nav in nav_elements:
        nav_links = nav.find_all('a', href=True)
        for link in nav_links:
            url = link['href']
            if url and url not in links:
                links.append(url)

    # Extracting all links from the entire page
    all_links = soup.find_all('a', href=True)
    for link in all_links:
        url = link['href']
        if url and url not in links:
            links.append(url)

    return links


def extract_data_from_links(links):
    data = []
    for link in links:
        print(f"Visiting {link}")
        data.append(scrape_web_bs(link))
        time.sleep(2)
    return data


# Function to scrape data from each individual webpage (the body content)
def scrape_web_bs(web):
    driver_path = "./chromedriver.exe"

    options = wd.ChromeOptions()
    driver = wd.Chrome(service=Service(driver_path, options=options))

    try:
        driver.get(web)
        print(f"Page {web} loaded")
        html = driver.page_source

        # Extract the body content of the page
        soup = BeautifulSoup(html, 'html.parser')
        body_content = soup.body

        if body_content:
            return str(body_content)
        return "No body content found."

    finally:
        driver.quit()

# Function for cheaking if url is valid or not
def is_valid_url(url, base_domain):
    try:
        parsed = urlparse(url)
        return parsed.netloc == base_domain and bool(parsed.scheme)
    except:
        return False


def clean_cont(content):

    soup = BeautifulSoup(content, 'html.parser')
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    # Geting text from soup
    text = soup.get_text()
    # Remove extra whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text

#Spliting the data to chunks for paassing it to LLM
def split_dom_cont(content, max_chunk_size=8000):
    # Split content by page breaks
    pages = content.split("===PAGE BREAK===")
    
    chunks = []
    current_chunk = ""
    
    for page in pages:
        if len(current_chunk) + len(page) < max_chunk_size:
            current_chunk += page + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = page + "\n"

    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks



