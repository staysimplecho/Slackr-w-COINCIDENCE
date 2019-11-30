# Software engineering principles:

## KISS:
- Software design principle tightly bonds with the concepts ***DRY*** and ***KISS***. In order to follow the given principle, we introduced a new file named `all_deco.py` which contains all of the decorators we created to simplify the codes' complexity. 
In the file `all_deco.py`, we constructed 12 decorators. They are mainly used to check the conditions or edge cases for functions, in order to ensure the correctness of *verification* (eg.check_valid_token) and *validation*(eg.check_name_length). Additionally,  we noticed that the function `get_user_from_token` which returns a user's information by decoding a given token is most frequently used among all the helper functions we have constructed before. Therefore we decided to alter it into a decorator for a more simplified version of code. 

## DRY:
- Similarly, in order to follow ***DRY*** and ***KISS*** principles, we added more helper functions in the file `iter3.py`. For example, the function `is_user` returns either true/false determining whether a user with a valid token is inside the database / has registered or not. Helper functions can also be found inside classes. Some of the abilities are frequently used only for a section of functions, hence they were all directly added to a class to make the code more readable and usable. For instance, in the class NewMessage, a function (method) named `def edit(self, new)` can directly help to change the original message to a new one without reaccessing the stored data.

## DESIGN SMELL
- Another aspect of software engineering principle is called ***DESIGN SMELL***. It includes 8 terminologies which intend to make the code *reusable*, *maintainable*, *understandable* and *testable*. During the implementation, we regularly checked with the list, and ensured we tried our best to stick with the requirements. As we mentioned above, *NEEDLESS COMPLEXITY* and *NEEDLESS REPETITION* are solved by adding decorators and helper functions. *RIGIDITY*, *IMMOBILITY*, and *OPACITY* are improved by renaming variables and adding comments as well as breaking complicated functions into several individual ones. *VISCOSITY* is solved in subtle details, an example would be reducing the timmer time while testing. *FRAGILITY* and *COUPLING* are on the other hand solved by holding face-to-face team meetings. Efficient communication, regular updates and team collaboration ensures the interdependence between components being maintained, as well as reduces the tendency for software to break when a single change is made. In addition, they are also improved by separating a huge collection of functions into different clearly-named files according to their usage, which reduces the effort for debugging. 

## SINGLE RESPONSIBILITY
- ***Single responsibility principle*** is also highlighted. We followed the principle in both micro and macro ways. Microly, this principle is applied to class.  Most of the methods that have been included in class only has one responsibility (eg. `class NewMessages` - `edit` - changing the old message to the new one). Macroly, every file mainly has only one responsibility as well. The file `proj_server.py` is only responsible for working with frontend; `all_decos.py` only contains decorators; `new_profile.py` only takes charge of editing/renewing profiles; `auth_register_test.py` only tests for one function auth_register. By following single responsibility principle, issues such as allocating tasks, debugging, multiple people working together, increasing codes' readability became easier to solve, which is a significant reason of obeying software engineering principles. 

## ENCAPSULATION
- The concept of ***ENCAPSULATION*** were also emphasised during iteration 3. In order to maintain the type abstraction, we mainly used the data type class for data storing.  It helps us to restrict direct access to internal representation of types, abstract functionalities, which assists in an easy construction of related functions as well as leave spaces for further changes. For example,  in the given task we are asked to include a functionality which allows members in a channel to add other members to this channel. Within the `class Channel` we have attributes `self.channel_id`, `self.owner`, `self.members` etc. We then  constructed a method called `def add_member` which only does one thing - appending a member. When this functionality being called, we do not have to access to internal representation, but instead can just call the method, which promotes software engineering principles along the way. 


## By implementing the ***top-down*** engineering thinking, we provide a general outlook of the steps we took to follow software engineering principles: 
## (this is not sorted chronologically)

- a.  The way to store member and owner lists are changed from dict `u_id`, `name`, `img_url` to only `u_id` as other information is changeable. This reduces the *fragility* of code, improves the *design smell*. In addition, instead of using a static dictionary to store and update the channel member list, `channel_detail` function takes care of it appending new members to the current list and return the latest version. This reduces *needless complexity* by getting rid of a data storage method. 

- b.  Add decorators -check for valid token. This decorator is needed by most of the functions. This allows us to follow the *DRY* and *KISS* principles.

- c.  Change the arguments that functions take in to correspond to the addition of decorators. By correctly using key arguments and positional arguments, the aspects of *design smell* -- *fragility* and *compile* are improved.

- d.  Add more details and overall comments to tests to make it more understandable to others which helps to improve the *design smell*.

- e.  Move the scattered helper functions that have been built in each individual function file(espcially `server.py`)  into `iter3.py` as shared functions to make them *reusable*. This helps with *DRY* and *design smell*.

- f.  Change tests to avoid testing the same aspects repeatedly, which follows the *DRY* principle.

- g.  Change all magic numbers (etc all kinds of invalid input) to named constants or variables, as to make the code *understandable* and reduce *needless repetition*.

- h.  Reduce the length of time when testing `standup` and `message_sendlater` function for *viscosity*.

- i.  Separate functions to limited and clear named files according to their usage on slackr, strictly follows the *single responsibility principle*.


