package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"io"
	"os"
)

func main() {
	r := bufio.NewReader(os.Stdin)

	input, err := io.ReadAll(r)
	if err != nil {
		os.Exit(1)
	}

	output := bytes.NewBuffer(nil)
	if err := json.Indent(output, input, "", "  "); err != nil {
		os.Exit(1)
	}

	_, _ = os.Stdout.Write(output.Bytes())
}
