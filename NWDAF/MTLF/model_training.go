package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

func handler(w http.ResponseWriter, req *http.Request) {
	fmt.Println("Training response:")
	fmt.Println("Method : ", req.Method)

	b, _ := ioutil.ReadAll(req.Body)
	defer req.Body.Close()

	var prettyJSON bytes.Buffer
	error := json.Indent(&prettyJSON, b, "", "\t")
	if error != nil {
		log.Fatal("JSON parse error: ", error)
		return
	}

	fmt.Println("body:", string(prettyJSON.Bytes()))
	fmt.Println("Request transferred!\n")
}

func requestModelTraining(reqNfInstanceId string) {
	jsonBody := map[string]interface{}{}
	jsonBody["reqNFInstanceID"] = reqNfInstanceId
	jsonBody["nfService"] = "training"
	now_t := time.Now().Format("2006-01-02 15:04:05")
	jsonBody["reqTime"] = now_t
	jsonBody["data"] = "None"
	jsonStr, _ := json.Marshal(jsonBody)
	//print("*********")
	resp, err := http.Post("http://localhost:9537", "application/json; charset=UTF-8", bytes.NewBuffer(jsonStr))
	if err != nil {
		log.Fatal("error: %v", err)
	} else {
		fmt.Println("Header: ", resp.Header)
		fmt.Println("************")
		fmt.Println("Resp: ", resp)
		fmt.Println("************")
	}
}

func main() {
	go requestModelTraining("NF-Function(training)")
	go http.ListenAndServe(":9536", http.HandlerFunc(handler))

	select {
	case <-time.After(time.Second * 20):
		os.Exit(0)
	}
}

