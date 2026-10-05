# Web Scraping for Web Page's Adidas

This project has the goal getting the images from the Web Page of Adidas company.
Those images will be used for educational purposes, appling in real project the 
techniques for extrating data from the web
The URL of the webpage is https://www.adidas.com/us/shoes?grid=true

The packages for making the project that I've used are Selenium(API) and lxml
Programming Language used is Python

1. As is the public knowledge, the API-Selenium allow us interact with the web from a console using 
a programming laguage. The achitecture or structure to use it is in its documentation. So
   the structure of the project is similar to others.

2. The difference is how to apply and in which cases. For the present project, due to fact that the 
web page load only when we scrolldown on it, I used the method `execute_script()` to execute script of
JS `window.scrollTo()`.

3. Once the webpage have loaded, I could download it and using the lxml package with its method 
Xpath to find the `src` of `<img>`.

4. The final step is connecting with mongodb to save the images.
