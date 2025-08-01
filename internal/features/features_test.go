package features

import (
	"testing"
	"bytes"
	"os"
	"io"
)

func TestShowSystemInfo(t *testing.T) {
	// Capture output to ensure function doesn't panic
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("ShowSystemInfo panicked: %v", r)
		}
		os.Stdout = old
	}()
	
	ShowSystemInfo()
	
	w.Close()
	os.Stdout = old
	
	// Read captured output
	var buf bytes.Buffer
	io.Copy(&buf, r)
	
	output := buf.String()
	if output == "" {
		t.Error("ShowSystemInfo should produce output")
	}
}

func TestShowNetworkTools(t *testing.T) {
	// Test that function doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("ShowNetworkTools panicked: %v", r)
		}
	}()
	
	ShowNetworkTools()
}

func TestShowSecurityTools(t *testing.T) {
	// Test that function doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("ShowSecurityTools panicked: %v", r)
		}
	}()
	
	ShowSecurityTools()
}

func TestShowKaliTools(t *testing.T) {
	// Test that function doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("ShowKaliTools panicked: %v", r)
		}
	}()
	
	ShowKaliTools()
}

func TestShowTermuxTools(t *testing.T) {
	// Test that function doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("ShowTermuxTools panicked: %v", r)
		}
	}()
	
	ShowTermuxTools()
}

func TestRunDemo(t *testing.T) {
	// Test that function doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("RunDemo panicked: %v", r)
		}
	}()
	
	// Note: This test might take a few seconds due to spinner animations
	// In a real test environment, you might want to mock the time.Sleep calls
	RunDemo()
}