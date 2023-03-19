As a preface, please note that I used my finance pset as a base for the structure of my website. This let me save a lot of time because I did not have to recode common features like login and change password.

This website is based on the SQL database characters.db. This database consists of three tables: characters, users, and notes. Characters contains all the characters used by the website for the cards. Users contains information about the registered users of the website. Notes contains notes that the individual users can edit and they are attached to their respective character pool. Below I will write a summary of the tables and their columns.

characters {
    id INTEGER NOT NULL PRIMARY KEY
    character VARCHAR (Chinese character)
    pronunciation VARCHAR NOT NULL (Pinyin)
    meaning TEXT NOT NULL
}

users {
    id INTEGER NOT NULL PRIMARY KEY
    username TEXT NOT NULL
    hash TEXT NOT NULL (password hash)
    number_seen INTEGER DEFAULT 0
    difficulty INTEGER DEFAULT 5
}

notes {
    note ID INTEGER NOT NULL PRIMARY KEY
    note TEXT
    character_id INTEGER NOT NULL FOREIGN KEY REFERENCES characters.id
    user_id INTEGER NOT NULL FOREIGN KEY REFERENCES users.id
}

Most of this is self-explanatory, but there are a couple of important things to note. First is that number_seen counts the number of characters that a user has seen and this starts at 0. This number will be updated when the user learns new words. The second thing to note is that the difficulty is an integer starting at the value 5. This will be done to make math easier later because the difficulty will represent how many characters we add to an learn or review session. Easy corresponds to 5, medium to 7, and hard to 10.

The user starts with registration. This process is the same as the finance pset. On a get request the website renders the registration template which contains 3 forms. One for username, one for password, and one to confirm password. If any of these are empty on a submission, an apology page will be displayed. This is done by calling the apology helper function in helpers.py. This function takes a message and the origin directory. Then it prints the apology page with the message and a button that links to the origin directory. In this case, the button links you back to /register. If you fill in all the fields and submit, flask will check if the username you created already exists in the users table. If it does, you get an apology to make a new username. If it doesn't your account is made and you are redirected to the login page.

At the login page you can login with your new account and be taken to the index. I made a navbar with all the different pages on the site. There is a link to the index on the Characters Cards logo, the rest of the links take you to the pages described by their text.

The change difficulty site consists of a select menu form. On a get requests, we check the user's difficulty setting in the database and use that as the default value in the database. Then the two other difficulty options are added to the select menu. You can choose a difficulty level and hit submit and on the post request, the site will update the users database to change your difficulty level to the one you chose.

If you have zero words learned and you hit review, you will get redirected to the learn new words page. Otherwise, you will have to review a number of words equal to 5 plus your difficulty level (or if your number_seen is less than that you will be shown all you words you've seen). This list is random. The character list is passed into render_template so that Javascript and Jinja could access the character data. The page will start by showing you a character and testing you on the meaning through a text input. You can hit check answer and it will take your input and check it with the meaning of the character in the database. If it is right the input will turn green, red otherwise. Then the pronunciation, meaning, and your note for the character are revealed. If you have no note, the note will say none. You can then hit next character, and it will go to the next character in the sequence, rehide the information and update it for the current character, and then you can be quizzed again. This goes until you check your answer on the last character and it reveals a button to go back to the index. I used Javascript to make the buttons work. I added an event listener for clicks to both buttons and then a function goes off to either reveal information or change to the next character. This is how I did all my other buttons as well.

The learn characters site on a get requests finds your difficult level and the number of characters you have seen. If your number seen is equal to the amount of characters in the database, you are redirected to the review page. If not, the site finds a number of new characters equal to your difficulty level (if there are less new characters than your difficulty level, you are simply shown the rest of the list and no more). You are shown the character, the meaning, and the pronunciation. If you hit next character, the information is changed to the subsequent character on the list. This goes until you run out of characters and a return home button is revealed. If you hit this button it will update your number seen by the number of new characters you just saw. Then it will create a blank not for each character you just saw, tied to your user id.

The add notes page on a get request gives you a form where you can type your query and choose what you'd like to search for. You can either search for the meaning of a character in English or you can type the character in Chinese and change the drop down menu to character instead. Then you can submit a post request to the website with your query. If the search field is empty, you will get an apology. If it is not, it will search through the database for a matching character. It will then pass this character to "add_note.html" and it will print the characer, meaning, and pronunciation. There will be a form on the bottom where you can write the note you would like to add and then you hit submit. This post request updates the notes table to add that text to the note correspanding to that character id and your user id.

The logout link works just like in finance where it clears the session and redirects you to login.

The change password also works just like in finance. It has a form with old password, new password, and confirm password. It checks to make sure none of the fields are empty, the old password is correct, and the new passwords match. The user table is then updated with your new password and you are redirected to login.