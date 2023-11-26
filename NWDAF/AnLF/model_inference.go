package main

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"
)

type Payload struct {
	T              int     `json:"t"`
	CellId         int     `json:"cell_id"`
	CatId          int     `json:"cat_id"`
	PeId           int     `json:"pe_id"`
	Load           float64 `json:"load"`
	HasAnomaly     bool    `json:"-"`
	Last2mean      float64 `json:"last2_mean"`
	PerChangeLast2 float64 `json:"per_change_last2"`
	PerChangeLast3 float64 `json:"per_change_last3"`
	PerChangeLast4 float64 `json:"per_change_last4"`
}

func handler(rw http.ResponseWriter, req *http.Request) {
	fmt.Println("Inference request:")
	fmt.Println("Method : ", req.Method)

	b, _ := io.ReadAll(req.Body)
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

func countLines(filePath string) (int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return 0, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	lineCount := 0

	for scanner.Scan() {
		lineCount++
	}

	if err := scanner.Err(); err != nil {
		return 0, err
	}

	return lineCount, nil
}

func readCsvFile(filePath string, line int) Payload {
	f, err := os.Open(filePath)
	if err != nil {
		log.Fatal("Unable to read input file "+filePath, err)
	}
	defer f.Close()

	var result Payload
	count := 0

	r := csv.NewReader(f)
	for {
		record, err := r.Read()

		count++

		if err == io.EOF {
			break
		}

		if count != line {
			continue
		}

		if err != nil {
			panic(err)
		}

		T, _ := strconv.Atoi(record[0])
		CellId, _ := strconv.Atoi(record[1])
		CatId, _ := strconv.Atoi(record[2])
		PeId, _ := strconv.Atoi(record[3])
		Load, _ := strconv.ParseFloat(record[4], 64)
		HasAnomaly, _ := strconv.ParseBool(record[5])
		Last2mean, _ := strconv.ParseFloat(record[6], 64)
		PerChangeLast2, _ := strconv.ParseFloat(record[7], 64)
		PerChangeLast3, _ := strconv.ParseFloat(record[8], 64)
		PerChangeLast4, _ := strconv.ParseFloat(record[9], 64)

		result = Payload{
			T,
			CellId,
			CatId,
			PeId,
			Load,
			HasAnomaly,
			Last2mean,
			PerChangeLast2,
			PerChangeLast3,
			PerChangeLast4,
		}
	}

	return result
}

func getRandomPayload() Payload {
	filePath := "../data/nwdaf_data_processed.csv"

	lineCount, err := countLines(filePath)
	if err != nil {
		log.Fatal("Error:", err)
	}

	min := 1
	max := lineCount
	randomValue := rand.Intn(max-min+1) + min

	record := readCsvFile(filePath, randomValue)

	return record
}

func requestModelTraining(reqNfInstanceId string) {
	jsonBody := map[string]interface{}{}
	jsonBody["reqNFInstanceID"] = reqNfInstanceId
	jsonBody["nfService"] = "inference"
	now_t := time.Now().Format("2006-01-02 15:04:05")
	jsonBody["reqTime"] = now_t
	payload := getRandomPayload()
	jsonBody["data"] = payload
	jsonStr, _ := json.Marshal(jsonBody)

	fmt.Println("JSON request: ", string(jsonStr))
	fmt.Println("*********")
	resp, err := http.Post("http://localhost:9537", "application/json; charset=UTF-8", bytes.NewBuffer([]byte(jsonStr)))
	if err != nil {
		log.Fatal("error: ", err)
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
