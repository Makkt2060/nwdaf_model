package main

import (
	"bytes"
	"errors"
	"fmt"
	"io/ioutil"
	"net/http"
)

func handler(rw http.ResponseWriter, req *http.Request) {
	fmt.Println("Method : ", req.Method)

	b, _ := ioutil.ReadAll(req.Body)
	defer req.Body.Close()
	fmt.Println("Body : ", string(b))
	fmt.Println("Request transferred")
	switch req.Method {
	case "POST":
		rw.Write([]byte("post request success !"))
		buff := bytes.NewBuffer(b)
		resp, err := http.Post("http://localhost:5000", "application/json", buff)
		if err != nil {
			panic(err)
		}

		data, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			panic(err)
		}
		resp.Body.Close()
		fmt.Printf("success: %s\n", string(data))

		buff = bytes.NewBuffer(data)
		resp, err = http.Post("http://localhost:9536", "application/json", buff)
		if err != nil {
			panic(err)
		}
		resp.Body.Close()
	case "GET":
		rw.Write([]byte("get request success !"))
	}
}

func main() {
	port := 9537
	fmt.Printf("Listen on port: %d \n\n", port)
	err := http.ListenAndServe(fmt.Sprintf("%s%d", ":", port), http.HandlerFunc(handler))
	if errors.Is(err, http.ErrServerClosed) {
		fmt.Printf("server closed\n")
	} else if err != nil {
		fmt.Printf("error listening for server: %s\n", err)
	}
}
