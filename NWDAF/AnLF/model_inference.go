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

type Payload struct {
  CellId float32 `json:"cell_id"`
  CatId float32 `json:"cat_id"`
	PeId float32  `json:"pe_id"`
	Load float32 `json:"load"`
	Last2mean float32 `json:"last2_mean"`
	PerChangeLast2 float32 `json:"per_change_last2"`
	PerChangeLast3 float32 `json:"per_change_last3"`
	PerChangeLast4 float32 `json:"per_change_last4"`
}

func handler(rw http.ResponseWriter, req *http.Request) {
	fmt.Println("Inference request:")
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
	jsonBody["nfService"] = "inference"	
	now_t := time.Now().Format("2006-01-02 15:04:05")
	jsonBody["reqTime"] = now_t
	payload := Payload{
		CellId: 2,
		CatId: 2,
		PeId: 4,
		Load: 5.976979,
		Last2mean: 5.981692,
		PerChangeLast2: 0.402706,
		PerChangeLast3: -1.985990,
		PerChangeLast4: -3.211737,
	}
	jsonBody["data"] = payload
	jsonStr, _ := json.Marshal(jsonBody)

	fmt.Println("JSON request: ", string(jsonStr))
	fmt.Println("*********")
	resp, err := http.Post("http://localhost:9537", "application/json; charset=UTF-8", bytes.NewBuffer([]byte(jsonStr)))
	if err != nil {
		log.Fatal("error: %v", err)
	} else {
		fmt.Println("Header: ", resp.Header)
		fmt.Println("************")
		fmt.Println("Resp: ", resp)
		fmt.Println("************")
		respBody, _ := ioutil.ReadAll(resp.Body)
		jsonData := map[string]interface{}{}
		json.Unmarshal(respBody, &jsonData)
		fmt.Println(jsonData)
	}
}

func main() {
	go requestModelTraining("NF-Function(inference)")
	go http.ListenAndServe(":9536", http.HandlerFunc(handler))

	select {
	case <-time.After(time.Second * 20):
		os.Exit(0)
	}
}

