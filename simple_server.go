package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
)

// JSON-RPC message structure
type Request struct {
	JSONRPC string          `json:"jsonrpc"`
	ID      json.RawMessage `json:"id,omitempty"`
	Method  string          `json:"method"`
	Params  json.RawMessage `json:"params,omitempty"`
}

type Response struct {
	JSONRPC string      `json:"jsonrpc"`
	ID      json.RawMessage `json:"id,omitempty"`
	Result  interface{} `json:"result,omitempty"`
	Error   *RespError  `json:"error,omitempty"`
}

type RespError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

// Tool call params
type ToolCallParams struct {
	Name      string                 `json:"name"`
	Arguments map[string]interface{} `json:"arguments"`
}

// Helper: send response to stdout
func send(resp Response) {
	enc := json.NewEncoder(os.Stdout)
	enc.SetEscapeHTML(false)
	err := enc.Encode(resp)
	if err != nil {
		log.Printf("SERVER: [ERROR] failed to send response: %v\n", err)
	}
}

func main() {
	// log to stderr
	log.SetOutput(os.Stderr)
	log.Println("SERVER: [INFO] Simple MCP server (Go) starting up...")

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		var req Request
		if err := json.Unmarshal([]byte(line), &req); err != nil {
			log.Printf("SERVER: [ERROR] failed to parse: %s\n", err)
			continue
		}
		log.Printf("SERVER: [INFO] Received request: %+v\n", req)

		switch req.Method {
		case "initialize":
			send(Response{
				JSONRPC: "2.0",
				ID:      req.ID,
				Result: map[string]interface{}{
					"protocolVersion": "2025-06-18",
					"capabilities": map[string]interface{}{
						"tools": map[string]bool{"listChanged": true},
					},
					"serverInfo": map[string]string{
						"name":    "SimpleGoServer",
						"version": "0.1",
					},
				},
			})

		case "notifications/initialized":
			// no-op, no response

		case "tools/list":
			send(Response{
				JSONRPC: "2.0",
				ID:      req.ID,
				Result: map[string]interface{}{
					"tools": []map[string]interface{}{
						{
							"name":        "greet",
							"description": "Greet someone by name.",
							"inputSchema": map[string]interface{}{
								"type": "object",
								"properties": map[string]interface{}{
									"name": map[string]string{"type": "string"},
								},
								"required": []string{"name"},
							},
							"outputSchema": map[string]interface{}{
								"type": "object",
								"properties": map[string]interface{}{
									"result": map[string]string{"type": "string"},
								},
								"required": []string{"result"},
							},
						},
					},
				},
			})

		case "tools/call":
			var params ToolCallParams
			if err := json.Unmarshal(req.Params, &params); err != nil {
				log.Printf("SERVER: [ERROR] bad tool call params: %v\n", err)
				send(Response{
					JSONRPC: "2.0",
					ID:      req.ID,
					Error:   &RespError{Code: -32602, Message: "Invalid params"},
				})
				continue
			}
			name := "stranger"
			if v, ok := params.Arguments["name"].(string); ok {
				name = v
			}
			greeting := fmt.Sprintf("Hello, %s!", name)
			send(Response{
				JSONRPC: "2.0",
				ID:      req.ID,
				Result: map[string]interface{}{
					"content": []map[string]string{
						{"type": "text", "text": greeting},
					},
					"structuredContent": map[string]string{
						"result": greeting,
					},
					"isError": false,
				},
			})

		default:
			send(Response{
				JSONRPC: "2.0",
				ID:      req.ID,
				Error:   &RespError{Code: -32601, Message: "Method not found"},
			})
		}
	}
}
