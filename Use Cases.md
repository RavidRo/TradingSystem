# Use Cases

#### Table of Contents:

[Guest](#Guest)

-   [2.3. Registration](#2.3.%20Registration)
-   [2.4. Login](#2.4.%20Login)
-   [2.5. Getting store information](#2.5.%20Getting%20store%20information)
-   [2.6. Product search with filter](#2.6.%20Product%20search%20with%20filter)
-   [2.6. Filter search results](#2.6.%20Filter%20search%20results)
-   [2.7. Save products in shopping bag](#2.7.%20Save%20products%20in%20shopping%20bag)
-   [2.8 Visit cart](#2.8%20Visit%20cart)
-   [2.8. Delete product from cart](#2.8.%20Delete%20product%20from%20cart)
-   [2.8. Change amount of product in cart](#2.8.%20Change%20amount%20of%20product%20in%20cart)
-   [2.9. Purchase products](#2.9.%20Purchase%20products)

[Member](#Member)

-   [3.1. Logout](#3.1.%20Logout)
-   [3.2. Open a store](#3.2.%20#Open%20a%20store)
-   [3.7. Get personal purchase history](#3.7.%20Get%20personal%20purchase%20history)

[Owner and manager](#Owner%20and%20manager)

-   [enter store](#enter%20store)
-   [4.1. **no_name**](#4.1.%20__no_name__)
-   [4.2. Add new product](#4.2.%20Add%20new%20product)
-   [4.2. Remove product](#4.2.%20Remove%20product)
-   [4.2. Change product quantity](#4.2.%20Change%20product%20quantity)
-   [4.2. Edit product details](#4.2.%20Edit%20product%20details)
-   [4.2. Get purchase types and policies](#4.2.%20Get%20purchase%20types%20and%20policies)
-   [4.2. Get discount types and policies](#4.2.%20Get%20discount%20types%20and%20policies)
-   [4.2. Edit purchase types](#4.2.%20Edit%20purchase%20types)
-   [4.2. Edit discount types](#4.2.%20Edit%20discount%20types)
-   [4.2. Edit purchase policy](#4.2.%20Edit%20purchase%20policy)
-   [4.2. Edit discount policy](#4.2.%20Edit%20discount%20policy)
-   [4.3. Appoint new store owner](#4.3.%20Appoint%20new%20store%20owner)
-   [4.5. Appoint new store manager](#4.5.%20Appoint%20new%20store%20manager)
-   [4.6. Edit manager’s responsibilities](#4.6.%20Edit%20manager’s%20responsibilities)
-   [4.7. Dismiss an owner](#4.3.%20Dismiss%20an%20owner)
-   [4.9. Get store personnel information](#4.9.%20Get%20store%20personnel%20information)
-   [4.11. Get store purchase history](#4.11.%20Get%20store%20purchase%20history)

[System manager](#System%20manager)

-   [6.4. Get store purchase history (system manager)](<#6.4.%20Get%20store%20purchase%20history%20(system%20manager)>)
-   [6.4. Get user purchase history (system manager)](<#6.4.%20Get%20user%20purchase%20history%20(system%20manager)>)

## Guest

### 2.3. Registration

**Actors**: User  
**Parameters**: \_username, \_user_details  
**Pre-conditions**: User is not logged in.  
**Post-conditions**: There is a member in the system whose user name is username.  
**Actions**:

1. <ins>User</ins>: Chooses to register
2. <ins>System</ins>: Asks for user name and user details
3. <ins>User</ins>: Enters \_username and \_user_details
4. <ins>System</ins>: If \_username is already a member, generate error message and return to action 2.
5. <ins>System</ins>: Else, register \_username as member and generate success message.

**Tests**:  
<ins>_happy path_</ins>: The user enters username that is not exist in the system and other user details. The system registers the user to the system.  
<ins>_sad path_</ins>: The user enters a username that is already exist in the system. The system generates an error message.

### 2.4. Login

**Actors**: User  
**Parameters**: \_username, \_user_details  
**Pre-conditions**: User is not logged in.  
**Post-condition**: User is logged in.  
**Actions**:

1. <ins>User</ins>: Chooses to log in.
2. <ins>System</ins>: Asks for user name and \_user_details
3. <ins>User</ins>: Enters \_username and \_user_details
4. <ins>System</ins>: If \_username is a member and the other \_user_details match, log the user in.
5. <ins>System</ins>: Else, generate error message and return to action 2.

**Tests**:  
<ins>_happy path_</ins>: the user logs in with correct username and match details. The system logs the user in.  
<ins>_sad path_</ins>: the user enters user name that exist in the system but the other user details (password for example does not match to the username)

### 2.5. Getting store information

**Actors**: User  
**Parameters**: None  
**Pre-conditions**: None.  
**Pos-tconditions**: None.  
**Actions**:

1. <ins>User</ins>: chooses to get all stores information.
2. <ins>System</ins>: searches the information in database.
3. <ins>System</ins>: shows the information.

happy path: all the stores are shown as expected.  
sad path: the user tries to search stores when there are no stores in the system.

### 2.6. Product search with filter

**Actors**: User  
**Parameters**: \_search_phrase  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>User</ins>: chooses to search products.
2. <ins>System</ins>: queries the user for search phrase.
3. <ins>User</ins>: enters \_search_phrase.
4. <ins>System</ins>: ask for field to filter by
5. <ins>User</ins>: enters \_filter_field
6. <ins>Optional</ins>: System: asks for optional parameters.
7. <ins>Optional</ins>: User: enters \_optional_parameters.
8. <ins>System</ins>: searches results by name, category, or keywords.
9. <ins>System</ins>: if there are results from search shows the results.
10. Else, generate message “there are no results”

happy path: the user searches a product with a product name which exists in the system and gets the results.  
sad path: the user wrongs in one letter in the product name that he desire to search and gets the message “there are no results.

### 2.6. Filter search results

**Actors**: User, Product search  
**Parameters**: \_filter_field, \_optional_parameters  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Optional</ins>: Product search: finished
2. <ins>User</ins>: chooses to filter the search results.
3. <ins>System</ins>: asks for field to filter by.
4. <ins>Use</ins>r: enters \_filter_field.
5. <ins>Optional</ins>: System: asks for optional parameters.
6. <ins>Optional</ins>: User: enters \_optional_parameters.
7. <ins>System</ins>: filters the search results.

happy path: the user filter by store rank (above average).  
sad path: the user filter by price range and enters negative prices

### 2.7. Save products in shopping bag

**Actors**: User  
**Parameters**: \_product  
**Pre-condition**: None.  
**Post-condition**: \_product is added to the store's bag.  
**Actions**:

1. <ins>User</ins>: choose to save \_product
2. <ins>System</ins>: if \_product already in the bag, update the amount of \_product in the bag.
3. <ins>System</ins>: Else, add \_product to the bag.
4. <ins>System</ins>: if User is logged in, save \_product to the database.

happy path: the user chooses to save to the bag a product that already exists there and the shopping bag updates accordingly.  
sad path: the user though he saved the product, but he didn’t.

### 2.8 Visit cart

**Actors**: User  
**Parameters**: None  
**Pre-condition**: None.  
**Post-conditions**: None.  
**Actions**:

1. <ins>User</ins>: chooses to visit cart.
2. <ins>System</ins>: shows the user's cart.

### 2.8. Delete product from cart

**Actors**: User, Visit cart  
**Parameters**: \_to_delete_product  
**Pre-condition**: The cart contains \_to_delete_product.  
**Post-condition**: The cart doesn't contain \_to_delete_product.  
**Actions**:

1. <ins>Visit cart</ins>: finished
2. <ins>User</ins>: chooses \_to_delete_product from the cart.
3. <ins>System</ins>: asks the user for the action
4. <ins>User</ins>: chooses to delete \_to_delete_product
5. <ins>System</ins>: deletes \_to_delete_product from the cart.

happy-user chooses to delete a product that exists in the cart and the system asks for the action from the user. The user accepts the action and the product is deleted from the cart.  
sad-user accidentally chooses to delete a product from the cart. The product exists in the cart. When the system asks the user for the action, the user cancels the deletion.

### 2.8. Change amount of product in cart

**Actors**: User, Visit cart  
**Parameters**: \_to_change_product, \_amount  
**Pre-condition**: \_amount > 0, to_change_product is in the cart.  
**Post-condition**: The cart contains \_amount of \_to_change_product.  
**Actions**:

1. <ins>Visit cart</ins>: finished
2. <ins>User</ins>: chooses \_to_change_product from the cart.
3. <ins>System</ins>: asks the user for the action
4. <ins>User</ins>: chooses to change \_to_change_product's amount
5. <ins>System</ins>: queries user for the new amount.
6. <ins>User</ins>: enters \_amount
7. <ins>System</ins>: updates \_to_change_product's amount to \_amount.

happy-user chooses to change product’s amount in the cart. Right now the product exists in the cart and has 5 copies of it. after the system queries the user for the action and the amount , the user changes the product’s quantity from 5 to 7 and the cart updates successfully.  
sad-user accidently chooses to change a product’s A amount in the cart. instead of to change product’s B amount in the cart. after the system queries the user for the action , the user cancels it.

### 2.9. Purchase products

**Actors**: User, Outside Cashing, Outside Supplyment  
**Parameters**: \_payment_information  
**Pre-condition**: None.  
**Post-condition**: Cart (of immediate products section) is empty.  
**Actions**:

1. <ins>User</ins>: chooses to purchase the products in his cart.
2. <ins>System</ins>: start timer (10 minutes)
3. <ins>System: foreach shopping bag:
    1. for each product:
        1. <ins>System</ins>: if product is not available, generate error message.
        2. <ins>System</ins>: if product has multiple purchase options.
            1. <ins>System</ins>: ask User to choose purchase type.
            2. <ins>User</ins>: chooses the type.
        3. <ins>System</ins>: If the type is “immediate purchase”:
            1. <ins>System</ins>: apply discount policy on the product and sum up its price.
            2. <ins>System</ins>: else, move the product to the other product’s section in the bag (for example, bid offer).
4. <ins>System</ins>: removes all the products were bought from the store.
5. <ins>System</ins>: ask for user the payment information.
6. <ins>User</ins>: enters \_payment_information.
7. <ins>System</ins>: sends \_payment_information and total price to Outside Cashing.
8. <ins>Outside Cashing</ins>: performs billing and returns indicate message.
9. <ins>System</ins>: if the process succeeded, return success message, else generate error message and abort.
10. <ins>System</ins>: sends the products to Outside Supplyment.
11. <ins>Outside Supplyment</ins>: supply products, return indicate message.
12. <ins>System</ins>: if outside supplyment accepts, generates success message and returns to the user.
13. <ins>System</ins>: else, generate error message.
14. <ins>System</ins>: generates the appropriate shopping details and saves it as “user purchase history” and “stores purchase history”.
15. <ins>System</ins>: removes all the products from user’s shopping cart.
    Timer timeout : generate error message

## Member

### 3.1. Logout

**Actors**: Member  
**Parameters**: None  
**Pre-condition**: Member is logged in.  
**Post-condition**: Member is not logged in.  
**Actions**:

1. <ins>Member</ins>: chooses to log out.
2. <ins>System</ins>: logs the user out.

### 3.2. Open a store

**Actors**: Member  
**Parameters**: \_store_information  
**Pre-condition**: None.  
**Post-condition**: A new store is created.  
**Actions**:

1. <ins>Member</ins>: chooses to open a new store.
2. <ins>System</ins>: asks for the store information.
3. <ins>Member</ins>: enters store_information.
4. <ins>System</ins>: creates a new store with Member as the owner and Store_information as the store information.
5. <ins>System</ins>: adds the new store’s reference to the member

### 3.7. Get personal purchase history

**Actors**: Member  
**Parameters**: None  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Member</ins>: chooses to get personal purchase history.
1. <ins>System</ins>: gets the purchase history from the database.
1. <ins>System</ins>: shows the purchase history.

## Owner and manager

### enter store

**Actors**: Store personnel  
**Parameters**: \_store  
**Pre-condition**: \_store exists in the system, Store personnel is a manager or an owner of \_store.  
**Post-condition**: None.  
**Actions**:

1. <ins>Store personnel</ins>: chooses to enter a store.
1. <ins>System</ins>: asks for the store identifier.
1. <ins>Store owner</ins>: enters \_store.
1. <ins>System</ins>: shows \_store’s data and possible actions.

### 4.1. **no_name**

### 4.2. Add new product

**Actors**: Store personnel, enter store  
**Parameters**: \_product_information, \_quantity, \_store  
**Pre-condition**: \_quantity>0, all \_product_information is valid (price>0 etc.).  
**Post-condition**: \_quantity of products is added to \_store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to add a new product.
1. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product information and \_quantity.
    1. <ins>Store personnel</ins>: enters \_product_information and \_quantity.
        1. if \_quantity legal and information legal
            1. <ins>System</ins>: asks the user for approval
        1. <ins>System</ins>: if user approves ,adds \_quantity of products to \_store.
        1. else, decline the process
        1. else, generate an error message
1. Else, generate an error message

### 4.2. Remove product

**Actors**: Store personnel, enter store  
**Parameters**: \_product_identifier, \_store  
**Pre-condition**: The product exists in \_store.  
**Post-condition**: The product is removed from \_store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to remove a product.
1. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product identifier.
    1. <ins>Store personnel</ins>: enters product_identifier.
        1. if product identifier correct
            1. <ins>System</ins>: the product is removed from store.
        1. else, generate error message
1. else, generate an error message

### 4.2. Change product quantity

**Actors**: Store personnel, enter store  
**Parameters**: \_product_identifier, \_quantity, \_store  
**Pre-condition**: \_store exists, product exists in \_store, \_quantity > 0.  
**Post-condition**: The product’s quantity is changed in \_store to \_quantity.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to update a product’s quantity.
1. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product identifier and quantity.
    1. <ins>Store personnel</ins>: enters product_identifier and \_quantity.
    1. <ins>System</ins>: the product’s quantity is updated in \_store.
    1. <ins>System</ins>: else, genetate error message and abort.

### 4.2. Edit product details

**Actors**: Store personnel, enter store  
**Parameters**: \_product_information, \_store  
**Pre-condition**: The product exists in \_store, all \_product_information is valid (price > 0 etc.).  
**Post-condition**: The product’s information is updated in \_store to product_information.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store </ins>: chooses to update product’s information.
1. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product information.
    1. <ins>Store personnel</ins>: enters product_information.
    1. <ins>System</ins>: asks for approval for the update
        1. if user approves
            1. the product’s information is updated in \_store.
        1. Else, dicline process

### 4.2. Get purchase types and policies

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to receive purchase types and policies.
1. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: searches the information.
    1. <ins>System</ins>: shows the information.
    1. <ins>System</ins>: else, generate error message and abort.

### 4.2. Get discount types and policies

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to receive purchase types and policies.
1. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: searches the information.
    1. <ins>System</ins>: shows the information.
    1. <ins>System</ins>: else, generate error message and abort.

### 4.2. Edit purchase types

**Actors**: Store personnel, enter store  
**Parameters**: \_types, \_store  
**Pre-condition**: \_types includes the default purchase type.  
**Post-condition**: The buying types in the store are updated to \_types.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to edit the store’s purchase types.
1. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated purchase types.
    1. <ins>Store personnel</ins>: enters \_types.
    1. If user chooses to delete the default type:
        1. Generate an error message.
        1. Else, delete the type.
    1. <ins>System</ins>: updates the purchase types of the store to \_types.
    1. <ins>System</ins>: else, generate error message and abort.

### 4.2. Edit discount types

**Actors**: Store personnel, enter store  
**Parameters**: \_types, \_store  
**Pre-condition**: \_types includes the default purchase type.  
**Post-condition**: The buying types in the store are updated to \_types.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to edit the store’s purchase types.
1. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated purchase types.
    1. <ins>Store personnel</ins>: enters \_types.
    1. If user chooses to delete the default type:
        1. Generate an error message.
        1. Else, delete the type.
    1. <ins>System</ins>: updates the purchase types of the store to \_types.
    1. <ins>System</ins>: else, generate error message and abort.

### 4.2. Edit purchase policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy, \_store  
**Pre-condition**: \_policy is valid policy.  
**Post-condition**: The purchase policy in the store is updated to \_policy.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to edit the store’s purchase policy.
1. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated purchase policy.
    1. <ins>Store personnel</ins>: enters \_policy.
    1. <ins>System</ins>: updates the purchase policy of the store to \_policies.
    1. <ins>System</ins>: else, generate error message and abort.

### 4.2. Edit discount policy

**Actors**: Store personnel, enter store  
**Parameters**: \_discount, \_store  
**Pre-condition**: \_discount is valid policy.  
**Post-condition**: The discount policy in the store is updated to \_policy.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to edit the store’s discount policy.
1. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated discount policy.
    1. <ins>Store personnel</ins>: enters \_policy.
    1. <ins>System</ins>: updates the discount policy of the store to \_policies.
    1. <ins>System</ins>: else, generate error message and abort.

### 4.3. Appoint new store owner

**Actors**: Store owner, enter store  
**Parameters**: \_new_owner, \_store  
**Pre-condition**: \_new_owner is a member, \_new_owner is not an owner of this store.  
**Post-condition**: \_new_owner is an owner of this store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store owner</ins>: chooses to appoint a new store owner.
1. <ins>System</ins>: asks for the new owner information.
1. <ins>Store owner</ins>: enters new_owner.
1. <ins>System</ins>: adds the new owner to the store.

### 4.5. Appoint new store manager

**Actors**: Store owner, enter store  
**Parameters**: \_new_manager, \_store  
**Pre-condition**: \_new_manager is a member, \_new_manager is not a manager of this store.  
**Post-condition**: \_new_manager is a manager of this store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store owner</ins>: chooses to appoint a new store manager.
1. <ins>System</ins>: asks for the new manager information.
1. <ins>Store owner</ins>: enters new_manager.
1. <ins>System</ins>: adds new_manager to the store.
1. <ins>System</ins>: assign the default responsibilities to new_manager.

### 4.6. Edit manager’s responsibilities

**Actors**: Store owner, enter store  
**Parameters**: \_manager, \_responsibilities, \_store  
**Pre-condition**: \_manager is a store manager of this store.  
**Post-condition**: \_manager’s responsibilities are updated to \_responsibilities.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store </ins>: chooses to change a manager’s responsibilities.
1. <ins>System</ins>: asks for the manager identifier and updated responsibilities.
1. <ins>Store owner</ins>: enters \_manager and \_responsibilities.
1. <ins>System</ins>: updates \_manager’s responsibilities.

### 4.7. Dismiss an owner

**Actors**: Store owner, enter store  
**Parameters**: \_manager, \_store  
**Pre-condition**: \_manager was appointed by Store owner.  
**Post-condition**: \_manager is no longer a manager of \_store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store owner</ins>: chooses to dismiss a manager.
1. <ins>System</ins>: asks for the manager’s information.
1. <ins>Store owner</ins>: enters \_manager.
    1. if data legal removes \_manager from the store.
        1. removes all the users that were appointed by him and their subtrees of responsibilities.
    1. else, generate an error message.

### 4.9. Get store personnel information

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to get personal information.
1. <ins>System</ins>: if Store personnel is an owner of this store or a manager with permission to access this information:
    1. <ins>System</ins>: searches for the personnel information for the store.
    1. <ins>System</ins>: shows the information.

### 4.11. Get store purchase history

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
1. <ins>Store personnel</ins>: chooses to get store purchase history.
1. <ins>System</ins>: if Store personnel is an owner of this store or a manager with permission to access this information:
    1. <ins>System</ins>: searches for the store’s purchase history.
    1. <ins></ins>: shows the purchase history.

## System manager

### 6.4. Get store purchase history (system manager)

**Actors**: System manager  
**Parameters**: \_store  
**Pre-condition**: \_store exists in the system.  
**Post-condition**: None.  
**Actions**:

1. <ins>System manager</ins>: chooses to get a store’s purchase history.
1. <ins>System</ins>: asks for the store identifier.
1. <ins>Store owner</ins>: enters \_store.
1. <ins>System</ins>: searches for the information in the database.
1. <ins>System</ins>: shows the information.

### 6.4. Get user purchase history (system manager)

**Actors**: System manager  
**Parameters**: \_user  
**Pre-condition**: \_user exists in the system.  
**Post-condition**: None.  
**Actions**:

1. <ins>System manager</ins>: chooses get user’s purchase history.
1. <ins>System</ins>: asks for the user identifier.
1. <ins>Store owner</ins>: enters \_user.
1. <ins>System</ins>: searches for the information in the database.
1. <ins>System</ins>: shows the information.
