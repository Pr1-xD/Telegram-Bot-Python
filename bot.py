from pyexpat.errors import messages
from subprocess import call
from tabnanny import check
from timeit import repeat
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
from credentials import bot_token, bot_user_name,URL

updater = Updater(bot_token,
				use_context=True)

jobqueue = updater.job_queue

txhash=''


#start function

def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hello sir, Welcome to the Bot.Please write\
		/help to see the commands available.")


#help function		

def help(update: Update, context: CallbackContext):
	update.message.reply_text("""Available Commands :-
	/motivate: get quotes""")


#unknown handler function	

def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry '%s' is not a valid command" % update.message.text)


#motivation quote function		

def motivate(update, context):
    quote = requests.request(url='https://api.quotable.io/random',method='get')
    update.message.reply_text(quote.json()['content'])


# returns token price for fixed token address	

def tokenprice(update, context):
    quote = requests.request(url='https://api.covalenthq.com/v1/1/xy=k/uniswap_v2/pools/?quote-currency=USD&format=JSON&contract-addresses=0x4ae2cd1f5b8806a973953b76f9ce6d5fab9cdcfd&key=ckey_7e494e0bde414fd19967dfc3586',method='get')
    update.message.reply_text(quote.json()["data"]["items"][0]["token_0"]["quote_rate"])


# returns token price for any token address	

def gettokenprice(update, context: CallbackContext):
	geturl="https://api.covalenthq.com/v1/1/xy=k/uniswap_v2/pools/?quote-currency=USD&format=JSON&contract-addresses="+context.args[0]+"&key=ckey_7e494e0bde414fd19967dfc3586"
	print(geturl)
	quote = requests.request(url=geturl,method='get')
	if(quote.json()["data"]["items"][0]["token_0"]["quote_rate"]):
		update.message.reply_text(quote.json()["data"]["items"][0]["token_0"]["quote_rate"])
	else:
		update.message.reply_text("Can not get price")	

# returns liquidity for fixed token address			

def liquidity(update, context):
    quote = requests.request(url='https://api.covalenthq.com/v1/1/xy=k/uniswap_v2/pools/?quote-currency=USD&format=JSON&contract-addresses=0x4ae2cd1f5b8806a973953b76f9ce6d5fab9cdcfd&key=ckey_7e494e0bde414fd19967dfc3586',method='get')
    update.message.reply_text(quote.json()["data"]["items"][0]["total_liquidity_quote"])


# gets latest buys from txlist

def getNewBuys():
	global txhash
	cnt=-1

	txlist = requests.request(url='https://api.covalenthq.com/v1/1/xy=k/uniswap_v2/tokens/address/0x461b71cff4d4334bba09489ace4b5dc1a1813445/transactions/?quote-currency=USD&format=JSON&page-number=&page-size=&key=ckey_7e494e0bde414fd19967dfc3586',method='get')
	newtxhash=txlist.json()['data']['items'][cnt]['tx_hash']

	print('last tx hash'+txhash)
	print('new tx hash'+newtxhash)
	
	if(txhash!=newtxhash):
		print(txlist.json()['data']['updated_at'])
		while(txlist.json()['data']['items'][cnt]['tx_hash']!=txhash and cnt>-10):
			print(txlist.json()['data']['items'][cnt]['tx_hash'])
			cnt=cnt-1
		txhash=newtxhash


# repeating function 

def refreshtx(context: CallbackContext):
	print('60s')
	getNewBuys()
	context.bot.send_message(chat_id=1345491631,text='New Buy/Sell')


# testing bnb price function

def wbnb(update, context):
	quote = requests.request(url='https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&apikey=Q8YP1QDJBZ537SB47ECQGW7UPIAFE2VTZZ',method='get')
	update.message.reply_text(quote.json()['status'])   
	getNewBuys(txhash)     


# unknown handler function 

def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)


# repeating function testing

def callback_30(context: CallbackContext):
    context.bot.send_message(chat_id=1345491631,text='New Buy/Sell')



updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('motivate', motivate))
updater.dispatcher.add_handler(CommandHandler('price', tokenprice))
updater.dispatcher.add_handler(CommandHandler('getprice', gettokenprice))
updater.dispatcher.add_handler(CommandHandler('liquidity', liquidity))
updater.dispatcher.add_handler(CommandHandler('wbnb', wbnb))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands


# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

jobqueue.run_repeating(refreshtx, 60)

updater.start_polling()

updater.idle()


# run repeat ---------
# add to group
# api call	
# messages
# buy sell check
# hosting

# taxes, liq, max buy/sell, wallet and mc