<h1>RocketDBaaS Database UI & API / EPICs</h1>


URL Base: http://RocketDBaaS.??????.com


<h2> What do I need to be able to do</h2>

* Pushing out changes to all PostgreSQL or MongoDB servers.  
    * So I need a list of all Active & PostgreSQL 
    * GET: /api/{dbmsType}/clustersServers/
    * POST: /api/{dbmsType}/clustersServers/
    
* Create a list of PoolServers that will later be used to build out clusters
    * POST: /api/{dbmsType}/poolServers
    * DELETE: /api/{dbmsType}/poolServers
    
* Pull & Update new servers from the PoolServer making them used
    * GET: /api/{dbmsType}/poolServersPullAndLock/{numberOfServers}?cpu={}&ram={}&dbGigs={}
        * Updates it as Locked
    * PATCH: /api/{dbmsType}/poolServers/{ServerName}
        * Updates it as Used or Free if a failure

* Create a new Cluster with object that is Application, Cluster, Servers) 
    * POST: /api/{dbmsType}/Cluster
* Get details on a Cluster
    * GET: /api/{dbmsType}/Cluster/{ClusterName}
    
    
<h2> What do I want </h2>

* Patch Clusters in a Rolling fashion
    * Run against servers in a rolling manner
    * Update tables 
        * server is being patch
        * patch version
        * Patch Type (DB/OS)
        * Outcome
        * Store details of patch output

* Contacts for given Applications
    * Create/Update/Expire Contacts
    * Link Applications and 1 or more Contacts
    * Update Patching statuses to email Contacts
    * /api/contacts/

* A way to track activities that happen to a cluster (ie. Audit Log)
    * /api/{dbmsType}/activities/
    * Examples: Failover, Down, Up, Patch, DbRestart, ServerRestart
    * For unplained events it would be nice to be able to put in a link to a ticket

* Store backup details
    * Store backups info like backupType, status, DbSizeGigs, BkupSizeGigs, start, stop
    * Roll them off when valid to do so

* Webpage for the intake form so we can use and referrence it easier

<h2> Future Goals <h2>

* Produce a few reports or website, probably broken down by database type
    * Number of DBs
    * Size of DBs & trends
    * Size of Backups & trends
    * Unplaned Failovers
    * Downtime percents
    * Unpatched Servers/Clusters counts
    * Page showing costs per Application

* Allow users to
    * Have a dashboard of their databases
    * Allow them to sign up contacts