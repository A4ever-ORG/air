package platform

import (
	"fmt"
	"os"
	"runtime"
	"strings"
	"time"

	"github.com/fatih/color"
	"github.com/shirou/gopsutil/v3/host"
)

type PlatformInfo struct {
	Name        string
	OS          string
	Arch        string
	Kernel      string
	IsKali      bool
	IsTermux    bool
	Features    []string
	InstallPath string
}

var (
	platformInfo *PlatformInfo
	initialized  bool
)

func Init() {
	if initialized {
		return
	}

	platformInfo = &PlatformInfo{
		OS:     runtime.GOOS,
		Arch:   runtime.GOARCH,
		Kernel: getKernelVersion(),
	}

	// Detect platform
	detectPlatform()
	initialized = true
}

func GetPlatformInfo() *PlatformInfo {
	if !initialized {
		Init()
	}
	return platformInfo
}

func detectPlatform() {
	// Check for Termux
	if isTermux() {
		platformInfo.Name = "Termux (Android)"
		platformInfo.IsTermux = true
		platformInfo.Features = []string{
			"Android compatibility",
			"Termux API support",
			"Mobile-optimized UI",
			"Touch-friendly interface",
			"Battery optimization",
		}
		platformInfo.InstallPath = "/data/data/com.termux/files/home"
		return
	}

	// Check for Kali Linux
	if isKaliLinux() {
		platformInfo.Name = "Kali Linux"
		platformInfo.IsKali = true
		platformInfo.Features = []string{
			"Penetration testing tools",
			"Security analysis",
			"Network scanning",
			"Forensic capabilities",
			"Advanced networking",
		}
		platformInfo.InstallPath = "/usr/local/bin"
		return
	}

	// Default Linux
	platformInfo.Name = "Linux"
	platformInfo.Features = []string{
		"Standard Linux support",
		"Cross-platform compatibility",
		"Basic functionality",
	}
	platformInfo.InstallPath = "/usr/local/bin"
}

func isTermux() bool {
	// Check for Termux environment
	termuxEnv := os.Getenv("TERMUX_VERSION")
	if termuxEnv != "" {
		return true
	}

	// Check for Termux path
	if strings.Contains(os.Getenv("PATH"), "com.termux") {
		return true
	}

	// Check for Android
	if runtime.GOOS == "android" {
		return true
	}

	return false
}

func isKaliLinux() bool {
	// Check for Kali Linux specific files
	if _, err := os.Stat("/etc/os-release"); err == nil {
		data, err := os.ReadFile("/etc/os-release")
		if err == nil {
			content := string(data)
			if strings.Contains(strings.ToLower(content), "kali") {
				return true
			}
		}
	}

	// Check for Kali Linux hostname
	hostname, err := os.Hostname()
	if err == nil && strings.Contains(strings.ToLower(hostname), "kali") {
		return true
	}

	return false
}

func getKernelVersion() string {
	info, err := host.Info()
	if err != nil {
		return "Unknown"
	}
	return info.PlatformVersion
}

// Platform-specific functions
func ShowPlatformFeatures() {
	info := GetPlatformInfo()
	
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	
	cyan.Println("🎯 Platform Features:")
	fmt.Println()
	
	for i, feature := range info.Features {
		green.Printf("  %d. %s\n", i+1, feature)
	}
	fmt.Println()
	
	yellow.Printf("📁 Install Path: %s\n", info.InstallPath)
	fmt.Println()
}

func GetInstallationInstructions() string {
	info := GetPlatformInfo()
	
	if info.IsKali {
		return getKaliInstallInstructions()
	} else if info.IsTermux {
		return getTermuxInstallInstructions()
	}
	
	return getGenericInstallInstructions()
}

func getKaliInstallInstructions() string {
	return GetKaliInstallationGuide()
}

func getTermuxInstallInstructions() string {
	return GetTermuxInstallationGuide()
}

func getGenericInstallInstructions() string {
	return `🖥️  Generic Linux Installation:

1. Install Go:
   # Ubuntu/Debian
   sudo apt install golang-go
   
   # CentOS/RHEL
   sudo yum install golang

2. Clone and build:
   git clone https://github.com/awesome-project/go-multi-platform.git
   cd go-multi-platform
   go build -o go-multi-platform

3. Install:
   sudo cp go-multi-platform /usr/local/bin/
   sudo chmod +x /usr/local/bin/go-multi-platform

4. Run:
   go-multi-platform`
}