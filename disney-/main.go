package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type Video struct {
	Title string `json:"title"`
	Path  string `json:"path"`
	Group string `json:"group"`
}

const htmlTemplate = `
<!DOCTYPE html>
<html>
<head>
    <title>Disney Minus (Text Only)</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        a { color: #0f0; text-decoration: none; }
        a:hover { background: #0f0; color: #000; }
        h1 { border-bottom: 1px solid #0f0; padding-bottom: 10px; }
        .group { margin-top: 20px; color: #ff0; }
        ul { list-style: none; padding-left: 0; }
        li { margin-bottom: 5px; }
        .vlc { margin-left: 10px; font-size: 0.8em; color: #aaa; }
    </style>
</head>
<body>
    <h1>DISNEY MINUS - Text Media Browser</h1>
    {{range $group, $vids := .}}
        <div class="group">[{{$group}}]</div>
        <ul>
            {{range $vids}}
                <li>
                    <a href="/{{.Path}}">{{.Title}}</a>
                    <a class="vlc" href="vlc://http://localhost:8001/{{.Path}}">[VLC]</a>
                </li>
            {{end}}
        </ul>
    {{end}}
    <footer style="margin-top: 50px; font-size: 0.7em; color: #555;">
        VLC links may require a protocol handler or browser extension.
    </footer>
</body>
</html>
`

func getVideos() ([]Video, error) {
	var videos []Video
	root := "./data"

	err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			ext := strings.ToLower(filepath.Ext(path))
			if ext == ".mkv" || ext == ".mp4" || ext == ".webm" {
				relPath, _ := filepath.Rel(".", path)

				// Group by parent folder name
				parent := filepath.Base(filepath.Dir(path))
				if parent == "data" {
					parent = "Movies"
				}

				videos = append(videos, Video{
					Title: info.Name(),
					Path:  relPath,
					Group: parent,
				})
			}
		}
		return nil
	})
	return videos, err
}

func main() {
	// Serve video files directly
	http.Handle("/data/", http.FileServer(http.Dir(".")))

	// Main text-based UI
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}

		videos, err := getVideos()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// Group videos
		groups := make(map[string][]Video)
		for _, v := range videos {
			groups[v.Group] = append(groups[v.Group], v)
		}

		tmpl, _ := template.New("index").Parse(htmlTemplate)
		tmpl.Execute(w, groups)
	})

	// API for TUI
	http.HandleFunc("/api/videos", func(w http.ResponseWriter, r *http.Request) {
		videos, err := getVideos()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		json.NewEncoder(w).Encode(videos)
	})

	fmt.Println("Disney Minus backend starting on http://localhost:8001")
	log.Fatal(http.ListenAndServe(":8001", nil))
}
