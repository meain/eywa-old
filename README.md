# eywa

````
Python version : 2.x
Django version : 1.9
````

## Useful stuff

### Using current aiml engine

It is quiet easy to use the aiml engine.
All you have to do is to add the aiml files in to the folder `eywa/ai/apis/aiml_files`.

Now if you need to have aiml files from multiple locations, just add the the other sources in `eywa/ai/apis/aimlbot.py`

### Adding apis

Adding more apis to the backend is quiet easy. All the apis base level apis are to be added in `eywa/ai/apis`.
Now in order to link them to the chat handle, we have two layers of abstraction over the base api.

**Layers of abstraction**

Level 2 : `reply.py` ( appends all apis result into a list to be sent over )

Level 1 : `apihandler.py` ( communicates with individual apis and format it as needed )

Level 0 : Base api

Now once you have implemented the base api we have to implement the formatting function in `apihandler.py`.
The format for any result could be of two types, it could either be a text result or an image(image link) result.

All result is a dict with two entries.
* content : Will contain the reply in the case of a text result and will contain the link to the image in case it is an image result
* type : Will contain the type of the result. It could be image or text and this field helps the js to differentiate between image link and text.

Below is how to define functions in `apihandler.py`

In the case of a text result :

```python
def text_result(params):
    item = {}
    item['content'] = callApiHere(query)
    item['type'] = "text"
    return item
```

In the case of an image result : 

```python
def image_result(params):
    item = {}
    item['content'] = callApiHere(query) # api should be returning image url
    item['type'] = "image"
    return item
```

Next part is to implement the call these functions defined in `apihandler.py` from `reply.py`

Here is where we decide which queries are to routed to which apis. In here we make use of the `get_result` function to divert the input to the desired api through `apihandler.py`.

## The flow of data

### Frontend

The frontend is mostly written in stylus(converted to css), pug(converted to html) and js.

* All html files are in `eywa/ai/templates`

* All static files like images, css and js are in `eywa/ai/static`

The initial page served is available in `eywa/ai/templates/ai/index.html`. It is derived from the base page `eywa/ai/templates/ai/base.html`

There is mostly two user interaction implemented in frontend [ user signin and chat ].
All the user interaction handling is done using the javascript file `chatjs.js`.

This javascript file (`chatjs.js`) is what is responsible for initiating the WebSocket connection to the server.
It start the WebSocket connection as soon as the page is loaded.

The user sign in handles by the funcions `onSignIn` and `signOut`.

Now when the user types in a chat message and clicks thesend button,
we aggregate the uesr information(using `formatRequest`) available from the google authentication platform and the user input into one single json doc and sends it over to the backend through this WebSocket connection.

On receiving the result back from the sever we iterates over all the results adding them down the last div in the chat window.

### Backend

The backend is written in `python` using [django framework](www.djangoproject.com), and using the help of [django channels](http://channels.readthedocs.org/) for WebSocket connection.

#### Quick Overview

**Http requests** - `urls.py`(eywa/eywa) > `urls.py`(eywa/ai) > `views.py`(eywa/ai)

**WebSocket request** - `route.py`(eywa/eywa) > `consumers.py`(eywa/ai) > `reply.py`(eywa/ai) > handles api calls and stuff

#### Working

The **initial webpage** request is routed through `urls.py` to `views.py` inside `eywa/ai/`.
Inside `views.py` we return the predefined page `index.html` located in `eywa/ai/templates/`

After initial http request, all the data transfer between server and client happens through a WebSocket connection initiated by js(`chatjs.js`).
All **user queries in the chat** are sent over to the backend through this WebSocket connection which
will be routed through `routing.py` in `eywa/eywa` into`consumers.py` in `eywa/ai`.

In `consumers.py` we essentially extract the user information and the chat message out of the recived WebSocket packet.
This information is sent over to `reply.py` in order to process the information using various apis and return the result back to `consumers.py` and further to the user through the WebSocket connection.
This file also logs the incoming data into a database.

In `reply.py` we classify the kind of query and send a request to the corresponding api by using `apihandler.py`.
It is mostly hardcoded stuff in here as of now but once we can implement NLP it could be much better.

The file `apihandler.py` is used to communicate to the base level api and return the result in a [{answer, type(image/text)}] format to `reply.py`

> Alll the apis are to be implemented in `eywa/ai/apis/`

Tracing it back up, all apis return the result to `apihandler.py` which formats the result to the necessary format and sends it over to `reply.py`
`reply.py` aggregates all these results and then send it over to `consumers.py`. In here we format it in json format appending the result over with the query and sends it back to the user though the same WebSocket connection.

## Screenshot
### ! Web
![web](http://i.imgur.com/0f7OhkO.png)
### ! Mobile
![mobile](http://i.imgur.com/CFQZ0s5.png)
