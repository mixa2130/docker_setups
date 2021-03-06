# MongoDB

It's a NoSQL solution that allows us to store data in collections that are made up of documents.

## Console

Connection in docker cli:

~~~bash
> mongo -u gree -p 8771
> show dbs
admin 0.000GB
local  0.000GB
~~~

There is no “create” command in the MongoDB shell. In order to create a database, you will first need to switch the
context to a non-existing database using the use command:

~~~bash
> use tests
~~~

Note that for now, **only the context has been changed**. If you enter the show dbs command, the result should still be
the same:

~~~bash
> show dbs
admin 0.000GB
local  0.000GB
~~~

Wait a second. Where’s tests?

MongoDB only creates the database when you first store data in that database. This data could be a collection or even a
document.

To add a document to your database, use the db.collection.insert() command.

~~~bash
> db.user.insertOne({name: "Ada Lovelace", age: 205})
WriteResult({ "nInserted" : 1 })
~~~

A couple of notes. The “user” in the command refers to the collection that the document was being inserted in.
Collections in MongoDB are like tables in a SQL database, but they are groups of documents rather than groups of
records.