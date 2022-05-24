package main
import "time"
func Main(args map[string]interface{}) map[string]interface{} {
    time.Sleep(2 * time.Second) 
	msg := make(map[string]interface{})
	msg["message"] = "Hello World Openwhisk"
	msg["version"] = 2
	return msg
}
