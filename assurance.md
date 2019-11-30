## Assurance
## Epic 1: Admins of the workspace - Administrate the workspace
As an admin, I want to promote workspace Admins from users so that they can help me manage the workspace.
* The button to set permission should be placed at the top.
* Types of permission, including members, owners, admins should be displayed and be able to select.
* The field to input the id of a user as to change its permission is needed
* User who is already an admin or owner can not be set as an admin or owner again.

## Epic 2: General Accessibility
As a user, I want to be able to register with email so that I can have my private account associated with my email address.
* The super link to go to  register is needed in log page with blue word ?Don't have an account? Register?
* The register form should contain email, password, name first, name last
* The email which has been registered cannot be registered again
* The email should be a valid email address
* The password should not be less than 8 characters
* The register user would receive a unique token and id
* The register user would be automatically login

As a user, I want to login with my credentials so that I can securely access my personal account.
* A login page should contain two placeholders to input email and password.
* If input email has not been registered, login page should return an error message saying bad request.
* If the password does not match the corresponding email, the login page should return an error message and fail login.
* The webpage should switch to user's personal slackr page after successfully login.

As a user, I want to be able to log out after login so that I can switch to another account or quit the website securely.
* The logout button should be placed at the top right corner.
* User's login token should be deactivated.
* After logout, the page should turn back to login page.


As a user, I want to be able to reset my password so that I can recover it once I forget.
* The superlink that goes to the reset password page should be placed under the login box.
* The superlink should written in a user-friendly message: Forgot password?
* The field to reset password should be placed at the centre of page.
* The field contains a placeholder with grey-color text:Email*
* The button with text 'send recovery email' is displayed below the placeholder.
* The placeholder displays once the user starts typing.
* The validation of email would be checked once click the button.
* If the input email has not been register page will raise error.
* Recovery email will be sent once pass the check of validation.
* The page will be turned to reset password page once pass the check of validation.


 
As a user, I want to view a list of all the channels in which I joined so that I can keep track of their updates.
* The channel list field should be displayed on the right of page.
* The channel list should contain all the public channels' name exist on slackr.


As a user, I want to be able to create a channel so that I can have a communication platform for a specific group of people. 
* The create button should be placed on the right of page and top of 'my channel' field with '+'' symbol.
* Show the create channel pop window right after clicking button.
* Provide option of public/private on the create channel window.
* Display a placeholder with grey text: Channel name on window.
* The text should disappear when start typing.
* A unique channel id should be generated after the successful creation of a channel.
* Channel name should be less than 20 characters.
* New channel?s name should be display on channel list.

As a user, I want to be able to join a channel so that I can receive information from a channel that I am interested in.
* The join button should be seen after clicking the channels? name on the right of page.
* The join button should have blue text: Join the channel with white background.
* Error would raise if user try to  join the private channel
* Channel's name should be displayed under the field of ?my channel?, after successfully join.
* Raise error if channel id is invalid.
* The channel would be displayed by date joined from newest to oldest.


As a user, I want to view other users' profiles so that I can learn more about them.
* Show the user's profile page by clicking their name

As a user, I want to be able to edit my profile so that other users can learn more about me.
* Show the user?s profile page by clicking their name.
* Users can change their name.
* Users can change their email.
* Users can change their handle.
* The placeholders display users? current information in grey.
* The texts display once start typing.
* Have a change button shaped like a pencil besides the each placeholder.
* After clicking the change button, user can enter new information.
* Have save/discard button beside placeholders after clicking change button.
* User can discard or save new changes by clicking save/discard button.
* Once click save or discard button, page will return to previous stage.
* Error would raise, if the new update is invalid.
* Once click the save button, the information will be updated.
* Once click the discard button, information will not be changed.

As a user, I want my default handle to be my first name and last name combined so that it will not be necessary for me to edit.
* The handle needs to be unique.
* The default handle is combination of first name and last.
* Add '1' behind the handle if the handle has been taken by other users.

As a user, I want to be able to search for messages by entering a key string so that I can find my required information quickly. 
* A search box should be provided within a channel.
* It will return all texts that match up with the target one.


## Epic3: Members in a channel - Communication
As a member, I want to be able to view the details of the channel so that I understand the purpose of the channel and know the people  involved in this channel.
* Provide a label under the name of the channel to allow users to view the details of the channel including the member list and description. 
* A symbol of a figure with plus on the left side should be displayed on the right side of the member?s name
* If the member is not the channel?s owner, a line should across through the symbol

As a member, I want to be able to invite people to a channel so that I can give that person access to the channel.
* Provide a button called invite people right under the name of the user which allow he/she to invite others to a channel.
* If the user one invited does not exist, one will receive a value error message saying the u_id one provides does not exist. 
* If the channel one invited others to join does not exist, one will receive a value error message saying the channel_id one provides does not exist.
* If a user that tends to invite others to the channel is itself not a member, the user will receive an access error saying he/she is not part of the channel. 
* Once a user has been invited successfully, the name of the user will immediately appear in the channel member list showing they have joined the channel successfully. 

As a member, I want to be able to leave a channel so that I can stop receiving information from a channel that I no longer interested in. 
* Provide a leave option right under the name of the user.
* If the member leaves the channel successfully, all the information of the channel will disappear on users? page, the name of the channel will be removed from the channel list.
* If the given channel id is invalid, then a value error message will show up saying the channel is invalid. 

As a member, I want to be able to see the messages that have been sent to the channel from other members so that I can keep myself updated. 
* Provide a textbox within a channel that reads in a number that indicates which line of message the user wants to read from as to let users view the messages that have been sent to the channel.
* Return up to 50 messages between index "start" (the integer user put down in the textbox) and "start + 50". 
* If the given channel id is invalid then a value error will be sent out saying the channel is invalid. 
* If the user is not in the channel yet, an access error will be sent out saying the user is not authorized to view messages in a channel that he/she is not in.
* If  the value that user put in is greater than the total number of messages in the channel, a value error will be sent. 
* If the channel that a user wants to send messages to does not exist, a value error will be shown saying invalid channel.  

As a member, I want to be able to send messages on the channel so that I can interact with other members. 
* Within the channel message area, provide a textbox where users can type messages in.
* Provide a send-out button which allows users to send out the messages they typed in. 
* For messages that have been sent out, they can be seen immediately on the channel, or can be searched later on. 
* If the message a user wants to send has length greater than 1000, an error message will be shown saying too many characters.
* If the message a user wants to send out is empty, an error message will be shown saying empty messages are not allowed.
* If the user is not in the channel yet, an access error will be sent out saying the user is not authorized to send messages in a channel that he/she is not in.
* If the channel that user wants to send messages to does not exist, a value error will be raised saying invalid channel. 

As a member, I want to be able to edit messages I sent on the channel so that I can fix any typos or inappropriate expressions.
* Provide a pen label at the right corner of each message that allows users (the user that sent out this particular message or an admin or an owner or the slackr) to edit.
* After editing, the message will be immediately updated.
* If a user that is not user who sent out the message or an admin, owner, slackr, an access error will be thrown saying the user does not have authority to edit this message.
 
As a member, I want to be able to pin messages so that important messages and their replies will be gathered on details pane for easy reference.
* Provide a pin method at the right corner of each message to allow users to pin  messages easily. 
* When a message is pinned, it will immediately be given special display treatment by the frontend.
* If the message has already been pinned, a value error will be thrown saying the message cannot be further pinned.
* If a user wants to pin a message in a channel that he/she is not in, an access value will be thrown saying user does not have permission to pin messages.
* If a user that is not an admin wants to pin a message, a value error will be thrown saying the user has no authority to pin a message. 
* If a user wants to pin a message with invalid message id, a value error will be thrown saying the message he/she wants to pin is not valid. 

As a member, I want to be able to unpin messages that were pinned to the channel in order to remove messages that are no longer important from the details pane
* Provide an unpin method at the right corner of each message to allow users unpin messages easily.
* When a message is unpinned, it will be immediately removed its special display treatment by the frontend
* If the message has already been unpinned, a value error will be thrown saying the message cannot be further unpinned.
* If a user wants to unpin a message in a channel that he/she is not in, an access value will be thrown saying user does not have permission to pin messages.
* If a user that is not an admin wants to unpin a message, a value error will be thrown saying the user has no authority to unpin a message. 
* If a user wants to unpin a message with invalid message id, a value error will be thrown saying the message he/she wants to pin is not valid. 

As a member, I want to be able to add emoji reactions to any messages being sent to the channel so that I do not need to send follow-up messages.
* Provide a thumb up label at the right corner of each message to allow users to react to messages.
* When a message was reacted, an emoji label will immediately appear under that message. 
* If the react id is not valid in the channel that the user is in, a value error will be shown saying reaction is not valid.
* If a user wants to react to a message that has already been reacted, a value error will be thrown saying the message can not be reacted again.  

As a member, I want to be able to remove a reaction that I've added so that I can respond to the message with another emoji reaction.
* Provide a thumb up label at the right corner of each message to allow users to unreact to messages.
* When a message was unreacted, an emoji label will immediately be removed under that message. 
* If the react id is not valid in the channel that the user is in, a value error will be shown saying reaction is not valid.
* If a user wants to unreact a message that has not already been reacted, a value error will be thrown saying the message can not be unreacted.  

As a member, I want to be able to delete messages I sent so that I can remove any mistakes in my message.
* Provide a bin label at the right corner of each message, therefore the user can remove messages by simply clicking on them.
* After removing a message, the message will immediately disappear in the channel message area and cannot be searched by others. 
* If a user wants to remove a message that no longer exists, a value error will be thrown warning that the user cannot remove a message that has already been deleted. 
* If the user is not an admin, an owner, a slackr or the user that sent this particular message but wants to remove a message, an access error will be thrown waring that the user does not have permission.

As a member, I want the system to help me send a message at a pre-set time so that I don't have to be online at that time.
* Provide a sendlater method within the textbox that user can type messages in.
* By clicking on the clock label and entering the sendlater time, the message that the user wants to send will be sent out at the exact time as the user set up before.
* If the message is over 1000, a value error will be thrown saying message has over 1000 characters.
* If the user tries to send a sendlater message to a channel that he/she is not in, an access error message will be thrown saying the user does not have permission. 
* If the channel that the user wants to send to is invalid(with invalid channel id), ab value error will be raised warning the user that the channel is invalid.
* If the time user set up is in the past, a value error will be thrown warning that one can not send out a message in the past.

As a member, I want to have a 15-mins' standup session within the channel so that we can hold a brief online meeting.
* A standup buttom should be placed at the left side of the channel name.
* The standup will be active after initiating the start button and all messages will be stored.
* If a standup is currently active and the user wants to initiate another standup, an value error will be thrown saying another standup is currently active. 
* If the user that wants to initiate a standup is not a member in the channel, an access error will be thrown saying the user does not have permission to start a standup.
* If the user wants to initiate a standup in a channel with invalid id, a value error will be thrown saying invalid channel. 


As a member, I want messages sent to the channel in a standup session to be collected and summarized by the system at the end of the session so that we do not have to gather information manually.
* The standup will be active after successfully clicking the start button.
* A new placeholder with text: standup message will be added to the button of channel field.
* After 15 mins starting the standup, the standup session will be closed.
* During the standup session, all the messages send in the standup field should be added to summary message with user?s handle and message.
* Right before the end of the standup session, summary message will be sent by user who start whih standup.


## Epic4: Owner of a channel 
As the owner of a channel, I want to be able to transfer ownership to another person so that I can enable another person to help me manage channel. 
* After clicking the figure button besides the member?s name with a line across, the member will be added to the channel?s owners.
* After clicking the figure button besides the member?s name without a line across, the member will be removed from the channel?s owners.
* Error would raise when the owner who is the only owner of channel try to remove himself/herself.
* Error would raise when the member who is not the owner of the channel  or owner/admin of slackr try to change ownership.

## Strategies: 
Most of functions will be tested by coverage with pytest  and frontend.

For example, the channel_create functions will be tested by pytest with coverage report that  make sure the branch coverage is one hundred percent. 
And also, it will be tested in frontend with simple set up data, to make sure the functions are working well with frontend.

But when come to some special functions related to time, the terminal may report runtime error if we need to wait for a couple of minutes to get the sernd_later message and “standup” summary message.
Therefore, to test send later functions, it is  easier to test with frontend.
And for the standup functions which has not corresponding frontend, it can only be tested using postman to check return finish time. And use terminal to catch the message_sent.

At the same time, the pylint is used to check the basic format of code.

Use error reported on terminal to catch the ValueError and description



