# Pretty REST API docs authored in Markdown

1. Write a Markdown file that describes your REST API -- with some light
   conventions (see "Conventions" below) to structure to your doc file. E.g.:
   
        $ cat api.restdown    # or api.md or index.markdown whatever
        ---
        title: My Awesome REST API
        ---
        
        # My Awesome REST API
        
        Some introduction...
        
        # Wuzzers
        
        ## GET /wuzzers
        
        ...

        ## POST /wuzzers
        
        ...

2. Run it through `restdown` and out pops (a) "api.html", fairly light semantic
   HTML5 for your API; and (b) "api.json", a JSON representation of your API.
   
        $ restdown -m STATICDIR api.restdown

   where "STATICDIR" is a path to your static content served dir.

You should now have pretty decent looking REST API docs.



# Conventions in Restdown content

- The first `h1` is the API title, and its body is an introduction to the API.
- Subsequent `h1`'s are API section titles. If your whole API is one logical
  grouping then you might need that second `h1` anyway. This should be fixed
  if that is the case.
- `h2`'s are API endpoints of the form "HTTP-VERB URL-PATH". For example:
  `GET /widgets/:id`. This format is not required though.
- `h3`'s are just normal subsection headers within endpoints, if needed for
  longer documentation for a particular endpoint.
- `h4`'s are typically for showing example request and response output for
  an endpoint. A `pre`-block inside an `h4` will get a CSS class.


# Brands

A "brand" is a directory with all of the styling (CSS, JS, images) for a
restdown-created .html file. The default brand is called "ohthejoy". It was
originally derived from the styling of <https://api.no.de>. I should add more.

The idea is that you can start with the brand here and tweak it to create your
or style. You can use your own brand files (for your own HTML/CSS/image
tweaks). Start by copying one of the brands in the restdown/brands directory
and then use the "-b|--brand" option to restdown.


# api.json

The generated "api.json" file currently looks like this:

    {
      "endpoints": [
        "GET    /wuzzers", 
        "POST   /wuzzers", 
        "DELETE /wuzzers",
        ...
      ]
    }

This might or might not be useful to you. For example, a request to
<https://api.no.de/> without "Accept: text/html" will return JSON similar to this:

    $ curl https://api.no.de/
    {
      "endpoints": [
        "GET  /",
        "GET  /account",
        "PUT  /account",
        "GET  /sshkeys",
        ...
      ]
    }

If you swing with the [expressjs](http://expressjs.com) crowd, here is how I
typically wire this into my project:

    app.get('/', function(req, res) {
      var accept = req.header("Accept");
      if (accept && (accept.search("application/xhtml+xml") != -1
                     || accept.search("text/html") != -1)) {
        res.sendfile(__dirname + "/docs/api.html");
      } else {
        res.header("Content-Type", "application/json");
        res.sendfile(__dirname + "/docs/api.json");
      }
    });

