## Assume that
1. All the functions being tested can be runned and works correctly.
2. Slackr admins and owner can add/remove the channel owners.
3. Admins and owners of the Slackr cannot modify their own permissions.
4. Slackr allows multiple owners and admins, they can be modified by other owners or admins.
5. A member of a channel can be an owner of the slackr.
6. Slackr owner, Slackr admin, Slackr member, channel owner and channel member will have permission id from 1 to 5 respectively.
7. `ValueErr` will raise if an invalid token is detected for all functions, while the implementation of detection is not yet able to carry out in this stage.
8. Apart from the dummy functions,  
   every registered user has a unique `u_id`,  
   every single message has a unique `message_id`,  
   every channel has a unique `channel_id`,
   ID will never change unless its related user/message/channel has been deleted.       
9. A `token` contains information that is subject to any actions a logged-in user took, and it can somehow reflects the user's id, such that it's always unique.
10. `messages` is a valid data type that stores all messages sent in the Slackr.
11. If the passed-in parameters would raise two types of errors, the `AccessError` should come first while the `ValueErr` can be neglected.

## Authentication
1. Assume that the actual implementation of `auth_register()` calls `auth_login()` before `return` and the `token` returned is in fact the one returned by `auth_login()`.
2. Assume that it's not possible for multiple logged-in users to have the same `token`.
3. Assume that the `token` becomes invalid once the user logged out.
4. Assume that we are able to get and use the secret code sent to the user by `auth_passwordreset_request()`.

## channel details
1. Assume that `channel_listall()` can list all public and private channels.
2. Assume that `channel_list()` and `channel_listall()` will return an empty list if no channel exists.
3. Assume that an `AccessError` will raise for `channel_invite()` if a user puts an invalid `token`.

## message_send/edit
1. Assume that an `AccessError` will raise if a user who is not a member of a channel attempts to send messages on that channel.
2. Assume that a `ValueErr` will raise if the message being sent is an empty string `''` or has more than 1000 characters.
3. Assume that a newline character `'\n'` will be appended to the end of a message when the user hits Enter to send a message.
4. Assume that Assumption 3 ensures that every message ends with a `'\n'` so that when passing `'\n'` in `search()` function, it returns all the messages on the channels that the user has joined.
5. Assume that `message_send_later()` takes in current time and a future time that the user specified, it will compare if the future time is ahead of current time.
6. We cannot test if a message has been send sucessfully by checking the existance of message on channelID, since there may exists a message with the same content but different message_id


## message_remove
Assume that
> the message no longer exists

refers to that message_id is not a valid message within channels that the user has joined.
We can't really rely on an existing function to test if a user is the Slackr Admin or owner.

## message_react/message_unreact
Since Sally and Bob didn't specified a valid data type that stores reactions, we assume that it is not worth writing tests in that stage.
1. Assume that each `react_id` refers to a different emoji on the Slackr.
2. Assume that reactions is a list of dictionaries, where each dictionary contains `{message_id, u_id, react_id}`

## user_profile
1. Assume that every user has to be a member of at least one channel.
2. Assume that using `user_profile_set*()` functions to test the return value of `user_profile()` is not reliable since they don't have proper exceptions that handles the matching cases, e.g. returned_email = original_email.
3. Assume that symbols are allowed to appear in the email address. 
4. Assume that space is not allowed to appear in the email address. 
5. Assume the profile image being uploaded through `user_profiles_uploadphoto()` has to be cropped into a square which means x_end - x_start = y_end - y_start.
6. Assume that both symbols and space are allowed to appear in `handle_str`. 

## standup
1. Assume that a `ValueErr` will raise for `standup_start()` if the channel ID does not exist.
2. Assume that an `AccessError` will raise for `standup_start()` if the user is not a member of this channel.
3. Assume user can only start a standup if he/she is a member of the channel.

## search
1. Assume that empty query string is not allowed to be passed into `search()`.

