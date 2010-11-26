---
title: Joyent API
---

# Joyent API

<div class="basic_info" markdown="1">
#### All API calls start with

<pre class="base important">
https://api.no.de
</pre>

#### Path

For this documentation, we will assume every request begins with the above path.

#### Format

All calls are returned in **JSON**.

#### Status Codes

- **200** Successful GET and PUT.
- **201** Successful POST.
- **202** Successful Provision queued.
- **204** Successful DELETE
- **401** Unauthenticated.
- **409** Unsuccessful POST, PUT, or DELETE (Will return an errors object)
</div>



# Account

## GET /account

Expects basic auth to get an existing customer. API will return **200**.

##### example request

    $ curl -k -u jill:secret https://api.no.de/account

##### response

    {
      "username": "jill",
      "first_name": "Jill",
      "last_name": "Doe",
      "company": "Joyent",
      "email": "jill@joyent.com"
    }
