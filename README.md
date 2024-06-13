# Leya

AI coding assistant which can directly be ported into the terminal and be used to query complex Git repositories

https://pypi.org/project/leya/

## Overview

The Git Coding Assistant is a versatile tool designed to allow you to query and find solutions to code within your git repository. Leveraging the power of Git and OpenAI, it offers functionalities such as cloning repositories, selecting repositories for focused queries, and extracting relevant code snippets and providing you solutions to your queries.

## Features

- **Repository Cloning**: Easily clone GitHub repositories directly from the command line.
- **Repository Selection**: Select repositories to work with, enabling focused queries and interactions.
- **Code Querying**: Query repositories for specific code issues or information using natural language queries.
- **Function-based Queries**: Narrow down queries by specifying function names to focus on.
- **Intelligent Answer Generation**: Utilize AI to extract and provide intelligent answers to code-related queries.

## Usage


Before using Leya, you need to set up your environment variables for the OpenAI API key and Pinecone API key:

**Option 1: Export Environment Variables (Linux and macOS)**

Open your terminal and export the environment variables using the following commands:
```bash
    $ export OPENAI_API_KEY=<your_openai_api_key>
    $ export PINECONE_KEY=<your_pinecone_api_key>
```


**Option 2: Export Environment Variables (Windows)**

**For Windows users, you can set the environment variables using the following commands in PowerShell**
    ```bash
        $ $env:OPENAI_API_KEY="<your_openai_api_key>"
        $ $env:PINECONE_KEY="<your_pinecone_api_key>"
    ```
**Option 3: Add Environment Variables (Manual)**

Alternatively, you can manually add the environment variables through your system settings:

OpenAI API Key: Add a new environment variable named OPENAI_API_KEY with your OpenAI API key as the value.
Pinecone API Key: Add a new environment variable named PINECONE_KEY with your Pinecone API key as the value.
After setting up the environment variables, Leya will be able to access your API keys for authentication

# After Environment Variable setup 

1. **Downloading the package**:
   ```bash
   $ pip install leya
   
2. **Cloning Repositories and uploading repo chunks to pinecone**:
   ```bash
   $ leya -r <repository_url>
3. **Selecting Repositories**:
   ```bash
   $ leya -s
4. **Querying Repositories**:
   ```bash
   $ leya -q "<query>" 
5. **Optional addition of Function-based Queries**:
   ```bash
   $ leya -q "<query>" -f <function_name_1> <function_name_2> ...


## Contributing

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

## Credits

Developed by: PranavN1234

## Working 
### Store repositories

![Screenshot 2024-04-24 125402](https://github.com/PranavN1234/Leya/assets/44135759/f811430d-d93a-4364-82da-8763d35a8ea8)


### Swap between stored repositories 

![Screenshot 2024-04-24 125420](https://github.com/PranavN1234/Leya/assets/44135759/1dce74e8-37a1-4b3e-bed2-065379010055)


### Sample queries

** Query without functional parameters ** 

![Screenshot 2024-04-24 125501](https://github.com/PranavN1234/Leya/assets/44135759/e8098cc3-b347-4287-b2c0-6b9730412159)

** Query with functions appended to narrow scope of search **
![Screenshot 2024-04-24 125642](https://github.com/PranavN1234/Leya/assets/44135759/826719cc-0b97-4aa2-879d-670b5cec125c)





