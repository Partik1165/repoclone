import os
import zipfile
import shutil
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
GIT_REPO = os.getenv("GIT_REPO")
CLONE_DIR = "cloned_repo"
ZIP_NAME = "repo_backup.zip"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive.")

async def send_repo(context: ContextTypes.DEFAULT_TYPE):
    try:
        # Clean up previous
        if os.path.exists(CLONE_DIR):
            shutil.rmtree(CLONE_DIR)
        if os.path.exists(ZIP_NAME):
            os.remove(ZIP_NAME)

        # Clone the repo
        subprocess.run(["git", "clone", GIT_REPO, CLONE_DIR], check=True)

        # Zip the folder
        shutil.make_archive("repo_backup", 'zip', CLONE_DIR)

        # Send the zip file
        await context.bot.send_document(chat_id=OWNER_ID, document=open(ZIP_NAME, 'rb'), caption="📦 GitHub repo backup")

    except Exception as e:
        await context.bot.send_message(chat_id=OWNER_ID, text=f"❌ Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Schedule the repo send task on startup
    app.job_queue.run_once(send_repo, 3)  # Delay 3s to make sure bot fully starts

    print("Bot started.")
    app.run_polling()
