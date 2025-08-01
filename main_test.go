package main

import (
	"testing"
	"os"
	"os/exec"
)

func TestMainFunctionality(t *testing.T) {
	// Test if the application builds without errors
	cmd := exec.Command("go", "build", "-o", "test-binary")
	err := cmd.Run()
	if err != nil {
		t.Fatalf("Failed to build application: %v", err)
	}
	
	// Clean up
	defer os.Remove("test-binary")
	
	// Test if the binary exists and is executable
	if _, err := os.Stat("test-binary"); os.IsNotExist(err) {
		t.Fatal("Binary was not created")
	}
}

func TestShowBanner(t *testing.T) {
	// Test that showBanner doesn't panic
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("showBanner panicked: %v", r)
		}
	}()
	
	showBanner()
}