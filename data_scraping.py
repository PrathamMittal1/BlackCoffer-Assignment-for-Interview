from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class DataScrapper:
    def __init__(self):                          # constructor initializing the selenium driver for chrome
        options = Options()
        options.add_argument('--headless=new')
        service = Service(executable_path='chromedriver-win64/chromedriver.exe')
        self.__driver = webdriver.Chrome(options=options, service=service)

    @staticmethod
    def __saveToFile(url_id, text):                  # method for saving the extracted text in local storage
        with open('DataFiles/' + url_id + '.txt', 'w', encoding="utf-8") as f:
            f.write(text)

    def scrap(self, url_id, url):                # scraping the interested text part from the webpage
        self.__driver.get(url)
        title = self.__driver.find_element(By.XPATH, '/html/body/div[6]/article/div[1]/div['
                                                     '1]/div[2]/div[2]/header/h1').text
        article_text = self.__driver.find_element(By.CLASS_NAME, 'td-post-content.tagdiv-type').text
        final_text = title + '\n\n' + article_text
        self.__saveToFile(url_id, final_text)      # calling method to save the extracted text data
        return url_id, final_text


# if __name__ == '__main__':
#     obj = DataScrapper()
#     obj.scrap('Netclan20241017',
#               'https://insights.blackcoffer.com/ai-and-ml-based-youtube-analytics-and-content-creation-tool-for'
#               '-optimizing-subscriber-engagement-and-content-strategy/')
#     obj.scrap('Netclan20241028','https://insights.blackcoffer.com/securing-sensitive-financial-data-with-privacy-preserving-machine-learning-for-predictive-analytics/')

