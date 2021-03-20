## guest
### 2.3. Registration  
**Actors**: User  
**Parameters**: username, user details  
**Preconditions**: User is not logged in.  
**Postcondition**: There is a member in the system whose user name is username.  
**Actions**:  
1. User: chooses to register  
2. System: asks for user name and user details  
3. User: enters username and user details  
4. System: if _username is already a member, generate error message and return to action 2.  
5. System: Else, register username as member and generate success message.  
6. 
**Tests**:  
<ins>*happy path*</ins>: The user enters username that is not exist in the system and other user details. The system registers the user to the system.  
<ins>*sad path*</ins>: The user enters a username that is already exist in the system. The system generates an error message.  
