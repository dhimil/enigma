## How to configure
`config.json` in the project root directory provides a list of configuration parameters which you can edit depending on your requirement.

## Parameters:
The following table lists all the default Enigma configuration parameters and also explains the usage:

Parameter name | Default | Description
--- | --- | ---
django_setup.SECRET_KEY | "" (Empty string) | `String` Set the DJANGO setup secret key. This value should be kept secret.
django_setup.DEBUG | True (dev mode only) | `Boolean` User authorised to view details of all users. <br>  **Note: DEBUG should be set to `False` in production.**
django_setup.ALLOWED_HOSTS | [] (Empty list) | `Array` User authorised to view access of all users. <br> If DEBUG is False, you also need to properly set the ALLOWED_HOSTS setting. Failing to do so will result in all requests being returned as “Bad Request (400)”
sso.googleapi.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY | "" (Empty string) | `String` Google OAuth 2.0 client ID. Obtain OAuth 2.0 credentials from the Google API Console.
sso.googleapi.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET | "" (Empty string) | `String` Google OAuth 2.0 client secret. Obtain OAuth 2.0 credentials from the Google API Console.
database.engine | sqlite3 | `String` The database backend to use. Enigma has support for **mysql** and **sqlite3**
database.dbname | "" (Empty string) | `String` The name of the database to use. *Not used with SQLite.*
database.username | "" (Empty string) | `String` The username to use when connecting to the database. *Not used with SQLite.*
database.password | "" (Empty string) | `String` The password to use when connecting to the database. *Not used with SQLite.*
database.host | "" (Empty string) | `String` The host to use when connecting to the database. *Not used with SQLite.*
database.port | | `Integer` The port to use when connecting to the database. *Not used with SQLite.*
access_modules.git_urls | ["https://github.com/browserstack/enigma-public-access-modules.git"] (Enigma's Access Module Repository)| `Array` List of Git URLs of access modules, these URLs are fed to the cloning script to pull the modules into the running container.
access_modules.RETRY_LIMIT | 5 | `Integer` Maximum number of tries to clone the access modules repository
enigmaGroup.MAIL_APPROVER_GROUPS | [] (Empty list) | `Array` List of approvers Email for managing groups.
email.access-approve | "" (Empty string) | `String` Admin access approver's email address
email.EMAIL_HOST | "" (Empty string) | `String` The host to use for sending email.
email.EMAIL_PORT | "" (Empty string) | `String` Port to use for the SMTP server
email.EMAIL_HOST_USER | "" (Empty string) | `String` Username to use for the SMTP server
email.EMAIL_HOST_PASSWORD | "" (Empty string) | `String` Password to use for the SMTP server
email.EMAIL_USE_TLS | True | `Boolean` Whether to use a TLS (secure) connection when talking to the SMTP server.
email.EMAIL_USE_SSL | False | `Boolean` Whether to use an implicit TLS (secure) connection when talking to the SMTP server.
email.DEFAULT_FROM_EMAIL | "" (Empty string) | `String` Default email address to use for various correspondence from Enigma.
background_task_manager.type | celery | `String` Type can be **celery** or **threading**
background_task_manager.config | | *Not used with threading.* <br> Refer to [Celery.md](docs/Celery.md) for detailed information on celery configuration parameters/


The config file contains only the default parameters (described above). You can edit the file and add the configuration parameters depending on your requirement.
You will also be required to update the `schema.json` with the new parameters:

`schema.json` defines the parameters and their properties in configuration file. It also specifies each attributes data type to ensure that only appropriate data is present.
To validate the configuration file run the following command:
```bash
make schema_validate
```
Once, it returns a success response, you are good to go!


Reference:
- [JSON Schema Basics](https://json-schema.org/understanding-json-schema/reference/index.html)