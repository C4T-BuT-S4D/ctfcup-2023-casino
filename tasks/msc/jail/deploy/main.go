package main

import (
	"context"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/gofiber/fiber/v2/middleware/timeout"
	"github.com/mattn/anko/env"
	"github.com/mattn/anko/vm"
)

func main() {
	env.Packages = make(map[string]map[string]reflect.Value)
	env.PackageTypes = make(map[string]map[string]reflect.Type)

	escape := func(c *fiber.Ctx) error {
		globalEnv := env.NewEnv()
		_ = globalEnv.DefineGlobal("whitelist", []string{"/tools/", "/jokes/"})
		_ = globalEnv.DefineGlobal("read", func(filename string) string {
			filename = filepath.Clean(filename)
			whitelist, _ := globalEnv.Get("whitelist")
			for _, prefix := range whitelist.([]string) {
				if strings.HasPrefix(filename, prefix) {
					content, err := os.ReadFile(filename)
					if err != nil {
						return err.Error()
					}
					return string(content)
				}
			}
			return "Access denied"
		})

		ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
		defer cancel()

		childEnv := globalEnv.NewEnv()
		childEnv.Define("whitelist", []string{})

		result, err := vm.ExecuteContext(ctx, childEnv.NewEnv(), nil, string(c.Body()))
		if err != nil {
			return c.JSON(map[string]string{"error": err.Error()})
		}

		return c.JSON(map[string]any{"result": result})
	}

	app := fiber.New()
	app.Use(recover.New())
	app.Post("/escape", timeout.NewWithContext(escape, 2*time.Second))
	app.Listen(":3000")
}
