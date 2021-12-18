# review-cloud
Creating a word cloud from Letterboxd user reviews.

### The Nature of a Letterboxd Review

Letterboxd is my favorite way to track my movie data. That app has everything.

![image](https://c.tenor.com/LUUv0JDl6eUAAAAC/place-has-everything-bill-hader.gif)

I can rate, write reviews, track the movies I've seen, track the movies I want to see, and make and follow [lists that contain both *Get Out* and *Shrek 2*](https://letterboxd.com/ronniebites/list/films-where-the-main-character-visits-his/) for one wildly specific yet profoundly true reason.

![image](https://user-images.githubusercontent.com/95309435/146652911-96549606-39fd-456e-b73f-4ea7ab7bffe6.png)

Whenever I finish watching a movie, I log it on Letterboxd then proceed to read the reviews. 

A Letterboxd review section is great because it has a sort of social aspect to it. It creates an atmosphere of discussion. Sometimes one of the top reviews is just a funny one-liner that somehow perfectly encapsulates everything you felt and could ever feel about the movie you just saw. There's no pressure in a Letterboxd review to present a perfectly polished head to toe analysis of a movie's successes and failures, leading to a place where people can simply express their impressions. 

Occasionally, a person's impressions will be similar to another's. I thought a word cloud would be a great way to surmise what the greatest impressions were that a movie left on its viewers. Take this word cloud of reviews on the movie *Do The Right Thing* for example:

|![wordcloud](https://user-images.githubusercontent.com/95309435/146653298-3fe739fe-000c-4b25-95d0-230d82fa45d5.png)|
|:--:|
| <b>Image Mask: http://clipart-library.com/clip-art/fist-transparent-background-10.htm</b>|

At first glance I have a few takeaways from the impressions this movie left on people. I see the words "character" and "message" and immediately know the characters and the message of the film were strong to many of the viewers. I also see the words "still" and "today" which, from reading through reviews, I know is the result of a lot of people discussing how even today, the movie's climactic scene is still relevant (another word in the cloud). 

Here's another example that proves Heath Ledger's Joker was the best part of *The Dark Knight*. 

|![dark knight](https://user-images.githubusercontent.com/95309435/146657033-517253f6-2741-47ac-b083-31bf3b8fd15e.png)|
|:--:|
| <b>Image Mask: https://flyclipart.com/camera-clipart-png-action-png-491541</b>|


### Troubleshooting the Code

One issue I encountered while trying to compile the reviews so the text could be used in a word cloud was expanding the collapsed reviews. On the Letterboxd website if a review is too long, you can click the 'more' button to expand it, but trying to make sure the more button was clickable on each instance seemed overly complicated. Luckily, and I do mean luckily, each review has its own URL within the HTML. All that was necessary from this point was combining that portion of the URL with the Letterboxd domain then navigating to each review's individual site and pulling the text from this new all text page:

```python
	for review in reviews:
		review_body = review.find("div", class_="body-text -prose collapsible-text") 
		linksuffix = review_body['data-full-text-url'] # suffix of full text url to concat
		link = "https://letterboxd.com" + linksuffix
		reviewpage = requests.get(link) # set up new soup for link url
		reviewsoup = BeautifulSoup(reviewpage.content, "html.parser")
		reviews_list.append(reviewsoup.get_text()) # append to list just text from reviews
```

Another issue I had that I couldn't figure out for the life of me was how to keep clicking to the next page of reviews until it got to the end. Whatever I was doing just wasn't working but thankfully [this py4u thread came through](https://www.py4u.net/discuss/174082). With that issue out of the way I was able to get the URL for the new current page so the loop could proceed, and even make it to where I could set a maximum page number if I didn't want to go through every single page of reviews and only do the top 100 pages of the top reviews, for example. 
```python
	try:
		driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/div/section/section/div/div[2]/a"))))
		driver.find_element(By.XPATH, "//*[@id='content']/div/div/section/section/div/div[2]/a").click()
		URL = driver.current_url # switch to next page
		if pagenumber !='':
			if URL == f"https://letterboxd.com/film/{moviename}/reviews/by/activity/page/{maxpagenumber}/":
				print('Done')
				break
	except TimeoutException:
		print('Finished')
		break
```
