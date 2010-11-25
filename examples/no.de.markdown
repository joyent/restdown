# Joyent API

    restdown TODO:

    - definition lists (have support for those? PHP Markdown? RDiscount?)
    - need the metadata? e.g. "{endpoint}"


## Welcome

All API calls start with

<pre class="important">
https://api.no.de
</pre>

Path:
    For this documentation, we will assume every request begins with the above path.
Format:
    All calls are returned in JSON.
Status Codes:
    - 200 Successful GET and PUT.
    - 201 Successful POST.
    - 202 Successful Provision queued.
    - 204 Successful DELETE
    - 401 Unauthenticated.
    - 409 Unsuccessful POST, PUT, or DELETE (Will return an errors object)

## Account

### GET /account  {endpoint}


