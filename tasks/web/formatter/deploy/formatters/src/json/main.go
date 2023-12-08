package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"os"
)

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

	output := bytes.NewBuffer(nil)
	if err := json.Indent(output, input, "", "  "); err != nil {
		os.Exit(1)
	}

	_, _ = os.Stdout.Write(output.Bytes())
}
