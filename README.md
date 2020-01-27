# pyShortURL

pyShortURL is a REST Api used for shortening urls

# Usage

There are two options you can take, use a custom url or generate a random one

### Random aproach

Make a POST to /random. include a JSON formatted like bellow.

```json
{
  "url": "https://example.com/0"
}
```

The above will return

```json
{
  "isError": false,
  "shortenedUrl": "SaBopD",
  "url": "https://example.com/0"
}
```

To get the original URL, make a GET to /, include a JSON formatted like bellow.

```json
{
  "shortenedUrl": "testeeeee"
}
```

The above will return

```json
{
  "isError": false,
  "shortenedUrl": "testeeeee",
  "url": "google.comgergregre"
}
```

### Custom aproach

Make a post request to the /custom endpoint. include a JSON formatted like bellow

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

To get the original URL, make a GET to /, include a JSON formatted like bellow.

```json
{
  "shortenedUrl": "test"
}
```

The above will return

```json
{
  "isError": false,
  "shortenedUrl": "testeeeee",
  "url": "https://example.com/1"
}
```

# Setup

## Setup a [virtual envoriment](https://github.com/pypa/virtualenv)

```sh
virtualenv pyShortUrl
```

or

```sh
python -m virtualenv pyShortUrl
```

Clone the repo

```sh
mkdir app
git clone https://github.com/ramenbroth/pyShortURL app
cd app/
```

Activate your virtual environment

```sh
source ../bin/activate.fish # replace .fish according to the shell you're using
```

Then install the requirements

```
pip install -r requirements.txt
```

And make sure to create the necessary tables

Open a python shell and run

```python
>>>import api
>>>api.setup_database()
```

After that just run

```sh
flask run
```
