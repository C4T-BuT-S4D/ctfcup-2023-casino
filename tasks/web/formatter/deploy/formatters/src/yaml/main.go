package main

import (
	"bufio"
	"os"
)

// TODO: properly format YAML
func main() {
	r := bufio.NewReader(os.Stdin)

	path, err := r.ReadString('\n')
	if err != nil {
		os.Exit(1)
	}

	input, err := os.ReadFile(path[:len(path)-1])
	if err != nil {
		os.Exit(1)
	}

	_, _ = os.Stdout.Write(input)
}
