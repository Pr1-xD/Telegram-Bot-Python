from telegram.ext import CallbackContext, Application

async def callback_minute(context: CallbackContext):
    await context.bot.send_message(chat_id='@priiiibot', text='One message every minute')

application = Application.builder().token('5649210270:AAGAkIcokndpiIPgJ-m64io11--uVCIv_gc').build()
job_queue = application.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=60, first=10)

application.run_polling()