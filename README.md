# sms2po

**sms2po** is a simple Python HTTP server listening on port 8088 to act as a custom SMSC provider in [QNAP Notification Center](https://www.qnap.com/solution/notification-center/). It will pull the the message text from SMS notifications and send via [Pushover](https://pushover.net/) instead.

## Install / Configure / Containerize

I've built my own Docker container and run **sms2po** on a ARM-based SBC, but you can do whatever suits you, of course. In a nutshell:
* **```git clone```** (or download & extract) this repo
* edit the **PUSHOVER_*** variables in ```compose.yaml``` as below:

###### Required:
```
PUSHOVER_TOKEN=yourpushovertoken
PUSHOVER_USER=yourpushoveruserkey
```
###### Optional: (defaults are listed here)
```
PUSHOVER_TITLE=QNAP NAS
PUSHOVER_SOUND=none
PUSHOVER_PRIO=0
```

### Build & Launch Docker Container:
```bash
docker compose up --build --detach
```

## Configuring QNAP Notification Center

* **```+ Add SMSC Service```**
* Select **```custom```** as the **```SMS service provider```**.
* **```Alias```** can be whatever you like
* For **```URL template text```** specify:  
**```http://<host>:8088?phone=@@PhoneNumber@@&text=@@Text@@```**
* **```SMS server login name```** and **```SMS server login password```** can be left blank

**\<host\>:8088** is where this container is running - perhaps on the QNAP itself in [Container Station](https://www.qnap.com/en/software/container-station)

## Phone Numbers in Notification Center
The recipient phone number you configure can be anything - it is ignored when using Pushover

## Support

You are on your own, but I occasionally lurk in the [QNAP forums](https://forum.qnap.com/") 

## License

[MIT](https://choosealicense.com/licenses/mit/)
