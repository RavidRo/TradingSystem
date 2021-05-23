# Installation

### Backend:

-   install python version >3.9
-   install pip
-   install all requirements `pip install -r "requirements.txt"`

### Fronted:

-   install Node >= 10.16 and npm >= 5.6
-   install install dependencies `cd ./Frontend && npm install`

# Run the app:

-   **Backend**: `python api.py`
-   **Frontend**: `cd ./Frontend && npm start`

# Documentation

### Config file format:
```javascript
{
	"admins": <list-of-admin-usernames (list[str])>,
	"password": <admins-password (str)>,
	"timer_length": <length-of-timer (int)>,
	"payment_system": <payment-system (str)>,
	"supply_system": <supply-system> (str),
	"DB": <database (str)>
}
```

### State file format:

![image](https://user-images.githubusercontent.com/48616609/119277382-f976f000-bc27-11eb-9aaa-feb60954412f.png)

### [Use Cases](Documentation/Use%20Cases.md)

## Class Diagram

![class diagram](Documentation/ClassDiagram.drawio.svg)

### [Edit Diagram](https://viewer.diagrams.net/?highlight=0000ff&edit=https%3A%2F%2Fapp.diagrams.net%2F%23HSeanPikulin%252FTradingSystem%252FDocumentation%252FDocumentation%252FClassDiagram.drawio.svg&layers=1&nav=1&title=ClassDiagram.drawio.svg#Uhttps%3A%2F%2Fraw.githubusercontent.com%2FSeanPikulin%2FTradingSystem%2FDocumentation%2FDocumentation%2FClassDiagram.drawio.svg%3Ftoken%3DALTBLBTKMMZHRUJV7OT64XDALBLNS)
