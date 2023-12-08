package main

import (
	"bufio"
	"os"

	"gopkg.in/yaml.v3"
)

func main() {
	decoder := yaml.NewDecoder(bufio.NewReader(os.Stdin))

	var value any
	if err := decoder.Decode(&value); err != nil {
		os.Exit(1)
	}

	encoder := yaml.NewEncoder(os.Stdout)
	encoder.SetIndent(2)

	if err := encoder.Encode(value); err != nil {
		os.Exit(1)
	}
}
