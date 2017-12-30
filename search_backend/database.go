package main

import (
	"fmt"
	"gopkg.in/mgo.v2"
	"gopkg.in/mgo.v2/bson"
	"log"
	"os"
)

type ftp_server struct {
	Host  string
	Ports []int
}

type server struct {
	Url       string
	Port      int
	Extension string
	Path      string
	Scanned   int
}

type file_list struct {
	Filename string
	Server   []server
}

func GetAllFtpServer() []ftp_server {
	session, err := mgo.Dial("mongodb://127.0.0.1:27019")
	if err != nil {
		panic(err)
	}
	defer session.Close()

	c := session.DB("metadata").C("ftp_server")

	result := []ftp_server{}
	err = c.Find(bson.M{}).All(&result)
	if err != nil {
		log.Fatal(err)
	}

	return result
}

func GetFilesByName(name string) []file_list {
	session, err := mgo.Dial("mongodb://127.0.0.1:27019")
	if err != nil {
		panic(err)
	}
	defer session.Close()

	c := session.DB("metadata").C("file_list")

	result := []file_list{}
	err = c.Find(bson.M{"filename": name}).All(&result)
	if err != nil {
		log.Fatal(err)
	}

	return result
}

func printHelp() {
	fmt.Println("*** FairySearch search utility ***")
	fmt.Println("ftp_server		get all ftp-server from the mongo backend")
}

func main() {
	fmt.Println("*** FairySearch search utility ***")

	for index, element := range os.Args {
		if "ftp_server" == element {
			server := GetAllFtpServer()
			fmt.Println(server)
		}
		if "file_list" == element {
			file_list := GetFilesByName(os.Args[index+1])
			fmt.Println(file_list)
		}
		if "help" == element {
			printHelp()
		}
	}
}
