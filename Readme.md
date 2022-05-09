<div id="top"></div>

#### **This project is just a personal project and this page is simply an exercise in documentation and should not be used.** 

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <!-- <li><a href="#contact">Contact</a></li> -->
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple project contained within a Docker Container that takes messages posted in a Discord Channel and post them to Twitter. The project uses Twitter's OAuth 1.0a to access Twitter's Developer API and post tweets. 





### Built With

* [discord.py](https://discordpy.readthedocs.io/en/stable)
* [Twitter API](https://developer.twitter.com/en/products/twitter-api)
* [Docker](https://www.docker.com/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.



### Prerequisites

[Install Docker](https://docs.docker.com/get-docker/) for your system. 



### Installation

1. Create a [Twitter Developer](https://developer.twitter.com/en) account and create a project. 
2. Generate and store your `Consumer Key` and `Consumer Secret` from the Developer Portal. 
3. Create a Discord Application from the [Discord Developer Portal](https://discord.com/developers/applications).
4. Generate and store the `Client Secret` under the OAuth2 tab of the application. 
5. Use the URL Generator under the OAuth 2.0 tab checking the `bot` and `Read Message History` permissions and invite the bot to your server. 
6. Get and store your [Twitter ID](https://tweeterid.com/) for your Developer Account. 
3. Clone the repo.
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```



<!-- USAGE EXAMPLES -->
## Usage

##### Build the Image

```sh
sudo docker build -t rdmbot .
```

##### Get Access Tokens

Run the image's OAuth 1.0 script with your Twitter Consumer Key and Secret to have a user authorize your application and fetch their Twitter Access Token and Secret to access the Twitter API on their behalf. 

```sh
sudo docker run -it --rm -e CONSUMER_KEY=<CONSUMER_KEY> -e CONSUMER_SECRET=<CONSUMER_SECRET> rdmbot auth.py
```

Follow the link provided from the script and feed the access code back to the script. 

#####  Docker Compose

Example of a `docker-compose.yml` file. 

```yml
version: "3"
services:
  rdmbot:
    image: rdmbot
    container_name: rdmbot
    volumes:
      - ./backlog.txt:/app/backlog.txt
    environment:
      - CONSUMER_KEY=<CONSUMER_KEY>
      - CONSUMER_SECRET=<CONSUMER_SECRET>
      - ACCESS_TOKEN=<ACCESS_TOKEN>
      - ACCESS_TOKEN_SECRET=<ACCESS_TOKEN_SECRET>
      - DISCORD_BOT_KEY=<DISCORD_BOT_KEY>
      - TWITTER_ID=<TWITTER_ID>
```

Passing a `backlog.txt` as a volume is optional. 

##### Compose up
```sh
sudo docker-compose up -d
```



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
<!--
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com
Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)
-->



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [discord.py - Create a Bot Account](https://discordpy.readthedocs.io/en/stable/discord.html)
