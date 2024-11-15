# invite-counter-bot
Counts the number of invites from users in a group

## Prerequisites
Need a Telegram Bot API token. Follow instructions from [Telegram](https://core.telegram.org/bots/tutorial).
Need a webhook url. Can check [Ngrok](https://ngrok.com/docs/integrations/hostedhooks/webhooks/) for instructions. 

## Instructions
* Use src/telegram_credentials/credentials_encrypt.py to encrypt bot token
* Run python app.py [port_number] [webhook_url] [optional:mongo]
