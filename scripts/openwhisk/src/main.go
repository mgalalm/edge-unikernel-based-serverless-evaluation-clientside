package main
import "time"
func Main(args map[string]interface{}) map[string]interface{} {
    time.Sleep(20 * time.Second) 
	msg := make(map[string]interface{})
	msg["message"] = "Hello World Openwhisk"
	msg["version"] = 1.0
	return msg
}
