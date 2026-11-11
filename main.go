// Übungs-Buddy: kleiner lokaler Webserver + Browser als Oberfläche.
// Daten liegen als uebungen.json neben der exe.
package main

import (
	_ "embed"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
)

//go:embed index.html
var page []byte

//go:embed seed.json
var seed []byte

const addr = "127.0.0.1:47811"

func openBrowser() {
	url := "http://" + addr
	if runtime.GOOS == "windows" {
		exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	} else {
		exec.Command("xdg-open", url).Start()
	}
}

func main() {
	exe, _ := os.Executable()
	file := filepath.Join(filepath.Dir(exe), "uebungen.json")

	ln, err := net.Listen("tcp", addr)
	if err != nil { // läuft schon -> nur Browser öffnen
		openBrowser()
		return
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Write(page)
	})
	http.HandleFunc("/api", func(w http.ResponseWriter, r *http.Request) {
		// Nur die eigene Seite darf lesen/schreiben (kein DNS-Rebinding, kein CSRF).
		if r.Host != addr {
			http.Error(w, "forbidden", 403)
			return
		}
		if r.Method == "POST" {
			if r.Header.Get("Content-Type") != "application/json" {
				http.Error(w, "forbidden", 403)
				return
			}
			body, err := io.ReadAll(http.MaxBytesReader(w, r.Body, 200<<20))
			if err != nil || !json.Valid(body) {
				http.Error(w, "bad json", 400)
				return
			}
			// erst temp schreiben, dann umbenennen: kein halber Datenpool bei Absturz
			if err := os.WriteFile(file+".tmp", body, 0644); err == nil {
				err = os.Rename(file+".tmp", file)
			}
			if err != nil {
				http.Error(w, err.Error(), 500)
			}
			return
		}
		data, err := os.ReadFile(file)
		if err != nil {
			data = seed
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(data)
	})

	fmt.Println("Übungs-Buddy läuft: http://" + addr)
	fmt.Println("Daten: " + file)
	fmt.Println("Dieses Fenster schließen, um das Programm zu beenden.")
	openBrowser()
	http.Serve(ln, nil)
}
