#HOMEWORK

##Assumptions

- Listing can be huge and the listing and has to be fast if used by a webapp. I try to avoid table scan and using a btree index no matter the params searched. It will have the downside of a bigger database
- Id are incremental so we can use an cursor as efficient alternative to offset for pagination: [no-offset](http://use-the-index-luke.com/no-offset)
- Because status is not part of the property. I assumed that we return the `active` listings by default.
- Because we have coordinates, then I used them as GIS
- At least 1 bedroom and 1 bathroom for filtering and database integrity constraints
- Price are integer and won't have house price with floating point


##Comments

- Keep id as SERIAL as the csv as only integer val.
- DeclEnum is a recipe that I reused many times to avoid the use of db enum because dbenum can be really annoying to ALTER
- The fact that id is included in the CSV then it implies that we can run into race condition during insert due to the unique constraint on the PK. Usually, we would be using the default value for the id during insert which is 'sequence.next_val()' and because sequence are non transationnal we wouldn't hit the race condition problem during insert with unique constraint (more about this [here](http://rachbelaid.com/handling-race-condition-insert-with-sqlalchemy))
- I didn't added migrations support as it's the first version, if db changes was required then I will be using alembic support
- I didn't add extra logging but I would be using probably structlog to have contextual logging
- I didn't pin the dependencies but it will be something that I will on production project

##Installation


    python setup.py develop


##Database Setup

This project use PostgreSQL

###Create the DB

```
createuser -s homework # -s required as we are going to use the same role to create extensions
createdb --owner homework homework
initialize_db development.ini
```

###Populate the DB

```
populate_db development.ini
```

##Running the tests

    python setup.py test

##Extra

As I decided to return only the active listing per default.
You can filter per status or ask to receive them all.

    curl "/listings?status=sold"
    curl "/listings?status=all"

I used cursor base pagination (see Links header):

    curl "/listings?after=9"
    curl "/listings?before=9"

As we have GIS data, I added a filter per distance (in km)

    curl "/listings?coord=-112.1151215344,-33.4767593059&distance=1"
