\# CareSync



\### SMARTER HEALTHCARE. CONNECTED CARE.



CareSync is a Django-based healthcare management platform designed to connect patients and doctors through a centralized digital healthcare system.



\## Features



\* \*\*Patient Dashboard:\*\* Centralized access to healthcare services.

\* \*\*Appointment Booking:\*\* Book appointments with doctors.

\* \*\*Doctor Availability:\*\* View doctor specialties and availability.

\* \*\*Medicine Stock:\*\* Check medicine inventory and expiry information.

\* \*\*Emergency Assistance:\*\* Submit emergency consultation requests.

\* \*\*Virtual Assistance:\*\* Get predefined first-aid guidance based on reported problems.

\* \*\*Doctor Dashboard:\*\* Manage emergency consultation requests and patient interactions.

\* \*\*Video Consultation:\*\* Prototype video consultations using Jitsi Meet.



\## Technology Stack



\* \*\*Backend:\*\* Python, Django

\* \*\*Frontend:\*\* HTML, CSS, JavaScript

\* \*\*Database:\*\* SQLite

\* \*\*Video Consultation:\*\* Jitsi Meet

\* \*\*Version Control:\*\* Git, GitHub



\## Project Structure



```text

CareSync/

├── clinic/

├── medicalapp/

├── manage.py

├── requirements.txt

├── .gitignore

├── LICENSE

└── README.md

```



\## Installation and Setup



1\. Clone the repository:



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

```



2\. Navigate to the project:



```bash

cd CareSync

```



3\. Create a virtual environment:



```bash

python -m venv venv

```



4\. Activate it on Windows:



```bash

venv\\Scripts\\activate

```



5\. Install dependencies:



```bash

pip install -r requirements.txt

```



6\. Apply database migrations:



```bash

python manage.py migrate

```



7\. Create an administrator account:



```bash

python manage.py createsuperuser

```



8\. Start the development server:



```bash

python manage.py runserver

```



Open `http://127.0.0.1:8000/` in your browser.



\## Important Notes



\* The virtual assistance feature uses predefined responses and is not a substitute for professional medical advice.

\* Video consultation is a prototype and requires appropriate security measures before real patient use.

\* This repository does not include the local SQLite database or private credentials.



\## Future Enhancements



\* Secure patient authentication.

\* AI-assisted healthcare information retrieval with verified sources.

\* Improved doctor-patient communication.

\* Enhanced security and deployment.



\## Author



\*\*K. Bhavya Sree\*\*



B.Tech Computer Science

Woxsen University



\## License



All Rights Reserved. See the \[LICENSE](LICENSE) file.



