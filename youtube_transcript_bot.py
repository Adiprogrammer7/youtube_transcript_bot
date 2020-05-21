from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

PATH = 'C:\Program Files (x86)\chromedriver.exe'  #provide path to chromedriver.exe here.

class TranscriptBot:
	def __init__(self, video_link):
		self.driver = webdriver.Chrome(PATH)
		self.video_link = video_link
		self.transcript_text = ''
		self.title = ''
		self.channel_name = ''

	def get_transcript(self):
		self.driver.get(self.video_link)
		try:
			opt_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body/ytd-app/div[@id='content']/ytd-page-manager[@id='page-manager']/ytd-watch-flexy[@class='style-scope ytd-page-manager hide-skeleton']/div[@id='columns']/div[@id='primary']/div[@id='primary-inner']/div[@id='info']/div[@id='info-contents']/ytd-video-primary-info-renderer[@class='style-scope ytd-watch-flexy']/div[@id='container']/div[@id='info']/div[@id='menu-container']/div[@id='menu']/ytd-menu-renderer[@class='style-scope ytd-video-primary-info-renderer']/yt-icon-button[@id='button']/button[1]")))
			opt_btn.click()
			transcript_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-popup-container.style-scope.ytd-app:nth-child(13) iron-dropdown.style-scope.ytd-popup-container:nth-child(1) div.style-scope.iron-dropdown ytd-menu-popup-renderer.style-scope.ytd-popup-container paper-listbox.style-scope.ytd-menu-popup-renderer:nth-child(1) > ytd-menu-service-item-renderer.style-scope.ytd-menu-popup-renderer:nth-child(2)")))
			transcript_btn.click()
			# to toggle timestamp
			sleep(2)
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ytd-menu-renderer[@class='style-scope ytd-engagement-panel-title-header-renderer']//button[@id='button']"))).click()
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//ytd-menu-service-item-renderer[@class='style-scope ytd-menu-popup-renderer']"))).click()

			self.transcript_text = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-transcript-body-renderer"))).text
			self.title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[@class='title style-scope ytd-video-primary-info-renderer']"))).text
			self.channel_name = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='upload-info']//yt-formatted-string[@id='text']"))).text
		finally:
			self.driver.quit()

	def transcript_to_txt(self):
		filename = f'{self.channel_name} [{self.title}].txt'

		# removing character from filename which cannat be used in file naming conventions.
		bad_chars = ['<', '>', '*', '?', '/', '|', '"', ':'] #problemetic with '\' as its escape character in python.
		for char in bad_chars:
			filename = filename.replace(char, ' ')

		filepath = os.path.join('transcripted_txt_files', filename)
		with open(filepath, 'w') as file:
			file.write(self.transcript_text)
		print("{} done!".format(filename))


def main(video_link): 
	blob = TranscriptBot(video_link)
	blob.get_transcript()
	blob.transcript_to_txt()

main('https://www.youtube.com/watch?v=XQ0XQNCfRnc')  #provide the youtube video url here.