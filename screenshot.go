package main

import (
    "context"
    "encoding/json"
    "log"
    "os"
	"path/filepath"
    "runtime"
    "strings"
    "sync"
    "time"
	"math/rand"

    "github.com/chromedp/chromedp"
)

const domainListFolder string = "data/list"
const screenshotDir string = "./data/images"

const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

var seededRand *rand.Rand = rand.New(rand.NewSource(time.Now().UnixNano()))


func main() {
    jsonFiles, err := getJSONFiles(domainListFolder)
    checkError(err, "Error fetching JSON files")

    maxWorkers := runtime.NumCPU()
    runtime.GOMAXPROCS(maxWorkers)

    var wg sync.WaitGroup
    semaphore := make(chan struct{}, maxWorkers)

  bufPool := sync.Pool{
        New: func() interface{} {
            return make([]byte, 0, 1024*1024) // Adjust the size according to your needs
        },
    }

    for _, file := range jsonFiles {
        domains, err := readdomains(file)
        checkError(err, "Error reading domains from JSON file: "+file)

        wg.Add(len(domains))

        for _, domain := range domains {
            domain := domain // Create a local copy for the goroutine

            semaphore <- struct{}{}

            go func() {
                defer func() {
                    <-semaphore
                    wg.Done()
                }()

                ctx, cancel := chromedp.NewContext(context.Background())
                defer cancel()

                ctx, cancel = context.WithTimeout(ctx, 2*time.Minute)
                defer cancel()

                buf := bufPool.Get().([]byte)
				defer bufPool.Put(buf[:0])

                fullURL :=  domain 
                res := make([]byte, 0)

                if err := chromedp.Run(ctx, screenshot(ctx, fullURL, &res)); err != nil {
                    log.Printf("Error capturing screenshot for %s: %v", domain, err)
                    return
                }

                fileName := generateFileName(domain)
                if err := os.WriteFile(fileName, res, 0644); err != nil {
                    log.Printf("Error saving screenshot for %s: %v", domain, err)
                    return
                }

                log.Printf("Screenshot captured for %s and saved as '%s'", domain, fileName)
            }()
        }
    }

    wg.Wait()
    log.Println("All screenshots captured")
}


func getJSONFiles(folderPath string) ([]string, error) {
	var jsonFiles []string

	err := filepath.Walk(folderPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && strings.HasSuffix(info.Name(), ".json") {
			jsonFiles = append(jsonFiles, path)
		}

		return nil
	})

	if err != nil {
		return nil, err
	}

	return jsonFiles, nil
}



func generateRandomID(length int) string {
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[seededRand.Intn(len(charset))]
	}
	return string(b)
}

func generateFileName(domainURL string) string {
	// Remove the protocol and split the URL by '/'
	// Remove the protocol and split the URL by '/'
	parts := strings.Split(strings.TrimPrefix(domainURL, "https://"), "/")
	if len(parts) == 1 { // If "https://" prefix is not found, try with "http://"
		parts = strings.Split(strings.TrimPrefix(domainURL, "http://"), "/")
	}

	// Get the first part of the URL (domain)
	domain := strings.Split(parts[0], ".")
	if len(domain) < 2 {
		return filepath.Join(screenshotDir, generateRandomID(6) + ".png");
	}

	tld := domain[len(domain)-1]
	domainName := strings.Join(domain[:len(domain)-1], "_")
	randomID := generateRandomID(4)

	return filepath.Join(screenshotDir, domainName+"_"+randomID+"_"+tld+".png")
}



func screenshot(ctx context.Context, urlstr string, res *[]byte) chromedp.Tasks {
    return chromedp.Tasks{
        chromedp.Navigate(urlstr),
        chromedp.CaptureScreenshot(res),
    }
}

func readdomains(filename string) ([]string, error) {
    file, err := os.Open(filename)
    if err != nil {
        return nil, err
    }
    defer file.Close()

    var domains []string
    if err := json.NewDecoder(file).Decode(&domains); err != nil {
        return nil, err
    }

    return domains, nil
}

func checkError(err error, message string) {
    if err != nil {
        log.Fatalf("%s: %v", message, err)
    }
}