# pyShortURL

pyShortURL is a REST Api used for shortening urls

# Usage

There are two options you can take, use a custom url or generate a random one

### Random aproach

Make a post request to the /shorten endpoint. Include a JSON formatted like bellow.

```json
{
    "url": "https://example.com/0"
}
```

The above will return

```json
{
    "msg": "ok",
    "url": "a2jnc"
}
```

### Custom aproach

Make a post request to the /custom endpoint. Include a JSON formatted like bellow

```json
{
    "url": "https://example.com/1",
    "custom_url": "test"
}
```

The above will return a JSON

```json
{
    "msg": "ok",
    "url": "https://example.com/1", 
    "custom_url": "test"
}
```

## How to use this data

The usage is going to depend on which approach you chose

### Random approach

Make a GET request to /u/\<random-url-here>

For example, GET /u/a2jnc

This will return a JSON

```json
{
    "msg": "ok",
    "url": "https://example.com/0"
}
```

### Custom approach

Make a GET request to /c/\<custom-url-here>

For example, GET /c/test

This will return a JSON

```json
{
    "msg": "ok",
    "url": "https://example.com/1"
}
```

# Setup

## Setup a virtual envoriment

```
virtualenv pyShortUrl
```
or
```python
python -m virtualenv pyShortUrl
```

Clone the repo

```git
mkdir src
cd src/
git clone https://github.com/ramenbroth/pyShortURL
```

Then install the requirements
```
pip install requirements.txt
```

And make sure to install sqlite

After that just do

```
python api.py
```

Note that by default the api runs on port 8000, if you want to change that just set the enviroment variable "PORT" to whatever port you want it to run on and restart the api.

By default debugging is enabled, set the enviroment variable "PROD" to 'true' to disable it.