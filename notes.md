Ignore articles that the user reads after registration.

Ignore non-articles like crosswords.

Count each article once only. If an article appears twice for the same user, assume this is because they are navigating through their web history and they did not read the same article again.

Assue that each page_url is associated with only one name. That is, if a page_name changes (e.g. because the headline changes), but the url is still the same, count these separately.