package platform

import (
	"fmt"
	"os/exec"

	"github.com/fatih/color"
)

// KaliLinuxOptimizations provides Kali-specific features and optimizations
type KaliLinuxOptimizations struct {
	PenetrationTools []string
	SecurityTools    []string
	NetworkTools     []string
	ForensicTools    []string
}

// GetKaliOptimizations returns Kali Linux specific optimizations
func GetKaliOptimizations() *KaliLinuxOptimizations {
	return &KaliLinuxOptimizations{
		PenetrationTools: []string{
			"metasploit-framework",
			"nmap",
			"wireshark",
			"aircrack-ng",
			"john",
			"hashcat",
			"sqlmap",
			"burpsuite",
			"beef-xss",
			"social-engineer-toolkit",
		},
		SecurityTools: []string{
			"nikto",
			"dirb",
			"gobuster",
			"hydra",
			"medusa",
			"ncrack",
			"openvas",
			"nessus",
			"w3af",
			"zap",
		},
		NetworkTools: []string{
			"tcpdump",
			"tshark",
			"ettercap-graphical",
			"kismet",
			"reaver",
			"wash",
			"mdk4",
			"mdk3",
			"hostapd-wpe",
			"eaphammer",
		},
		ForensicTools: []string{
			"autopsy",
			"volatility",
			"foremost",
			"scalpel",
			"testdisk",
			"photorec",
			"bulk_extractor",
			"binwalk",
			"strings",
			"hexdump",
		},
	}
}

// CheckKaliToolsAvailability checks which Kali tools are available
func CheckKaliToolsAvailability() map[string]bool {
	optimizations := GetKaliOptimizations()
	availability := make(map[string]bool)

	// Check penetration tools
	for _, tool := range optimizations.PenetrationTools {
		availability[tool] = isToolAvailable(tool)
	}

	// Check security tools
	for _, tool := range optimizations.SecurityTools {
		availability[tool] = isToolAvailable(tool)
	}

	// Check network tools
	for _, tool := range optimizations.NetworkTools {
		availability[tool] = isToolAvailable(tool)
	}

	// Check forensic tools
	for _, tool := range optimizations.ForensicTools {
		availability[tool] = isToolAvailable(tool)
	}

	return availability
}

// isToolAvailable checks if a tool is available in the system
func isToolAvailable(tool string) bool {
	cmd := exec.Command("which", tool)
	err := cmd.Run()
	return err == nil
}

// ShowKaliToolsStatus displays the status of available Kali tools
func ShowKaliToolsStatus() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)
	red := color.New(color.FgRed, color.Bold)

	cyan.Println("⚔️ Kali Linux Tools Status")
	fmt.Println()

	optimizations := GetKaliOptimizations()
	availability := CheckKaliToolsAvailability()

	// Penetration Tools
	green.Println("🎯 Penetration Testing Tools:")
	for _, tool := range optimizations.PenetrationTools {
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

	// Forensic Tools
	green.Println("🔍 Forensic Analysis Tools:")
	for _, tool := range optimizations.ForensicTools {
		if availability[tool] {
			green.Printf("  ✅ %s\n", tool)
		} else {
			red.Printf("  ❌ %s\n", tool)
		}
	}
	fmt.Println()

	// Summary
	availableCount := 0
	totalCount := len(optimizations.PenetrationTools) + len(optimizations.SecurityTools) + 
		len(optimizations.NetworkTools) + len(optimizations.ForensicTools)

	for _, available := range availability {
		if available {
			availableCount++
		}
	}

	yellow.Printf("📊 Summary: %d/%d tools available (%.1f%%)\n", 
		availableCount, totalCount, float64(availableCount)/float64(totalCount)*100)
	fmt.Println()
}

// GetKaliInstallationGuide returns comprehensive Kali installation guide
func GetKaliInstallationGuide() string {
	return `🔧 Kali Linux Installation Guide

📋 Prerequisites:
   • Kali Linux 2023.1 or later
   • Root or sudo access
   • Internet connection

🚀 Quick Installation:
   1. Update Kali Linux:
      sudo apt update && sudo apt upgrade -y

   2. Install Go (if not installed):
      sudo apt install golang-go

   3. Clone the repository:
      git clone https://github.com/awesome-project/go-multi-platform.git
      cd go-multi-platform

   4. Build the application:
      go build -o go-multi-platform

   5. Install system-wide:
      sudo cp go-multi-platform /usr/local/bin/
      sudo chmod +x /usr/local/bin/go-multi-platform

   6. Create desktop shortcut:
      echo "[Desktop Entry]
      Name=Go Multi-Platform
      Comment=Advanced Multi-Platform Go Application
      Exec=/usr/local/bin/go-multi-platform
      Icon=terminal
      Terminal=true
      Type=Application
      Categories=System;Security;" > ~/Desktop/go-multi-platform.desktop
      chmod +x ~/Desktop/go-multi-platform.desktop

   7. Run the application:
      go-multi-platform

🎯 Kali-Specific Features:
   • Integration with Kali penetration testing tools
   • Advanced network scanning capabilities
   • Security analysis and vulnerability assessment
   • Forensic analysis tools
   • Professional reporting features
   • Automated penetration testing workflows

🔧 Additional Setup (Optional):
   • Install additional Kali tools: sudo apt install kali-linux-full
   • Configure Metasploit: msfdb init
   • Set up OpenVAS: sudo apt install openvas
   • Configure Wireshark: sudo usermod -a -G wireshark $USER

🎉 Enjoy your Kali Linux optimized experience!`
}

// GetKaliAdvancedFeatures returns advanced Kali-specific features
func GetKaliAdvancedFeatures() []string {
	return []string{
		"Automated penetration testing workflows",
		"Integration with Metasploit Framework",
		"Advanced network traffic analysis",
		"Wireless network security testing",
		"Web application security scanning",
		"Social engineering toolkit integration",
		"Forensic analysis capabilities",
		"Custom exploit development",
		"Advanced evasion techniques",
		"Professional security reporting",
		"Real-time threat intelligence",
		"Vulnerability assessment automation",
		"Incident response tools",
		"Malware analysis integration",
		"Advanced logging and monitoring",
	}
}

// ShowKaliAdvancedFeatures displays advanced Kali features
func ShowKaliAdvancedFeatures() {
	cyan := color.New(color.FgCyan, color.Bold)
	green := color.New(color.FgGreen, color.Bold)
	yellow := color.New(color.FgYellow, color.Bold)

	cyan.Println("🚀 Kali Linux Advanced Features")
	fmt.Println()

	features := GetKaliAdvancedFeatures()
	for i, feature := range features {
		green.Printf("  %d. %s\n", i+1, feature)
	}
	fmt.Println()

	yellow.Println("💡 These features are specifically optimized for Kali Linux")
	yellow.Println("   and provide professional-grade security testing capabilities.")
	fmt.Println()
}