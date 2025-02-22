# Disnake Bot Cogs

## Overview

This bot is composed of multiple cogs, each handling a specific function. Below is an overview of the available cogs:

## AI Cog

This AI Cog is a component of the bot that utilizes Google Generative AI to generate responses in a roleplaying style. The bot assumes the persona of Sokudo (速度), a 16-year-old Japanese girl with pink hair. The cog also includes moderation features such as bad word filtering, suicide prevention triggers, and mental health resource recommendations.

### Features

- **AI Chatbot**: Uses Google Generative AI (Gemini-2.0 Flash) for text responses and Gemini-1.5 Pro for image-based responses.
- **Message Filtering**: Replaces and censors bad words in messages.
- **Suicide Prevention**: Detects certain keywords related to self-harm and provides mental health resources.
- **Image Processing**: Accepts images as input for AI-generated responses.
- **Threaded Conversations**: Maintains chat history with context awareness.
- **Mention Handling**: Converts Discord user mentions into display names.
- **Game-Specific Knowledge**: Trained to answer questions about a specific game for a Discord community.
- **Custom Personality**: The AI chatbot is designed with a distinct personality to enhance engagement.


### Environment Variables

The cog requires the following environment variable:

- GAI: Your Google Generative AI API key.


### Usage

The AI Cog automatically listens to messages and responds when:

- The bot is mentioned.
- Certain trigger words (like “depressed”, “suicide”, etc.) are detected.
- A user replies to the bot's previous response.

### Moderation

- Messages containing blacklisted words are filtered and censored.
- If a message includes a trigger word, the bot provides relevant mental health resources.
- The bot will not respond to ^-prefixed messages to allow command execution without interference.

### Configuration

- Modify the bad_words dictionary to add or change word filtering rules.
- Adjust the triggers list to change how the bot detects sensitive topics.
- Customize mhr.json to update mental health resources.
- Modify the AI's behavior to adjust how it responds to game-related queries.

### Error Handling

- If a prompt is blocked by Google's API, the bot will notify users.
- If an unexpected error occurs, the bot logs the error and informs the user.

---

## Backup Cog

This Backup Cog allows administrators to create backups of the bot’s key files, including Python scripts, JSON configurations, and logs. The backup is automatically packaged into a .zip file and sent to the administrator.

### Features

- **Automated Backup**: Saves all .py, .json, .yml, and .log files.
- **Admin-Only Command**: Only users with administrator permissions can use the backup command.
- **ZIP Archive**: The backup is packaged into a zip file and sent as a Discord attachment.
- **Excludes Unnecessary Files**: Does not back up .git files.


### Usage

- Run ^backup (or your bot’s configured command prefix) in a channel where the bot has permission to send files.
- The bot will create a ZIP file and send it in the chat.

---

## Code Cog

The Code Cog provides file management capabilities for the bot, allowing users with the appropriate role to check directories, read, write, and delete files within the bot’s working directory.

### Features

- **Directory Listing**: Lists the contents of a specified directory.
- **File Reading**: Reads the contents of a specified file.
- **File Writing**: Saves provided content to a specified file.
- **File Deletion**: Deletes a specified file.
- **Role-Restricted**: Only users with a specific role can execute these commands.

---

## Backup Cog

This Backup Cog allows administrators to create backups of the bot’s key files, including Python scripts, JSON configurations, and logs. The backup is automatically packaged into a `.zip` file and sent to the administrator.

### Features

- **Automated Backup**: Saves all `.py`, `.json`, `.yml`, and `.log` files.
- **Admin-Only Command**: Only users with administrator permissions can use the backup command.
- **ZIP Archive**: The backup is packaged into a zip file and sent as a Discord attachment.
- **Excludes Unnecessary Files**: Does not back up `.git` files.

### Usage

- Run `^backup` (or your bot’s configured command prefix) in a channel where the bot has permission to send files.
- The bot will create a ZIP file and send it in the chat.

---

## Code Cog

The Code Cog provides file management capabilities for the bot, allowing users with the appropriate role to check directories, read, write, and delete files within the bot’s working directory.

### Features

- **Directory Listing**: Lists the contents of a specified directory.
- **File Reading**: Reads the contents of a specified file.
- **File Writing**: Saves provided content to a specified file.
- **File Deletion**: Deletes a specified file.
- **Role-Restricted**: Only users with a specific role can execute these commands.

### Usage

- `^code check <directory>` - Lists the contents of the specified directory.
- `^code read <file>` - Reads and displays the contents of the specified file.
- `^code write <file> <content>` - Writes the provided content to the specified file.
- `^code delete <file>` - Deletes the specified file.
- If an attachment is provided instead of content in the `write` command, the file is saved as an attachment.

---

## Journal Cog

The Journal Cog allows users to keep a personal journal within the bot. Entries are saved in a JSON file and can be viewed, added, or deleted by the user.

### Features

- **Add Journal Entries**: Users can add journal entries.
- **View Journal Entries**: Users can view all their past entries.
- **Delete Journal Entries**: Users can delete all their journal entries.
- **Save Data in JSON**: Journal entries are stored in `journal.json`.

### Usage

- `^add_entry <entry>` - Add a journal entry.
- `^view_entries` - View all journal entries.
- `^delete_entries` - Delete all journal entries.

---

## GoodCog

The GoodCog provides positive affirmations to users, encouraging them with a random message. It can be a nice addition to a bot for mental health and motivational support.

### Features

- **Random Affirmations**: Sends a positive affirmation message to the user.
- **Customizable Affirmation List**: The list of affirmations can be modified in the cog.

### Usage

- `^good` - Sends a random positive affirmation to the user.

```sh
pip install disnake google-generativeai pillow requests
```