# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import re
import datetime as dt
import time


#################################################
# Windows
#################################################
# Set Executable Path & Initialize Chrome Browser
executable_path = {'executable_path': r'C:\Users\Muntz\Desktop\ChromeDriver\chromedriver.exe'}
browser = Browser("chrome", **executable_path)



# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Get First List Item & Wait Half a Second If Not Immediately Present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Parse Results HTML with BeautifulSoup
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the Latest News Title
        # Use Parent Element to Find First <a> Tag and Save it as news_title
        news_title = slide_element.find("div", class_="content_title").text

        news_paragraph = slide_element.find("div", class_="article_teaser_body").text
    except AttributeError:
        return None, None
    return news_title, news_paragraph



# NASA JPL (Jet Propulsion Laboratory) Site Web Scraper
def featured_image(browser):
    time.sleep(10)
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    # <button class="full_image">Full Image</button>
    browser.click_link_by_partial_text("FULL IMAGE")

    # Find "More Info" Button and Click It
    time.sleep(5)
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    time.sleep(5)
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    time.sleep(5)
    img = image_soup.select_one("figure.lede a img").get("src")
    time.sleep(5)

    img_url = f"https://www.jpl.nasa.gov{img}"
    return img_url



# Mars Weather Twitter Account Web Scraper
# Commented out as Twitter was giving server errors every time. 
# def twitter_weather(browser):
#     # Visit the Mars Weather Twitter Account
#     url = "https://twitter.com/marswxreport?lang=en"
#     browser.visit(url)
    
#     # Parse Results HTML with BeautifulSoup
#     html = browser.html
#     weather_soup = BeautifulSoup(html, "html.parser")
    
#     # Find a Tweet with the data-name `Mars Weather`
#     mars_weather = weather_soup.find_all("span",text=re.compile('InSight sol')).text
#     return mars_weather


# Mars Facts Web Scraper
def mars_facts():
    # Visit the Mars Facts Site Using Pandas to Read
    time.sleep(5)
    try:
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None
    mars_df.columns=["Description", "Value"]
    return mars_df.to_html(classes="table table-striped")


# Mars Hemispheres Web Scraper
def hemisphere(browser):
    # Visit the USGS Astrogeology Science Center Site
    time.sleep(5)
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    time.sleep(5)
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        time.sleep(5)
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        time.sleep(5)
        browser.back()
    return hemisphere_image_urls

#################################################
# Main Web Scraping Bot
#################################################
def scrape_all():
    executable_path = {'executable_path': r'C:\Users\Muntz\Desktop\ChromeDriver\chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    # mars_weather = twitter_weather(browser)
    facts = mars_facts()
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        # "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())