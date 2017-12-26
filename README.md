__Please be aware that this is highly incomplete and many of this document act's as a brain-dump for me__

# FairySearch

A simple FTP Search engine with the intention to run in a local environment with many FTP Servers (like Chaos Events).

Currently only the Network will be searched for FTP Servers, and then for each found host the file-list is recursively fetched and saved to a MongoDB instance.

For scanning the Network I use nmap, so if you like to run this on your machine, please ensure that nmap is installed.

## Limitations
I suppose that there's a major flaw in the way I traverse recursively trough directories.
If there is anywhere a symlink folder which points to a/the parent directory, the algorithm is likely to traverse endless trough the loop, until the maximum stack size is reached and the python interpreter crashes.
I plan to implement prevention for this in the near future, but for the moment: Please be patient.

## Architectural Overview
This is currently under heavy development, so please don't judge me if this is outdated or wrong

My initial idea for implementing this was a distributed microservice architecture, where individual ftp_walker are spawned within docker container so they could be easily scaled up in a huge dockerswarm. Also I initially wanted to have as much as possible asynchronous to speed things up.

Currently I didn't manage to met my own acceptance criteria since I didn't found that much time for this project than I thought.
As of now (Dec/26/2017) the architecture is a bit limited:
The Network-Scanner (can be found in [network_scan.py][7]) runs async and then calls a callback for each found up host.
Then for each found up host I start a sync port-scanner to check for open ports.
I decided split these two steps, to speed up the host-discovery.
After a suitable server is found (a server with open Port 21) I start traversing trough the directory tree and fill an array with all found files.
After the `ftp_walker` is done I save the directory tree to MongoDB using [database.py][6], currently by using two collections.
1. `ftp_servers` which holds a list of all found ftp server and the associated port(s)
2. `file_list` an array of files, represented as dictionarys, like the example shown below.

### MongoDB
Like mentioned earlier I use MongoDB to store the files. Since I plan to use microservices whenever possible within this project I decided to run MongoDB inside a docker container.
This comes with the beauty of easily creating many mongo instances and cluster them together.
To spawn a MongoDB with docker use:

	docker pull mongo:latest # pull the latest mongo docker container from dockerhub
	docker run -v "$(pwd)/mongo" -t -i -p 27019:27017 --name mongo -d mongo mongod --smallfiles --bind_ip 0.0.0.0 --noauth

I know that I currently use `--noauth`, this is planned to be changed in the near future

Let's talk about the document structure:

#### ftp_server

	{
		"_id" : ObjectId("5a423094a735c340919c049b"),
		"host" : "1.2.3.4",
		"ports" : [ 21, 4444 ]
	}


#### file_list

	{
		"_id" : ObjectId("5a423094a735c340919c04ac"),
		"filename" : "5MB",
		"server" :
		[
			{
				"url" : "1.2.3.4",
				"port" : 21,
				"extension" : ".zip",
				"path" : "5MB.zip",
				"scan_date" : 1514287252.0955296
			},
			{
				"url" : "1.2.3.4",
				"port" : 31,
				"extension" : ".zip",
				"path" : "5MB.zip",
				"scan_date" : 1514287252.116543
			},
			{
				"url" : "4.5.6.7",
				"port" : 21,
				"extension" : ".zip",
				"path" : "5MB.zip",
				"scan_date" : 1514287252.1361535
			}
		]
	}


## Install

### Dependencies
1. [nmap][1] (used for host discovery and port scanning)
2. [docker][2] (used for mongodb)
3. [python-nmap][3] (python API for nmap) `pip install python-nmap`

I try to keep the [requirements.txt][4] up to date, but it's likely that it's not, since i'm super lazy... :D

## Bugs
If you find bugs, feel free to report them [here][5].


[1]: https://nmap.org/
[2]: https://www.docker.com/
[3]: https://pypi.python.org/pypi/python-nmap
[4]: requirements.txt
[5]: https://github.com/cedi/FairySearch/issues
[6]: database.py
[7]: network_scan.py
