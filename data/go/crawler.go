package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
	"github.com/PuerkitoBio/goquery"
)



func main() {
	file, err := os.Open("../list/list.json")
	if err != nil {
		fmt.Printf("Failed to open JSON file: %v\n", err)
		return
	}
	defer file.Close()

	var urls []string
	err = json.NewDecoder(file).Decode(&urls)
	if err != nil {
		fmt.Printf("Failed to decode JSON: %v\n", err)
		return
	}

	for _, url := range urls {
		err := downloadImagesFromURL(url)
		if err != nil {
			fmt.Printf("Error downloading images from %s: %v\n", url, err)
		}
	}
}

func downloadImagesFromURL(url string) error {
	req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        return fmt.Errorf("Failed to create HTTP request: %v", err)
    }

    // Set the User-Agent header
    req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0")

    // Set the Referer header
    req.Header.Set("Referer", "https://duckduckgo.com")

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return fmt.Errorf("Failed to fetch the URL %s: %v", url, err)
    }
    defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return fmt.Errorf("Failed to parse HTML from %s: %v", url, err)
	}

	foundImages := false

	doc.Find("img").Each(func(i int, s *goquery.Selection) {
		imgSrc, exists := s.Attr("src")
		if exists {
			foundImages = true
			downloadImage(imgSrc)
		}
	})

	if !foundImages {
		fmt.Println("No images found on", url)
	}

	// Delay before the next request to avoid overloading the server
	time.Sleep(2 * time.Second) // Adjust the delay time as needed

	return nil
}

func downloadImage(url string) {
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("Failed to download image: %v\n", err)
		return
	}
	defer resp.Body.Close()

	fileName := getFileNameFromURL(url)
	file, err := os.Create("../../model/labeled/good/"+fileName)
	if err != nil {
		fmt.Printf("Failed to create file: %v\n", err)
		return
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		fmt.Printf("Failed to save image: %v\n", err)
		return
	}

	fmt.Printf("Image downloaded: %s\n", fileName)
}

func getFileNameFromURL(url string) string {
	split := strings.Split(url, "/")
	fileName := split[len(split)-1]
	return fileName
}
