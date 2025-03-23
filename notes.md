### Assumptions

Ignore articles that the user reads after registration has taken place.

Ignore non-articles like crosswords.

Count each article once only. If an article appears twice for the same user, assume this is because they are navigating through their web history and they did not read the same article again.

Assue that each page_url is associated with only one name. That is, if a page_name changes (e.g. because the headline changes), but the url is still the same, count these separately.

Assume that it is not possible to have data that shows a customer registers twice - but if there is only consider data before the first registration.


### Considerations

The pipeline intends to enable stakeholders to see the exact articles that users are reading before registering in the past day. Therefore assume that the hitlog file is refreshed daily and only contains data from the past 24 hours.  If this is not the case and we want to consider a larger time horizon, the pipeline will still run but the test test_timestamps will fail.


### Next steps

Other things that would be required to put this pipeline into production.

#### 1) Further testing of logic
Considering additional edge-cases. E.g. if a user views a page and immediately returns to the homepage does that consitiute a read article.

#### 2) Better logging
To identify where a failed run breaks down. As this is a smaller task I have used only simple error handling.

#### 3) Deployment
Use a tool like Airflow for scheduling and monitoring runs.