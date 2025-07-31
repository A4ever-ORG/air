package platform

import (
	"fmt"
	"os/exec"

	"github.com/fatih/color"
)

// TermuxOptimizations provides Termux-specific features and optimizations
type TermuxOptimizations struct {
	MobileTools     []string
	AndroidTools    []string
	NetworkTools    []string
	SecurityTools   []string
	TermuxAPITools  []string
}

// GetTermuxOptimizations returns Termux-specific optimizations
func GetTermuxOptimizations() *TermuxOptimizations {
	return &TermuxOptimizations{
		MobileTools: []string{
			"termux-api",
			"termux-tools",
			"termux-services",
			"termux-exec",
			"termux-battery-status",
			"termux-location",
			"termux-camera-info",
			"termux-sensor-list",
			"termux-wifi-scaninfo",
			"termux-bluetooth-scan",
		},
		AndroidTools: []string{
			"adb",
			"fastboot",
			"android-tools",
			"scrcpy",
			"android-sdk",
			"android-ndk",
			"gradle",
			"apktool",
			"jadx",
			"dex2jar",
		},
		NetworkTools: []string{
			"nmap",
			"ping",
			"traceroute",
			"netcat",
			"curl",
			"wget",
			"ssh",
			"telnet",
			"ftp",
			"httping",
		},
		SecurityTools: []string{
			"hashcat",
			"john",
			"hydra",
			"sqlmap",
			"nikto",
			"dirb",
			"gobuster",
			"nuclei",
			"subfinder",
			"amass",
		},
		TermuxAPITools: []string{
			"termux-vibrate",
			"termux-toast",
			"termux-notification",
			"termux-share",
			"termux-download",
			"termux-call-log",
			"termux-contact-list",
			"termux-sms-list",
			"termux-telephony-deviceinfo",
			"termux-usb",
		},
	}
}

// CheckTermuxToolsAvailability checks which Termux tools are available
func CheckTermuxToolsAvailability() map[string]bool {
	optimizations := GetTermuxOptimizations()
	availability := make(map[string]bool)

	// Check mobile tools
	for _, tool := range optimizations.MobileTools {
		availability[tool] = isTermuxToolAvailable(tool)
	}

	// Check Android tools
	for _, tool := range optimizations.AndroidTools {
		availability[tool] = isTermuxToolAvailable(tool)
	}

	// Check network tools
	for _, tool := range optimizations.NetworkTools {
		availability[tool] = isTermuxToolAvailable(tool)
	}

	// Check security tools
	for _, tool := range optimizations.SecurityTools {
		availability[tool] = isTermuxToolAvailable(tool)
	}

	// Check Termux API tools
	for _, tool := range optimizations.TermuxAPITools {
		availability[tool] = isTermuxToolAvailable(tool)
	}

	return availability
}

// isTermuxToolAvailable checks if a Termux tool is available
func isTermuxToolAvailable(tool string) bool {
	cmd := exec.Command("which", tool)
	err := cmd.Run()
	return err == nil
}

// ShowTermuxToolsStatus displays the status of available Termux tools
func ShowTermuxToolsStatus() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("📱 Termux Tools Status")
	fmt.Println()

	optimizations := GetTermuxOptimizations()
	availability := CheckTermuxToolsAvailability()

	// Mobile Tools
	green.Println("📱 Mobile Optimization Tools:")
	for _, tool := range optimizations.MobileTools {
		if availability[tool] {
			green.Printf("  ✅ %s\n", tool)
		} else {
			red.Printf("  ❌ %s\n", tool)
		}
	}
	fmt.Println()

	// Android Tools
	green.Println("🤖 Android Development Tools:")
	for _, tool := range optimizations.AndroidTools {
		if availability[tool] {
			green.Printf("  ✅ %s\n", tool)
		} else {
			red.Printf("  ❌ %s\n", tool)
		}
	}
	fmt.Println()

	// Network Tools
	green.Println("🌐 Network Analysis Tools:")
	for _, tool := range optimizations.NetworkTools {
		if availability[tool] {
			green.Printf("  ✅ %s\n", tool)
		} else {
			red.Printf("  ❌ %s\n", tool)
		}
	}
	fmt.Println()

	// Security Tools
	green.Println("🔒 Security Analysis Tools:")
	for _, tool := range optimizations.SecurityTools {
		if availability[tool] {
			green.Printf("  ✅ %s\n", tool)
		} else {
			red.Printf("  ❌ %s\n", tool)
		}
	}
	fmt.Println()

	// Termux API Tools
	green.Println("🔧 Termux API Tools:")
	for _, tool := range optimizations.TermuxAPITools {
		if availability[tool] {
			green.Printf("  ✅ %s\n", tool)
		} else {
			red.Printf("  ❌ %s\n", tool)
		}
	}
	fmt.Println()

	// Summary
	availableCount := 0
	totalCount := len(optimizations.MobileTools) + len(optimizations.AndroidTools) + 
		len(optimizations.NetworkTools) + len(optimizations.SecurityTools) + len(optimizations.TermuxAPITools)

	for _, available := range availability {
		if available {
			availableCount++
		}
	}

	yellow.Printf("📊 Summary: %d/%d tools available (%.1f%%)\n", 
		availableCount, totalCount, float64(availableCount)/float64(totalCount)*100)
	fmt.Println()
}

// GetTermuxInstallationGuide returns comprehensive Termux installation guide
func GetTermuxInstallationGuide() string {
	return `📱 Termux Installation Guide

📋 Prerequisites:
   • Android 7.0 or higher
   • Termux app installed from F-Droid
   • Internet connection
   • At least 2GB free storage

🚀 Quick Installation:
   1. Update Termux:
      pkg update && pkg upgrade -y

   2. Install essential packages:
      pkg install git golang

   3. Install additional tools (optional):
      pkg install nmap curl wget openssh
      pkg install hashcat john hydra sqlmap

   4. Install Termux API (for Android integration):
      pkg install termux-api

   5. Clone the repository:
      git clone https://github.com/awesome-project/go-multi-platform.git
      cd go-multi-platform

   6. Build the application:
      go build -o go-multi-platform

   7. Install locally:
      cp go-multi-platform ~/.local/bin/
      chmod +x ~/.local/bin/go-multi-platform

   8. Add to PATH (add to ~/.bashrc):
      echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
      source ~/.bashrc

   9. Create desktop shortcut (optional):
      echo '#!/data/data/com.termux/files/usr/bin/bash
      cd ~/go-multi-platform
      ./go-multi-platform' > ~/Desktop/go-multi-platform.sh
      chmod +x ~/Desktop/go-multi-platform.sh

   10. Run the application:
       go-multi-platform

🎯 Termux-Specific Features:
    • Mobile-optimized interface
    • Touch-friendly controls
    • Battery optimization
    • Android API integration
    • Offline capability
    • Low-resource optimization
    • Mobile security testing
    • Android app analysis

🔧 Additional Setup (Optional):
    • Install Termux Widgets: pkg install termux-widget
    • Set up Termux Services: pkg install termux-services
    • Install Termux Styling: pkg install termux-styling
    • Configure Termux API permissions in Android settings
    • Set up SSH server: sshd
    • Install additional security tools: pkg install metasploit

📱 Mobile Optimizations:
    • Touch gesture support
    • Battery usage optimization
    • Mobile-optimized scanning
    • Android sensor integration
    • Camera and GPS access
    • Bluetooth scanning capabilities

🎉 Enjoy your Termux optimized experience!`
}

// GetTermuxAdvancedFeatures returns advanced Termux-specific features
func GetTermuxAdvancedFeatures() []string {
	return []string{
		"Mobile-optimized penetration testing",
		"Android app security analysis",
		"Touch-friendly interface design",
		"Battery-efficient operations",
		"Android sensor data integration",
		"Mobile network scanning",
		"Bluetooth security testing",
		"WiFi network analysis",
		"Android API integration",
		"Mobile forensics capabilities",
		"Offline security testing",
		"Mobile-specific exploits",
		"Android malware analysis",
		"Mobile app reverse engineering",
		"GPS-based security testing",
		"Camera-based security tools",
		"Mobile social engineering",
		"Android device fingerprinting",
		"Mobile incident response",
		"Touch gesture controls",
	}
}

// ShowTermuxAdvancedFeatures displays advanced Termux features
func ShowTermuxAdvancedFeatures() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)

	cyan.Println("🚀 Termux Advanced Features")
	fmt.Println()

	features := GetTermuxAdvancedFeatures()
	for i, feature := range features {
		green.Printf("  %d. %s\n", i+1, feature)
	}
	fmt.Println()

	yellow.Println("💡 These features are specifically optimized for Termux on Android")
	yellow.Println("   and provide mobile-optimized security testing capabilities.")
	fmt.Println()
}

// GetTermuxBatteryOptimization returns battery optimization tips
func GetTermuxBatteryOptimization() []string {
	return []string{
		"Use low-power scanning modes",
		"Disable unnecessary background processes",
		"Optimize network scanning intervals",
		"Use efficient algorithms for mobile",
		"Implement smart caching strategies",
		"Reduce CPU-intensive operations",
		"Optimize memory usage for mobile",
		"Use Android's battery optimization",
		"Implement adaptive scanning",
		"Monitor battery usage in real-time",
	}
}

// ShowTermuxBatteryOptimization displays battery optimization tips
func ShowTermuxBatteryOptimization() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)

	cyan.Println("🔋 Termux Battery Optimization")
	fmt.Println()

	optimizations := GetTermuxBatteryOptimization()
	for i, optimization := range optimizations {
		green.Printf("  %d. %s\n", i+1, optimization)
	}
	fmt.Println()

	yellow.Println("💡 These optimizations help extend battery life during security testing.")
	fmt.Println()
}