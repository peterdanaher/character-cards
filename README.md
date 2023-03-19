This code should be executed on VS Code.
You can start by typing "cd final_project" into the terminal and hitting the enter key.
Once that has succeeded, you must type "flask run" into the terminal and hit the enter key.
Provided that goes well, a link should appear in the terminal. Command click that link to access the website.

You will start on the login page. You can go to the top right on the navbar to find the register link.
Create your username and password and hit submit. If you mess up along the way, you will get taken to a
page with an apology message and a link back to the registration page.

After your account is created, you will be taken to the login page where you can type in your accound credentials.
Once you log in, you will be taken to the index. Once at the index, you can use the navbar to see the different parts of the website.

A good place to start would be the set difficulty page. Every user starts off on easy difficulty. You can change it
to either medium or hard. Depending on your difficulty, you will be shown a different amount of new words and you will
have to review a different amount of words. The difficulties easy, medium, and hard correspond to the levels 5, 7, and 10, respectively. When you learn new words, you will be shown the number corresponding to your level. For example,
a user on medium difficulty will be shown 7 new words. When it comes time to review, you will have to review 5 plus your level characters. E.g. a user on easy difficulty will have to review 10 new words (5 + 5).

You currently have learned zero words so it would be advised that you learn some new words. For this you can either
go to the review page or to the learn new words page. Since you have zero words learned, the review page will redirect you to the learn new words page automatically.

In the learn new words page, you will be shown the character, pronunciation, and meaning for each word. You can click
"Next Character" to move onto the next one. Once you run out of characters, a button to return to the index will appear. Note that you need to hit this button for the website to record that you have learned these new words. Otherwise, the website will act as if you have not read the whole list and so it does not record it.

Once you have learned new words, the website initializes some notes for the characters you have learned. These notes are specific to your account. The text in the note is initialized as NULL, but you can go to the add notes page to edit the text in the notes. You must first search for the character you would like to edit. You can either search by meaning or if you know hov to type in Chinese characters, you can search by character. If your query is invalid or there are no results, you will be sent to an apology page with a message explaining what went wrong and a link to return to the add notes page. If the search goes through and a character is found, you will be shown the flashcard for the character, along with a field to add your new note. You can hit add note and this text will be added to your note in the database.

After you've written some notes, you can go to the review page to check them out. The review page shows you a character and there is a text box to quiz you on its meaning. You can hit "Check Answer" to check your answer and to reveal the pronunciation, meaning, and note for the character. You can hit "Next Character" to move on to the next one and repeat this process until you have run out of characters. Note that once there are no more characters, you must hit check answer and this will reveal the button to go back to the index page. Or if you wish to not look for the button, you can always click the "Character Cards" logo to go back to the index.

In addition to these functionalities, there are a few more basic ones. You can go to the log out page to clear your session data. You can also go to the change password page to change your passwords. For this you need to provide your old password as well as a new one. Then it will change your password in the database, log you out, and bring you to the login page.