# Reviewed by Daan Moll

In general, Daan thought it was clear how the code was written and how it worked. The api / database request were a bit longer in comparison to his and he used more javascript for things that I would implement with python/html (like required for radiolabel or the error messages).

1. When the initializing mollie api (top of application.py), the api key is hard coded but it is better to do this as an environmental key to ensure that people cannot take advantage of the key. I think I didn't think of implementing it like that because this is a test api but indeed I should always use environmental keys when using an api.

2. On line 139 of application.py, it says: book not found (yes, I copied that piece from books ;) and of course it should be movie not found.

3. I could use more javascript for specific messages. So instead of rendering the error.html I could use a javascript alert, this would make my code also more compact because I use it could a few times (and I would have used javascript a bit more ;).

4. The a movie can become an 'alreadywatched' movie (through the button) but it can't be undone (remove from the database). This is something that would make it more user-friendly and I just didn't think about that.