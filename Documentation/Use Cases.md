# Use Cases

#### Table of Contents:

[Guest](#Guest)

-   [2.3. Registration](#23-Registration)
-   [2.4. Login](#24-Login)
-   [2.5. Getting store information](#25-Getting-store-information)
-   [2.6. Product search with filter](#26-Product-search-with-filter)
-   [2.6. Filter search results](#26-Filter-search-results)
-   [2.7. Save products in shopping bag](#27-Save-products-in-shopping-bag)
-   [2.8 Visit cart](#28-Visit-cart)
-   [2.8. Delete product from cart](#28-Delete-product-from-cart)
-   [2.8. Change amount of product in cart](#28-Change-amount-of-product-in-cart)
-   [2.9. Purchase products](#29-Purchase-products)

[Member](#Member)

-   [3.1. Logout](#31-Logout)
-   [3.2. Open a store](#32-#Open-a-store)
-   [3.7. Get personal purchase history](#37-Get-personal-purchase-history)

[Owner and manager](#Owner-and-manager)

-   [enter store](#enter-store)
-   [4.1. Add new product](#41-Add-new-product)
-   [4.1. Remove product](#41-Remove-product)
-   [4.1. Change product quantity](#41-Change-product-quantity)
-   [4.1. Edit product details](#41-Edit-product-details)
-   [4.2. Get purchase types and policies](#42-Get-purchase-types-and-policies)
-   [4.2. Get discount types and policies](#42-Get-discount-types-and-policies)
-   [4.2. Edit purchase types](#42-Edit-purchase-types)
-   [4.2. Edit discount types](#42-Edit-discount-types)
-   [4.2. Add purchase policy](#42-Add-purchase-policy)
-   [4.2. Edit purchase policy](#42-Edit-purchase-policy)
-   [4.2. Remove purchase policy](#42-Remove-purchase-policy)
-   [4.2. Move purchase policy](#42-Move-purchase-policy)
-   [4.2. Add discount policy](#42-Add-discount-policy)
-   [4.2. Edit discount policy](#42-Edit-discount-policy)
-   [4.2. Remove discount policy](#42-Remove-discount-policy)
-   [4.2. Move discount policy](#42-Move-discount-policy)
-   [4.3. Appoint new store owner](#43-Appoint-new-store-owner)
-   [4.5. Appoint new store manager](#45-Appoint-new-store-manager)
-   [4.6. Edit manager’s responsibilities](#46-Edit-manager’s-responsibilities)
-   [4.7. Dismiss an owner](#43-Dismiss-an-owner)
-   [4.9. Get store personnel information](#49-Get-store-personnel-information)
-   [4.11. Get store purchase history](#411-Get-store-purchase-history)

[System manager](#System-manager)

-   [6.4. Get store purchase history (system manager)](#64-Get-store-purchase-history-system-manager)
-   [6.4. Get user purchase history (system manager)](#64-Get-user-purchase-history-system-manager)

## Guest

### 2.3. Registration

**Actors**: User  
**Parameters**: \_username, \_credentials  
**Pre-conditions**: User is not logged in.  
**Post-conditions**: There is a member in the system whose user name is username.  
**Actions**:

1. <ins>User</ins>: Chooses to register
2. <ins>System</ins>: Asks for user name and credentials
3. <ins>User</ins>: Enters \_username and \_credentials
4. <ins>System</ins>: If \_username is already a member, generate error message and return to action 2.
5. <ins>System</ins>: Else, register \_username as member and generate success message.

**Tests**:  
<ins>_Happy Path_</ins>: The user enters username that is not exist in the system and other user details. The system registers the user to the system.  
<ins>_Sad Path_</ins>: The user enters a username that is already exist in the system. The system generates an error message.

### 2.4. Login

**Actors**: User  
**Parameters**: \_username, \_credentials 
**Pre-conditions**: User is not logged in.  
**Post-condition**: User is logged in.  
**Actions**:

1. <ins>User</ins>: Chooses to log in.
2. <ins>System</ins>: Asks for user name and \_credentials
3. <ins>User</ins>: Enters \_username and \_credentials
4. <ins>System</ins>: If \_username is a member and the \_credentials match, log the user in.
5. <ins>System</ins>: Else, generate error message and return to action 2.

**Tests**:

-   <ins>_Happy Path_</ins>: The user logs in with correct username and match details. The system logs the user in.
-   <ins>_Sad Path_</ins>: The user enters user name that doesn't exist in the system.
-   <ins>_Sad Path_</ins>: The user enters user name that exist in the system but the credentials (password for example) does not match to the username

### 2.5. Getting store information

**Actors**: User  
**Parameters**: None  
**Pre-conditions**: None.  
**Post-conditions**: None.  
**Actions**:

1. <ins>User</ins>: chooses to get all stores information.
2. <ins>System</ins>: searches the information in database.
3. <ins>System</ins>: shows the information.

**Tests**:

-   <ins>_Happy Path_</ins>: All the stores are shown as expected.
-   <ins>_Sad Path_</ins>: The user tries to search stores when there are no stores in the system.

### 2.6. Product search with filter

**Actors**: User  
**Parameters**: \_search_phrase, \_filter_field, \_optional_parameters 
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

**Tests**:

-   <ins>_Happy Path_</ins>: The user searches a product with a product name which exists in the system and gets the results.
-   <ins>_Sad Path_</ins>: The user wrongs in one letter in the product name that he desire to search and gets the message “there are no results.

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

**Tests**:

-   <ins>_Happy Path_</ins>: The user filter by one of the possible options (for example: store rank (above average)).
-   <ins>_Sad Path_</ins>: The user tries to filter by a non possible option and doesn't get results.
-   <ins>_Sad Path_</ins>: The user filters by a possible option but enters invalid param (price range - enters negative prices)

### 2.7. Save products in shopping bag

**Actors**: User  
**Parameters**: \_product, \_store_id, \_quantity   
**Pre-condition**: quantity > 0.  
**Post-condition**: \_product is added to the store's bag with the specified quantity.  
**Actions**:

1. <ins>User</ins>: choose to save \_product with \_quantity.
2. <ins>System</ins>: if \_product doesn't exist with \_quantity in store with \_store_id, abort with error.
3. <ins>System</ins>: if \_product already in the bag, abort with error.
4. <ins>System</ins>: Else, add \_product to the bag with \_quantity.
5. <ins>System</ins>: if User is logged in, save \_product to the database.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to save to the bag a product that already exists there and the shopping bag updates accordingly.
-   <ins>_Sad Path_</ins>: The user though he saved the product, but he didn’t.
-   <ins>_Sad Path_</ins>: The user chooses a product which he already added to the bag.
-   <ins>_Sad Path_</ins>: The user chooses a product which is out of stock.

### 2.8 Visit cart

**Actors**: User  
**Parameters**: None  
**Pre-condition**: None.  
**Post-conditions**: None.  
**Actions**:

1. <ins>User</ins>: chooses to visit cart.
2. <ins>System</ins>: shows the user's cart.

-   <ins>_Happy Path_</ins>: User chooses to visit his cart and the system shows him all of his cart details.

### 2.8. Delete product from cart

**Actors**: User, Visit cart  
**Parameters**: \_to_delete_product, \_store_id  
**Pre-condition**: None 
**Post-condition**: The cart doesn't contain \_to_delete_product.  
**Actions**:

1. <ins>Visit cart</ins>: finished
2. <ins>User</ins>: chooses to delete \_to_delete_product from store with \_store_id from the cart.
3. <ins>System</ins>: asks the user for the action
4. <ins>User</ins>: chooses to delete \_to_delete_product
5. <ins>System</ins>: if cart doesn't hold a bag for store_id, abort with error.
6. <ins>System</ins>: if bag of store_id doesn't hold \_to_delete_product, abort with error.
7. <ins>System</ins>: deletes \_to_delete_product from the cart.

**Tests**:

-   <ins>_Happy Path_</ins>: User chooses to delete a product that exists in the cart and the system asks for the action from the user. The user accepts the action and the product is deleted from the cart.
-   <ins>_Sad Path_</ins>: User accidentally chooses to delete a product from the cart. The product exists in the cart. When the system asks the user for the action, the user cancels the deletion.
-   <ins>_Sad Path_</ins>: User accidently chooses a store_id which has no appropriate bag in cart.
-   <ins>_Sad Path_</ins>: User accidently chooses a product which is not in the shopping cart.

### 2.8. Change amount of product in cart

**Actors**: User, Visit cart  
**Parameters**: \_to_change_product, \_amount, store_id  
**Pre-condition**: \_amount > 0.  
**Post-condition**: The cart contains \_amount of \_to_change_product.  
**Actions**:

1. <ins>Visit cart</ins>: finished
2. <ins>System</ins>: asks the user for the action
4. <ins>User</ins>: chooses to change \_to_change_product's amount with new_amount
5. <ins>System</ins>: if cart doesn't hold a bag for store_id, abort with error.
6. <ins>System</ins>: if bag of store_id doesn't hold \_to_change_product, abort with error.
7. <ins>System</ins>: updates \_to_change_product's amount to \_amount.

**Tests**:

-   <ins>_Happy Path_</ins>: User chooses to change product’s amount in the cart. Right now the product exists in the cart and has 5 copies of it. after the system queries the user for the action and the amount , the user changes the product’s quantity from 5 to 7 and the cart updates successfully.
-   <ins>_Sad Path_</ins>: User accidentally chooses to change a product’s A amount in the cart. instead of to change product’s B amount in the cart. after the system queries the user for the action , the user cancels it.
-   <ins>_Sad Path_</ins>: User accidently chooses a store_id which has no appropriate bag in cart.
-   <ins>_Sad Path_</ins>: User accidently chooses a product which is not in the shopping cart.

### 2.9. Purchase products

**Actors**: User, Outside Cashing, Outside Supplyment  
**Parameters**: \_payment_information, products_purchase_info, \_address
**Pre-condition**: None.  
**Post-condition**: Cart (of immediate products section) is empty.  
**Actions**:

1. <ins>User</ins>: chooses to purchase the products in his cart.
2. <ins>System</ins>:  ask User to choose purchase types for products.
3. <ins>User</ins>: enters products with purchase types.
4. <ins>System: foreach shopping bag:
    1. for each product:
        1. <ins>System</ins>: if product is not available, generate error message and abort.
        2. <ins>System</ins>: if purchase type for product doesn't match the bag's store purchase policy, abort with error message.
        3. <ins>System</ins>: If the type is “immediate purchase”:
            1. <ins>System</ins>: apply discount policy on the product and sum up its price.
            2. <ins>System</ins>: else, move the product to the other product’s section in the bag (for example, bid offer).
    2. <ins>System</ins>: removes all the products that were acquired from the store.
5. <ins>System</ins>: start timer (10 minutes)
6. <ins>System</ins>: ask for user the payment information and address.
7. <ins>User</ins>: enters \_payment_information and \_address.
8. <ins>System</ins>: sends \_payment_information and total price to Outside Cashing.
9. <ins>Outside Cashing</ins>: performs billing and returns indicate message.
10. <ins>System</ins>: if the process succeeded, return success message, else rollback the purchase and return error.
11. <ins>System</ins>: sends the products and \_address to Outside Supplyment.
12. <ins>Outside Supplyment</ins>: supply products, return indicate message, else rollback the purchase and return error..
13. <ins>System</ins>: if outside supplyment accepts, generates success message and returns to the user.
14. <ins>System</ins>: else, generate error message and rollback the purchase.
15. <ins>System</ins>: removes all the products from user’s shopping cart.
16. <ins>System</ins>: generates the appropriate shopping details and saves it as “user purchase history” and “stores purchase history”.
    Timer timeout : generate error message, rollback the purchase and abort

**Tests**:

-   <ins>_Happy Path_</ins>: User chooses to purchase products in her cart, the system applies discounts . The user enters payment information correctly, the purchase was done and the system updates the products in the stores and the cart.
-   <ins>_Sad Path_</ins>: User chooses to purchase products from cart, but there are missing products in the store.
-   <ins>_Sad Path_</ins>: User chooses to purchase products from cart, but accidently chose not appropraite purchase types.s
-   <ins>_Sad Path_</ins>: User chooses to purchase products in her cart, the system applies discounts . When the system asks for payment information, the user enters her details but the cashing system declines the process and generates an error message.
-   <ins>_Sad Path_</ins>: User chooses to purchase products in her cart, the system applies discounts . When the system asks for payment information, user inserts all needed but then she goes and disappears for 15 minutes so the system gets into timeout and generates an error message.
-   <ins>_Sad Path_</ins>: User chooses to purchase products in her cart, the system applies discounts . When the system asks for payment information, user inserts all needed and then the system turns to supplyment system that rejects the process and generates an error message.

## Member

### 3.1. Logout

**Actors**: Member  
**Parameters**: None  
**Pre-condition**: Member is logged in.  
**Post-condition**: Member is not logged in.  
**Actions**:

1. <ins>Member</ins>: chooses to log out.
2. <ins>System</ins>: logs the user out.

**Tests**:

-   <ins>_Happy Path_</ins>: User wishes to logout from the system . the user chooses to logout from the system and the action succeeded.
-   <ins>_Sad Path_</ins>: User accidentally chooses to logout from the system and the action succeeded.

### 3.2. Open a store

**Actors**: Member  
**Parameters**: \_store_information  
**Pre-condition**: None.  
**Post-condition**: A new store is created.  
**Actions**:

1. <ins>Member</ins>: chooses to open a new store.
2. <ins>System</ins>: asks for the store information.
3. <ins>Member</ins>: enters store_information.
4. <ins>System</ins>: creates a new store with Member as the founder and Store_information as the store information.
5. <ins>System</ins>: adds the new store’s reference to the member

**Tests**:

-   <ins>_Happy Path_</ins>: Member wants to open a store. enters the right information and the store is created.
-   <ins>_Sad Path_</ins>: User wants to open a store. when the system asks for store information, the user accidentally enters letter in Greek.

### 3.7. Get personal purchase history

**Actors**: Member  
**Parameters**: None  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Member</ins>: chooses to get personal purchase history.
2. <ins>System</ins>: gets the purchase history.
3. <ins>System</ins>: shows the purchase history.

**Tests**:

-   <ins>_Happy Path_</ins>: Member chooses to see her personal purchase history and the system retrieves the data from the DB and shows it to her.
-   <ins>_Sad Path_</ins>: Member chooses to see her personal purchase history by mistake (did not mean to) and the system retrieves the data and shows it to her.

## Owner and manager

### enter store

**Actors**: Store personnel  
**Parameters**: \_store  
**Pre-condition**: \_store exists in the system, Store personnel is a manager or an owner of \_store.  
**Post-condition**: None.  
**Actions**:

1. <ins>Store personnel</ins>: chooses to enter a store.
2. <ins>System</ins>: asks for the store identifier.
3. <ins>Store owner</ins>: enters \_store.
4. <ins>System</ins>: shows \_store’s data and possible actions.

### 4.1. Add new product

**Actors**: Store personnel, enter store  
**Parameters**: \_product_information, \_quantity, \_store  
**Pre-condition**: \_quantity>0, all \_product_information is valid (price>0 etc.).  
**Post-condition**: \_quantity of products is added to \_store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to add a new product.
3. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product information and \_quantity.
    2. <ins>Store personnel</ins>: enters \_product_information and \_quantity.
        1. if \_quantity legal and information legal
            1. <ins>System</ins>: asks the user for approval
        2. <ins>System</ins>: if user approves ,adds \_quantity of products to \_store.
        3. else, decline the process
        4. else, generate an error message
4. Else, generate an error message

**Tests**:

-   <ins>_Happy Path_</ins>: The owner the store chooses to add to the store product in 20 pieces. The owner inserts the correct amount, the system asks for approval, the user approves and information and the process succeeds.
-   <ins>_Sad Path_</ins>: The owner of the store chooses to add to the store a product in 20 pieces. When the system requests for product’s amount the owner accidently enters 10 pieces. When the system requests for approval the owner

### 4.1. Remove product

**Actors**: Store personnel, enter store  
**Parameters**: \_product_identifier, \_store  
**Pre-condition**: The product exists in \_store.  
**Post-condition**: The product is removed from \_store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to remove a product.
3. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product identifier.
    2. <ins>Store personnel</ins>: enters product_identifier.
        1. if product identifier correct
            1. <ins>System</ins>: the product is removed from store.
        2. else, generate error message
4. else, generate an error message

**Tests**:

-   <ins>_Happy Path_</ins>: The owner of a store wants to remove a product from his store. The owner enters the correct product identifier and the system removes the item from the store.
-   <ins>_Sad Path_</ins>: The owner of a store wants to remove a product and enters wrong identifier, the system generates an error message.

### 4.1. Change product quantity

**Actors**: Store personnel, enter store  
**Parameters**: \_product_identifier, \_quantity, \_store  
**Pre-condition**: \_store exists, product exists in \_store, \_quantity > 0.  
**Post-condition**: The product’s quantity is changed in \_store to \_quantity.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to update a product’s quantity.
3. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product identifier and quantity.
    2. <ins>Store personnel</ins>: enters product_identifier and \_quantity.
    3. <ins>System</ins>: the product’s quantity is updated in \_store.
    4. <ins>System</ins>: else, genetate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: The user is a manager of a store and has the responsibility “change product quantity”. He updates the quantity of a product and the action succeeded.
-   <ins>_Sad Path_</ins>: A manager of a store which has the responsibility “change product quantity”, wants to update the amount of a product. After the system queries the user for the product id and quantity, the manager accidently typed a bigger amount which will lead to mistakes.

### 4.1. Edit product details

**Actors**: Store personnel, enter store  
**Parameters**: \_product_information, \_store  
**Pre-condition**: The product exists in \_store, all \_product_information is valid (price > 0 etc.).  
**Post-condition**: The product’s information is updated in \_store to product_information.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store </ins>: chooses to update product’s information.
3. <ins>System</ins>: if Store personnel is an owner of \_store or a manager with permissions to do this:
    1. <ins>System</ins>: asks for product information.
    2. <ins>Store personnel</ins>: enters product_information.
    3. <ins>System</ins>: asks for approval for the update
        1. if user approves
            1. the product’s information is updated in \_store.
        2. Else, dicline process

**Tests**:

-   <ins>_Happy Path_</ins>: One of the managers of the store wants to update a product’s details. He enters all the correct information and the product updates in the system.
-   <ins>_Sad Path_</ins>: One of the managers a store wants to update product’s details. After the system queries the user for the product information makes a typing mistake. Therefore, the updated information for the product is incorrect.

### 4.2. Get purchase types and policies

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to receive purchase types and policies.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: searches the information.
    2. <ins>System</ins>: shows the information.
    3. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: The owner chooses to see the purchase types and policies of the store.
-   <ins>_Sad Path_</ins>: The owner chooses to see the purchase types and policies of the store by mistake.

### 4.2. Get discount types and policies

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to receive purchase types and policies.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: searches the information.
    2. <ins>System</ins>: shows the information.
    3. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: The owner chooses to see the discount types and policies of the store.
-   <ins>_Sad Path_</ins>: The owner chooses to see the discount types and policies of the store by mistake.

### 4.2. Edit purchase types

**Actors**: Store personnel, enter store  
**Parameters**: \_types, \_store  
**Pre-condition**: \_types includes the default purchase type.  
**Post-condition**: The buying types in the store are updated to \_types.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to edit the store’s purchase types.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated purchase types.
    2. <ins>Store personnel</ins>: enters \_types.
    3. If user chooses to delete the default type:
        1. Generate an error message.
        2. Else, delete the type.
    1. <ins>System</ins>: updates the purchase types of the store to \_types.
    1. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to edit a store’s buying types and adds new purchase type. The system updates accordingly.
-   <ins>_Sad Path_</ins>: The user chooses to edit a store’s buying types but he accidently instead of deleting some purchase type he deletes another one.

### 4.2. Edit discount types

**Actors**: Store personnel, enter store  
**Parameters**: \_types, \_store  
**Pre-condition**: \_types includes the default purchase type.  
**Post-condition**: The buying types in the store are updated to \_types.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to edit the store’s purchase types.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated purchase types.
    2. <ins>Store personnel</ins>: enters \_types.
    3. If user chooses to delete the default type:
        1. Generate an error message.
        2. Else, delete the type.
    4. <ins>System</ins>: updates the purchase types of the store to \_types.
    5. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to edit a store’s discount types and entersnew discount type and it updated successfully.
-   <ins>_Sad Path_</ins>: The user chooses to edit a store’s discount types and accidently deleted a discount type that he didn’t want to

### 4.2. Add purchase policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_details, \_store  
**Pre-condition**: \_policy_details are valid policy details.  
**Post-condition**: The purchase policies in the store are updated to include a new policy with \_policy_details.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to add to the store’s purchase policies.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant permissions:
    1. <ins>System</ins>: asks for the new purchase policy's details.
    2. <ins>Store personnel</ins>: enters \_policy_details.
    3. <ins>System</ins>: adds the new purchase policy with \_policy_details to \_policies.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to add the policy and enters a valid policy details.
-   <ins>_Sad Path_</ins>: A guest tries to add a policy and the system generates error message.

### 4.2. Edit purchase policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_details, \_store  
**Pre-condition**: \_policy_details is valid policy.  
**Post-condition**: The purchase policy in the store is updated to \_policy_details.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to edit the store’s purchase policy.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated purchase policy.
    2. <ins>Store personnel</ins>: enters \_policy_details.
    3. <ins>System</ins>: updates a purchase policy in the store to \_policy_details.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to edit the policy and enters a valid policy.
-   <ins>_Sad Path_</ins>: A guest tries to edit policy and the system generates error message.

### 4.2. Remove purchase policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_id, \_store  
**Pre-condition**: \_policy_id is an id of an existing purchase policy.  
**Post-condition**: The purchase policies in the store are updated to not include the policy with \_policy_id.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to remove a purchase policy from a store.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant permissions:
    1. <ins>System</ins>: asks for the purchase policy's id.
    2. <ins>Store personnel</ins>: enters \_policy_id.
    3. <ins>System</ins>: removes the purchase policy with \_policy_id from \_policies.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to remove a policy and enters a valid policy id.
-   <ins>_Sad Path_</ins>: A guest tries to remove a policy and the system generates an error message.

### 4.2. Move purchase policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_id, \_parent_policy, \_store  
**Pre-condition**: \_policy_id is an id of an existing purchase policy, \_parent_policy is an existing policy.
**Post-condition**: the policy with \_policy_id is moved from its parent to be a child policy of \_parent_policy.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to move a purchase policy.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant permissions:
    1. <ins>System</ins>: asks for the policy id and the parent id.
    2. <ins>Store personnel</ins>: enters \_policy_id and \_parent_policy.
    3. <ins>System</ins>: moves the purchase policy with \_policy_id from its parent to \_parent_policy.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to move the policy and enters a valid parent policy.
-   <ins>_Sad Path_</ins>: A guest tries to move a policy and the system generates error message.

### 4.2. Add discount policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_details, \_store  
**Pre-condition**: \_policy_details are valid policy details.  
**Post-condition**: The discount policies in the store are updated to include a new policy with \_policy_details.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to add to the store’s discount policies.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant permissions:
    1. <ins>System</ins>: asks for the new discount policy's details.
    2. <ins>Store personnel</ins>: enters \_policy_details.
    3. <ins>System</ins>: adds the new discount policy with \_policy_details to \_policies.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to add the policy and enters a valid policy details.
-   <ins>_Sad Path_</ins>: A guest tries to add a policy and the system generates error message.

### 4.2. Edit discount policy

**Actors**: Store personnel, enter store  
**Parameters**: \_discount, \_store  
**Pre-condition**: \_discount is valid policy.  
**Post-condition**: a discount policy in the store is updated to \_discount.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to edit the store’s discount policy.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant responsibility:
    1. <ins>System</ins>: asks for the updated discount policy.
    2. <ins>Store personnel</ins>: enters \_discount.
    3. <ins>System</ins>: updates a discount policy of the store to \_discount.
    4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to edit the discount and enters a valid policy.
-   <ins>_Sad Path_</ins>: A guest tries to edit discount and the system generates error message.

### 4.2. Remove discount policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_id, \_store  
**Pre-condition**: \_policy_id is an id of an existing discount policy.  
**Post-condition**: The discount policies in the store are updated to not include the policy with \_policy_id.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to remove a discount policy from a store.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant permissions:
    1. <ins>System</ins>: asks for the discount policy's id.
    2. <ins>Store personnel</ins>: enters \_policy_id.
    3. <ins>System</ins>: removes the discount policy with \_policy_id from \_policies.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to remove a policy and enters a valid policy id.
-   <ins>_Sad Path_</ins>: A guest tries to remove a policy and the system generates an error message.

### 4.2. Move discount policy

**Actors**: Store personnel, enter store  
**Parameters**: \_policy_id, \_parent_policy, \_store  
**Pre-condition**: \_policy_id is an id of an existing discount policy, \_parent_policy is an existing policy.
**Post-condition**: the policy with \_policy_id is moved from its parent to be a child policy of \_parent_policy.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to move a discount policy.
3. <ins>System</ins>: if the personnel is an owner or a manager with the relevant permissions:
    1. <ins>System</ins>: asks for the policy id and the parent id.
    2. <ins>Store personnel</ins>: enters \_policy_id and \_parent_policy.
    3. <ins>System</ins>: moves the discount policy with \_policy_id from its parent to \_parent_policy.
4. <ins>System</ins>: else, generate error message and abort.

**Tests**:

-   <ins>_Happy Path_</ins>: A store owner chooses to move the policy and enters a valid parent policy.
-   <ins>_Sad Path_</ins>: A guest tries to move a policy and the system generates error message.

### 4.3. Appoint new store owner

**Actors**: Store owner, enter store  
**Parameters**: \_new_owner, \_store  
**Pre-condition**: \_new_owner is a member, \_new_owner is not an owner of this store.  
**Post-condition**: \_new_owner is an owner of this store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store owner</ins>: chooses to appoint a new store owner.
3. <ins>System</ins>: asks for the new owner information.
4. <ins>Store owner</ins>: enters new_owner.
5. <ins>System</ins>: adds the new owner to the store.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to appoint a new store owner and enters the owner identifier and the store identifier. The store owners are updated accordingly.
-   <ins>_Sad Path_</ins>: The user chooses to appoint a new store owner but types a wrong owner identifier, so the system will generate an error message and no new owner will be added.

### 4.5. Appoint new store manager

**Actors**: Store owner, enter store  
**Parameters**: \_new_manager, \_store  
**Pre-condition**: \_new_manager is a member, \_new_manager is not a manager of this store.  
**Post-condition**: \_new_manager is a manager of this store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store owner</ins>: chooses to appoint a new store manager.
3. <ins>System</ins>: asks for the new manager information.
4. <ins>Store owner</ins>: enters new_manager.
5. <ins>System</ins>: adds new_manager to the store.
6. <ins>System</ins>: assign the default responsibilities to new_manager.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to appoint a new store manager and enters the manager’s identifier and the store’s identifier. The store managers are updated accordingly.
-   <ins>_Sad Path_</ins>: The user chooses to appoint a new store manager but types a wrong manager identifier, so the system will generate an error message and no new maanger will be added.

### 4.6. Edit manager’s responsibilities

**Actors**: Store owner, enter store  
**Parameters**: \_manager, \_responsibilities, \_store  
**Pre-condition**: \_manager is a store manager of this store.  
**Post-condition**: \_manager’s responsibilities are updated to \_responsibilities.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store </ins>: chooses to change a manager’s responsibilities.
3. <ins>System</ins>: asks for the manager identifier and updated responsibilities.
4. <ins>Store owner</ins>: enters \_manager and \_responsibilities.
5. <ins>System</ins>: updates \_manager’s responsibilities.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to change a manager’s responsibilities and to add for him another responsibility. The system updates accordingly.

-   <ins>_Sad Path_</ins>: The user chooses to change a manager’s responsibilities and accidently clicks another responsibility than ment and then re-do the action.

### 4.7. Dismiss an owner

**Actors**: Store owner, enter store  
**Parameters**: \_manager, \_store  
**Pre-condition**: \_manager was appointed by Store owner.  
**Post-condition**: \_manager is no longer a manager of \_store.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store owner</ins>: chooses to dismiss a manager.
3. <ins>System</ins>: asks for the manager’s information.
4. <ins>Store owner</ins>: enters \_manager.
    1. if data legal removes \_manager from the store.
        1. removes all the users that were appointed by him and their subtrees of responsibilities.
    2. else, generate an error message.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to dismiss a manager and enters his correct details and the system dismisses him and all of his sub tree.

-   <ins>_Sad Path_</ins>: The user chooses to dismiss a manager and accidently enters incorrect details. The system generated an error message

### 4.9. Get store personnel information

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to get personal information.
3. <ins>System</ins>: if Store personnel is an owner of this store or a manager with permission to access this information:
    1. <ins>System</ins>: searches for the personnel information for the store.
    2. <ins>System</ins>: shows the information.

**Tests**:

-   <ins>_Happy Path_</ins>: The user is logged in, the entered store exists, and the user is one of the store personnel. Therefore, the system returns the store’s information.

-   <ins>_Sad Path_</ins>: The user is not a store personnel and the system returns an error message.

### 4.11. Get store purchase history

**Actors**: Store personnel, enter store  
**Parameters**: \_store  
**Pre-condition**: None.  
**Post-condition**: None.  
**Actions**:

1. <ins>Enter store</ins>: finishes.
2. <ins>Store personnel</ins>: chooses to get store purchase history.
3. <ins>System</ins>: if Store personnel is an owner of this store or a manager with permission to access this information:
    1. <ins>System</ins>: searches for the store’s purchase history.
    2. <ins></ins>: shows the purchase history.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to get a store purchase history and enters a store identifier that exists in the system. The system returns the store purchase history.
-   <ins>_Sad Path_</ins>: The user chooses to get a store purchase history and enters a store identifier. The user does not have permissions to view the purchase history at the requested store and the system returns an error message “You do not have permission to view the purchase history for the given store”.

## System manager

### 6.4. Get store purchase history (system manager)

**Actors**: System manager  
**Parameters**: \_store  
**Pre-condition**: \_store exists in the system.  
**Post-condition**: None.  
**Actions**:

1. <ins>System manager</ins>: chooses to get a store’s purchase history.
2. <ins>System</ins>: asks for the store identifier.
3. <ins>Store owner</ins>: enters \_store.
4. <ins>System</ins>: searches for the information in the database.
5. <ins>System</ins>: shows the information.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to get a store purchase history and enters a store id as the store identifier. The system returns the store purchase history.
-   <ins>_Sad Path_</ins>: The user chooses to get a store purchase history and a nonexistent store id as the store identifier. The requested store does not exist, and the system returns an error message “{the given identifier} store does not exist”.

### 6.4. Get user purchase history (system manager)

**Actors**: System manager  
**Parameters**: \_user  
**Pre-condition**: \_user exists in the system.  
**Post-condition**: None.  
**Actions**:

1. <ins>System manager</ins>: chooses get user’s purchase history.
2. <ins>System</ins>: asks for the user identifier.
3. <ins>Store owner</ins>: enters \_user.
4. <ins>System</ins>: searches for the information in the database.
5. <ins>System</ins>: shows the information.

**Tests**:

-   <ins>_Happy Path_</ins>: The user chooses to get a user purchase history and enters a username as the user identifier. The system returns the user purchase history.
-   <ins>_Sad Path_</ins>: The user chooses to get a user purchase history and enters an incorrect username as the store identifier. The requested user does not exist and the system returns an error message “{incorrect username} is not a user in the system”.
