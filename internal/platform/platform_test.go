package platform

import (
	"testing"
	"runtime"
)

func TestInit(t *testing.T) {
	// Reset for clean test
	initialized = false
	platformInfo = nil
	
	Init()
	
	if !initialized {
		t.Error("Init() should set initialized to true")
	}
	
	if platformInfo == nil {
		t.Error("Init() should initialize platformInfo")
	}
}

func TestGetPlatformInfo(t *testing.T) {
	info := GetPlatformInfo()
	
	if info == nil {
		t.Error("GetPlatformInfo() should not return nil")
	}
	
	if info.OS != runtime.GOOS {
		t.Errorf("Expected OS %s, got %s", runtime.GOOS, info.OS)
	}
	
	if info.Arch != runtime.GOARCH {
		t.Errorf("Expected Arch %s, got %s", runtime.GOARCH, info.Arch)
	}
	
	if info.Name == "" {
		t.Error("Platform name should not be empty")
	}
	
	if len(info.Features) == 0 {
		t.Error("Platform should have at least one feature")
	}
	
	if info.InstallPath == "" {
		t.Error("Install path should not be empty")
	}
}

func TestDetectPlatform(t *testing.T) {
	// Reset for clean test
	platformInfo = &PlatformInfo{
		OS:   runtime.GOOS,
		Arch: runtime.GOARCH,
	}
	
	detectPlatform()
	
	// Basic validation that detection completed
	if platformInfo.Name == "" {
		t.Error("Platform detection should set a name")
	}
}

func TestIsTermux(t *testing.T) {
	// This test will typically return false in a standard environment
	result := isTermux()
	
	// We can't assert the specific value since it depends on the environment
	// But we can ensure the function doesn't panic
	_ = result
}

func TestIsKaliLinux(t *testing.T) {
	// This test will typically return false in a standard environment
	result := isKaliLinux()
	
	// We can't assert the specific value since it depends on the environment
	// But we can ensure the function doesn't panic
	_ = result
}

func TestGetKernelVersion(t *testing.T) {
	version := getKernelVersion()
	
	if version == "" {
		t.Error("Kernel version should not be empty")
	}
}

func TestGetInstallationInstructions(t *testing.T) {
	instructions := GetInstallationInstructions()
	
	if instructions == "" {
		t.Error("Installation instructions should not be empty")
	}
	
	// Should contain basic installation steps
	if len(instructions) < 50 {
		t.Error("Installation instructions seem too short")
	}
}