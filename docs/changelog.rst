Changelog
=========

.. hint::
    What "previous revision ID" means? 
    If you are updating the package that never was stamped with 
    alembic you may need to stamp the database manually with following revision id, 
    from this point onwards you will be able to update schemas automaticly.
    Alembic 0.3.3+ (or current trunk for 2012-05-27) is required for this to function properly


2012-11-28 version 0.3 First Alpha release
-------------------------------------------
* This release should have a fairly stable API
* Hundreds of small and big changes - based on all great feedback we are now 
  using surrogate pkeys instead of natural pkeys for most models. 
  As result of this few methods started accepting id's instead usernames, 
  so consider yourself warned that this release might be bw. incompatible a bit 
  with your application
* At this point all tests should pass on mysql, postgresql, sqlite


2012-05-27 version 0.2 First public release
-------------------------------------------

* added proper alembic(pre 0.3.3 trunk) support for multiple alembic migrations via separate versioning table
* please do manual stamp for CURRENT revision ID: 54d08f9adc8c
* changes for first public pypi release
* Possible backwards incompatibility: Remove cache keyword cruft


2012-05-25
----------

* Possible backwards incompatibility: Remove invalidate keyword cruft

2012-03-10
----------

* Add registration date to user model, changed last_login_date to no-timezone type (this seem trivial enough to not faciliate schema change) 
* previous revision ID: 2d472fe79b95

2012-02-19
----------
* Made external identity fields bigger
* previous revision ID: 264049f80948

2012-02-13
----------
* Bumped alembic machinery to 0.2
* Enabled developers to set their own custom password managers
* added ordering column for resources in tree
* Stubs for tree traversal
* previous revision ID:  46a9c4fb9560

2011-12-20
----------
* Made hash fields bigger
* previous revision ID: 5c84d7260c5

2011-11-15
----------
* Added ExternalIdentityMixin - for storing information about user profiles connected to 3rd party identites like facebook/twitter/google/github etc.
* previous revision ID: 24ab8d11f014

2011-11-03
----------
* added alembic migration support
* previous revision ID: 2bb1ba973f0b

2011-08-14
----------
* resource.users_for_perm(),  resource.direct_perms_for_user() and resource.group_perms_for_user() return tuple (user/group_name,perm_name) now