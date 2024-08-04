# API Data Exporter

This application fetches data from various API endpoints, saves it in the desired file format, and sends it via email. The application is designed to be flexible, allowing you to specify the file format, the recipient email address, and which data files to create through command-line arguments.

## Features

- Fetch data from multiple API endpoints.
- Save data in various formats: CSV, JSON, or XLSX.
- Send the saved data as an email attachment.
- Use progress bars to track the status of API calls.
- Verbose logging to track the process.

## Setup

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/api-data-exporter.git
    cd api-data-exporter
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add the following environment variables:

    ```plaintext
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    GRANT_TYPE=your_grant_type
    SCOPE=your_scope
    EMAIL_ADDRESS=your_email_address@gmail.com
    EMAIL_PASSWORD=your_email_password
    TARGET_EMAIL=recipient@example.com
    ```

## Usage

You can run `main.py` with various options:

### Default Usage

This will save the data as `xlsx`, send it to the default email address, and fetch all available data.

```sh
python main.py
```

### Specify File Type

To save the data as CSV:

```sh
python main.py --file_type csv
```

### To save the data as JSON:

```sh
python main.py --file_type json
```

### Specify Recipient Email Address

### To send the email to a different email address:

```sh
python main.py --email someone@example.com
```

### Specify Which Files to Create

To specify which files to create (e.g., only roles and subscription groups):

```sh
python main.py --files roles subscription_groups
```

### Combine Options

You can combine options as needed. For example, to save the data as JSON, send it to a specific email address, and only create roles and jobs data files:

```sh
python main.py --file_type json --email someone@example.com --files roles jobs
```

## Components
### main.py

Handles the overall process, including fetching data, saving it, and sending the email.
### TokenGET.py

Handles obtaining the access token needed for API authentication.
### UsersGET.py

Contains functions to fetch data from various API endpoints related to users.
### DataSaver.py

Contains functions to save data in different formats (CSV, JSON, XLSX).
### EmailSender.py

Contains the function to send an email with the data file as an attachment.
### ProgressBars.py

Contains the function to display progress bars for API calls.
## License

This project is licensed under the MIT License. See the LICENSE file for details.